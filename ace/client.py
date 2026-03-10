"""
ACE Context Engineering - Client API.

Provides the context-provider API for injecting ACE into any LLM framework.
"""

import asyncio
import threading
import uuid
import warnings
from typing import Any, Dict, List, Optional, Tuple

from ace.config import ACEConfig
from ace.curator import Curator
from ace.playbook.manager import PlaybookManager
from ace.reflector import Reflector

class ACEClient:
    """The central client for Agentic Context Engineering.
    
    Acts as a 'Context Provider' that allows developers to fetch dynamic rules 
    and asynchronously submit feedback without blocking their applications.
    
    Args:
        playbook_name (str): Name of the playbook to use.
        vector_store (str): Type of vector store ('faiss', 'chromadb', 'qdrant').
        config (Optional[ACEConfig]): ACE configuration object. If provided, overrides 
                                      individual parameters.
        **kwargs: Additional arguments passed to PlaybookManager.
    """
    
    def __init__(
        self,
        playbook_name: str = "default",
        vector_store: str = "faiss",
        config: Optional[ACEConfig] = None,
        **kwargs
    ):
        self.config = config or ACEConfig(
            playbook_name=playbook_name, 
            vector_store=vector_store,
            **kwargs
        )
        
        self.playbook = PlaybookManager(
            playbook_dir=self.config.get_storage_path(),
            vector_store=self.config.vector_store,
            embedding_model=self.config.embedding_model,
            qdrant_url=self.config.qdrant_url if self.config.vector_store in ["qdrant", "qdrant-cloud"] else None,
            qdrant_api_key=self.config.qdrant_api_key if self.config.vector_store == "qdrant-cloud" else None,
            embedding_model_kwargs=self.config.embedding_model_kwargs
        )
        
        # Initialize internal state for tracking interactions
        # Maps interaction_id -> Dict containing interaction details needed for feedback
        self._interactions: Dict[str, Dict[str, Any]] = {}
        
        # Lazy initialization for Reflector and Curator (only needed on feedback)
        self._reflector = None
        self._curator = None
        
        print(f" ACEClient initialized for playbook '{playbook_name}'")
        
    def _get_reflector(self) -> Reflector:
        if self._reflector is None:
            self._reflector = Reflector(
                model=self.config.chat_model,
                storage_path=self.config.get_storage_path(),
                model_kwargs=self.config.chat_model_kwargs
            )
        return self._reflector
        
    def _get_curator(self) -> Curator:
        if self._curator is None:
            self._curator = Curator(
                playbook_manager=self.playbook,
                storage_path=self.config.get_storage_path()
            )
        return self._curator

    def get_context(self, user_query: str, top_k: Optional[int] = None) -> Tuple[str, str]:
        """Fetch the most relevant playbook context for a given query (Synchronous).
        
        Args:
            user_query (str): The query or current user intent.
            top_k (Optional[int]): Number of bullets to retrieve. Defaults to config.top_k.
            
        Returns:
            Tuple[str, str]: A tuple containing:
                - Formatted markdown context string.
                - A unique interaction ID to pass later to `submit_feedback`.
        """
        k = top_k if top_k is not None else self.config.top_k
        bullets = self.playbook.retrieve_relevant(user_query, top_k=k)
        used_bullets = [b.id for b in bullets]
        
        context_parts = ["# ACE Playbook Context\n"]
        context_parts.append("Use the following strategies from the playbook:\n")
        
        for bullet in bullets:
            context_parts.append(bullet.to_markdown())
            
        context_string = "\n\n".join(context_parts) if bullets else ""
        
        interaction_id = str(uuid.uuid4())
        
        # Store for future feedback submission
        self._interactions[interaction_id] = {
            "question": user_query,
            "used_bullets": used_bullets,
            # We don't have the model response here since the dev calls the model later,
            # but Reflector gracefully handles cases without exact model responses
            # if we document it. Ideally, developers can pass response during feedback.
            "model_response": ""
        }
        
        return context_string, interaction_id

    async def aget_context(self, user_query: str, top_k: Optional[int] = None) -> Tuple[str, str]:
        """Fetch the most relevant playbook context for a given query (Asynchronous).
        
        This method is preferred for async frameworks like FastAPI.
        
        Args:
            user_query (str): The query or current user intent.
            top_k (Optional[int]): Number of bullets to retrieve. Defaults to config.top_k.
            
        Returns:
            Tuple[str, str]: Context markdown string and interaction ID.
        """
        # Playbook retrieve_relevant is currently CPU/memory bound operations locally or fast HTTP
        # In the future, this can be pushed to an async executor
        return self.get_context(user_query, top_k)

    def _process_feedback_pipeline(self, interaction_data: Dict[str, Any], feedback_data: Any) -> None:
        """Internal synchronous method that runs the heavy Reflector/Curator pipeline."""
        try:
            reflector = self._get_reflector()
            curator = self._get_curator()
            
            insight = reflector.analyze_feedback(
                chat_data=interaction_data,
                feedback_data=feedback_data
            )
            
            delta = curator.process_insights(insight, feedback_data.feedback_id)
            
            if delta.total_operations > 0:
                curator.merge_delta(delta)
            
            # Use bullet_tags from Reflector if available
            used_bullets = interaction_data.get("used_bullets", [])
            
            if insight.bullet_tags:
                for bullet_tag in insight.bullet_tags:
                    bullet_id = bullet_tag.get("id")
                    tag = bullet_tag.get("tag", "").lower()
                    if bullet_id and tag == "helpful":
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif bullet_id and tag == "harmful":
                        self.playbook.update_counters(bullet_id, helpful=False)
            else:
                # Fallback: simple evaluation based on rating
                rating = feedback_data.rating
                is_positive = rating >= 4
                is_negative = rating <= 2
                for bullet_id in used_bullets:
                    if is_positive:
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif is_negative:
                        self.playbook.update_counters(bullet_id, helpful=False)
                        
            print(f" ACE Feedback pipeline completed successfully for {feedback_data.feedback_id}")
            
        except Exception as e:
            print(f" ACE Feedback processing error: {e}")

    def submit_feedback(
        self,
        interaction_id: str,
        user_feedback: str,
        rating: int,
        feedback_type: str = "user_feedback",
        model_response: str = ""
    ) -> bool:
        """Submit feedback for a specific interaction synchronously without blocking main thread.
        
        This spawns a background thread to handle the Reflector/Curator pipeline.
        
        Args:
            interaction_id (str): The ID returned from `get_context`.
            user_feedback (str): Text feedback explaining what went right or wrong.
            rating (int): Integer from 1 (terrible) to 5 (excellent).
            feedback_type (str): Type of feedback ('user_feedback', 'incorrect', etc.).
            model_response (str): The actual output from the LLM, highly recommended to include
                                  so the Reflector can analyze the mistake exactly.
            
        Returns:
            bool: True if feedback was successfully queued.
        """
        interaction_data = self._interactions.get(interaction_id)
        if not interaction_data:
            warnings.warn(f"Interaction ID {interaction_id} not found or expired.")
            return False
            
        # Update response if provided
        if model_response:
            interaction_data["model_response"] = model_response
            
        class FeedbackData:
            def __init__(self, feedback_type, user_feedback, rating, feedback_id):
                self.feedback_type = feedback_type
                self.user_feedback = user_feedback
                self.rating = rating
                self.feedback_id = feedback_id
                
        feedback_data = FeedbackData(
            feedback_type=feedback_type,
            user_feedback=user_feedback,
            rating=rating,
            feedback_id=f"fb_{interaction_id}"
        )
        
        # Fire and forget using a background thread
        thread = threading.Thread(
            target=self._process_feedback_pipeline,
            args=(interaction_data, feedback_data)
        )
        thread.daemon = True
        thread.start()
        
        # Optionally remove interaction array to prevent memory leaks if many requests form
        # self._interactions.pop(interaction_id, None)
        
        return True

    async def asubmit_feedback(
        self,
        interaction_id: str,
        user_feedback: str,
        rating: int,
        feedback_type: str = "user_feedback",
        model_response: str = ""
    ) -> bool:
        """Asynchronously submit feedback without blocking current async execution.
        
        Highly recommended for FastAPI, AIOHTTP, etc.
        
        Args:
            interaction_id (str): The ID returned from `aget_context`.
            user_feedback (str): Text feedback explaining what went right or wrong.
            rating (int): Integer from 1 (terrible) to 5 (excellent).
            feedback_type (str): Type of feedback.
            model_response (str): The LLM response the user is rating.
            
        Returns:
            bool: True if feedback was successfully queued.
        """
        interaction_data = self._interactions.get(interaction_id)
        if not interaction_data:
            warnings.warn(f"Interaction ID {interaction_id} not found or expired.")
            return False
            
        if model_response:
            interaction_data["model_response"] = model_response
            
        class FeedbackData:
            def __init__(self, feedback_type, user_feedback, rating, feedback_id):
                self.feedback_type = feedback_type
                self.user_feedback = user_feedback
                self.rating = rating
                self.feedback_id = feedback_id
                
        feedback_data = FeedbackData(
            feedback_type=feedback_type,
            user_feedback=user_feedback,
            rating=rating,
            feedback_id=f"fb_{interaction_id}"
        )
        
        # Use asyncio background task for the pipeline
        # Running synchronous code in executor to not block event loop
        loop = asyncio.get_running_loop()
        
        # Fire and forget
        loop.run_in_executor(
            None, 
            self._process_feedback_pipeline, 
            interaction_data, 
            feedback_data
        )
        
        return True
