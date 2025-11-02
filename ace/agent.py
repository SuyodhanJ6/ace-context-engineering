"""
ACE Agent Wrapper.

Wraps any LangChain agent or chat model with automatic ACE context injection.
"""

from typing import Any, List, Dict, Optional
from ace.playbook.manager import PlaybookManager
from ace.config import ACEConfig


class ACEAgent:
    """Wraps any LangChain agent/model with automatic ACE context injection.
    
    This wrapper transparently adds playbook context to agent calls without
    requiring users to manually inject context. It works with:
    - Chat models (init_chat_model)
    - ReAct agents (create_react_agent)
    - Custom agents
    - Any callable that accepts messages
    
    Args:
        base_agent: Any LangChain agent or chat model
        playbook_manager: PlaybookManager instance
        config: ACEConfig instance (optional, for settings)
        auto_inject: Whether to automatically inject context (default: True)
        top_k: Number of relevant bullets to retrieve (default: 10)
    
    Example:
        >>> from ace import ACEAgent, ACEConfig, PlaybookManager
        >>> from langchain.chat_models import init_chat_model
        >>> 
        >>> # Setup
        >>> config = ACEConfig(playbook_name="my_app")
        >>> playbook = PlaybookManager(
        ...     playbook_dir=config.get_storage_path(),
        ...     vector_store=config.vector_store,
        ...     embedding_model=config.embedding_model
        ... )
        >>> 
        >>> # Your agent
        >>> base_agent = init_chat_model("openai:gpt-4o-mini")
        >>> 
        >>> # Wrap with ACE
        >>> agent = ACEAgent(base_agent, playbook, config, auto_inject=True)
        >>> 
        >>> # Use normally - ACE automatically injects context!
        >>> response = agent.invoke([
        ...     {"role": "user", "content": "Process payment for order #123"}
        ... ])
        >>> 
        >>> # Get bullets used (for feedback tracking)
        >>> used_bullets = agent.get_used_bullets()
    """
    
    def __init__(
        self,
        base_agent: Any,
        playbook_manager: PlaybookManager,
        config: Optional[ACEConfig] = None,
        auto_inject: bool = True,
        top_k: int = 10,
        auto_feedback: bool = False
    ):
        """Initialize ACEAgent wrapper.
        
        Args:
            base_agent: Any LangChain agent or chat model
            playbook_manager: PlaybookManager instance
            config: ACEConfig instance (optional)
            auto_inject: Whether to automatically inject context (default: True)
            top_k: Number of relevant bullets to retrieve (default: 10)
            auto_feedback: Whether to automatically trigger feedback loop (default: False)
                          - True: Auto-critique after each response (no waiting for user feedback)
                          - False: Wait for explicit user feedback
        """
        self.base_agent = base_agent
        self.playbook = playbook_manager
        self.config = config
        self.auto_inject = auto_inject
        self.top_k = top_k if not config else config.top_k
        self.auto_feedback = auto_feedback
        self.used_bullets: List[str] = []
        self.last_interaction: Dict[str, Any] = {}  # Store last interaction for auto-feedback
        
        print(f" ACEAgent wrapper initialized")
        print(f"   Auto-inject: {self.auto_inject}")
        print(f"   Top-K: {self.top_k}")
        print(f"   Auto-feedback: {self.auto_feedback}")
    
    def invoke(self, messages: Any, **kwargs) -> Any:
        """Invoke agent with automatic context injection.
        
        Args:
            messages: Messages to send to agent (LangChain format)
            **kwargs: Additional arguments for agent
            
        Returns:
            Agent response
        """
        # Extract user query
        query = self._extract_query(messages)
        
        if self.auto_inject:
            # Get relevant bullets
            bullets = self.playbook.retrieve_relevant(query, top_k=self.top_k)
            self.used_bullets = [b.id for b in bullets]
            
            # Format context
            context = self._format_context(bullets)
            
            # Inject into system message
            messages = self._inject_context(messages, context)
        
        # Call original agent
        response = self.base_agent.invoke(messages, **kwargs)
        
        # Store interaction for potential feedback
        self.last_interaction = {
            "question": query,
            "model_response": self._extract_response_content(response),
            "used_bullets": self.used_bullets.copy()
        }
        
        # Auto-feedback mode: trigger auto-critique immediately
        if self.auto_feedback:
            self._trigger_auto_feedback()
        
        return response
    
    async def ainvoke(self, messages: Any, **kwargs) -> Any:
        """Async invoke agent with automatic context injection.
        
        Args:
            messages: Messages to send to agent (LangChain format)
            **kwargs: Additional arguments for agent
            
        Returns:
            Agent response
        """
        if self.auto_inject:
            # Extract user query from messages
            query = self._extract_query(messages)
            
            # Get relevant bullets
            bullets = self.playbook.retrieve_relevant(query, top_k=self.top_k)
            self.used_bullets = [b.id for b in bullets]
            
            # Format context
            context = self._format_context(bullets)
            
            # Inject into system message
            messages = self._inject_context(messages, context)
        
        # Call original agent (async)
        return await self.base_agent.ainvoke(messages, **kwargs)
    
    def stream(self, messages: Any, **kwargs):
        """Stream agent response with automatic context injection.
        
        Args:
            messages: Messages to send to agent (LangChain format)
            **kwargs: Additional arguments for agent
            
        Yields:
            Agent response chunks
        """
        if self.auto_inject:
            # Extract user query from messages
            query = self._extract_query(messages)
            
            # Get relevant bullets
            bullets = self.playbook.retrieve_relevant(query, top_k=self.top_k)
            self.used_bullets = [b.id for b in bullets]
            
            # Format context
            context = self._format_context(bullets)
            
            # Inject into system message
            messages = self._inject_context(messages, context)
        
        # Stream from original agent
        yield from self.base_agent.stream(messages, **kwargs)
    
    async def astream(self, messages: Any, **kwargs):
        """Async stream agent response with automatic context injection.
        
        Args:
            messages: Messages to send to agent (LangChain format)
            **kwargs: Additional arguments for agent
            
        Yields:
            Agent response chunks
        """
        if self.auto_inject:
            # Extract user query from messages
            query = self._extract_query(messages)
            
            # Get relevant bullets
            bullets = self.playbook.retrieve_relevant(query, top_k=self.top_k)
            self.used_bullets = [b.id for b in bullets]
            
            # Format context
            context = self._format_context(bullets)
            
            # Inject into system message
            messages = self._inject_context(messages, context)
        
        # Stream from original agent (async)
        async for chunk in self.base_agent.astream(messages, **kwargs):
            yield chunk
    
    def get_used_bullets(self) -> List[str]:
        """Get bullet IDs used in last call (for feedback tracking).
        
        Returns:
            List of bullet IDs that were injected into the last call
        """
        return self.used_bullets
    
    def get_last_interaction(self) -> Dict[str, Any]:
        """Get the last interaction data.
        
        Returns:
            Dictionary with question, model_response, and used_bullets
        """
        return self.last_interaction
    
    def submit_feedback(
        self,
        user_feedback: str,
        rating: int,
        feedback_type: str = "user_feedback",
        chat_data: Optional[Dict[str, Any]] = None,
        reflector: Optional[Any] = None,
        curator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Submit user feedback and trigger ACE pipeline.
        
        Args:
            user_feedback: User's feedback text
            rating: Rating from 1-5
            feedback_type: Type of feedback (default: "user_feedback")
            chat_data: Optional chat data dict with 'question', 'model_response', 'used_bullets'.
                      If not provided, uses internal last_interaction (convenience for single-user).
                      Recommended to provide explicitly for production/async/parallel users.
            reflector: Reflector instance (optional, creates one if None)
            curator: Curator instance (optional, creates one if None)
            
        Returns:
            Dictionary with processing results
        """
        # Use provided chat_data or fall back to last_interaction
        interaction_data = chat_data if chat_data is not None else self.last_interaction
        
        if not interaction_data:
            print("  No interaction to provide feedback for")
            return {"success": False, "message": "No interaction found"}
        
        print(f" Processing user feedback...")
        print(f"   Rating: {rating}/5")
        print(f"   Type: {feedback_type}")
        
        # Create feedback data object
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
            feedback_id=f"feedback_{id(interaction_data)}"
        )
        
        # Initialize Reflector and Curator if not provided
        if reflector is None:
            from ace.reflector import Reflector
            from ace.config import ACEConfig
            config = self.config or ACEConfig()
            reflector = Reflector(
                model=config.chat_model,
                storage_path=config.get_storage_path()
            )
        
        if curator is None:
            from ace.curator import Curator
            curator = Curator(
                playbook_manager=self.playbook,
                storage_path=self.config.get_storage_path() if self.config else None
            )
        
        # Run ACE pipeline
        try:
            # 1. Reflector analyzes feedback
            insight = reflector.analyze_feedback(
                chat_data=interaction_data,
                feedback_data=feedback_data
            )
            
            # 2. Curator creates delta
            delta = curator.process_insights(insight, feedback_data.feedback_id)
            
            # 3. Apply updates
            if delta.total_operations > 0:
                success = curator.merge_delta(delta)
            else:
                success = True
                print("     No updates created (low confidence)")
            
            # 4. Update bullet counters
            # Use bullet_tags from Reflector if available, otherwise fall back to rating
            used_bullets = interaction_data.get("used_bullets", [])
            
            if insight.bullet_tags:
                # Use Reflector's bullet_tags (per research paper)
                for bullet_tag in insight.bullet_tags:
                    bullet_id = bullet_tag.get("id")
                    tag = bullet_tag.get("tag", "").lower()
                    if bullet_id and tag == "helpful":
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif bullet_id and tag == "harmful":
                        self.playbook.update_counters(bullet_id, helpful=False)
            else:
                # Fallback: use rating directly (legacy behavior)
                is_positive = rating >= 4 or feedback_type == "positive"
                is_negative = rating <= 2 or feedback_type == "incorrect"
                for bullet_id in used_bullets:
                    if is_positive:
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif is_negative:
                        self.playbook.update_counters(bullet_id, helpful=False)
            
            print(f" Feedback processed successfully")
            
            return {
                "success": success,
                "insight": insight,
                "operations": delta.total_operations,
                "confidence": insight.confidence
            }
            
        except Exception as e:
            print(f" Error processing feedback: {e}")
            return {"success": False, "error": str(e)}
    
    async def asubmit_feedback(
        self,
        user_feedback: str,
        rating: int,
        feedback_type: str = "user_feedback",
        chat_data: Optional[Dict[str, Any]] = None,
        reflector: Optional[Any] = None,
        curator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Async submit user feedback and trigger ACE pipeline.
        
        Args:
            user_feedback: User's feedback text
            rating: Rating from 1-5
            feedback_type: Type of feedback (default: "user_feedback")
            chat_data: Optional chat data dict with 'question', 'model_response', 'used_bullets'.
                      If not provided, uses internal last_interaction.
                      Recommended to provide explicitly for production/async/parallel users.
            reflector: Reflector instance (optional, creates one if None)
            curator: Curator instance (optional, creates one if None)
            
        Returns:
            Dictionary with processing results
            
        Example:
            >>> # In async context (FastAPI, etc.)
            >>> result = await agent.asubmit_feedback(
            ...     user_feedback="Great response!",
            ...     rating=5,
            ...     chat_data={"question": "...", "model_response": "...", "used_bullets": [...]}
            ... )
        """
        # Use provided chat_data or fall back to last_interaction
        interaction_data = chat_data if chat_data is not None else self.last_interaction
        
        if not interaction_data:
            print("  No interaction to provide feedback for")
            return {"success": False, "message": "No interaction found"}
        
        print(f" Processing user feedback (async)...")
        print(f"   Rating: {rating}/5")
        print(f"   Type: {feedback_type}")
        
        # Create feedback data object
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
            feedback_id=f"feedback_{id(interaction_data)}"
        )
        
        # Initialize Reflector and Curator if not provided
        if reflector is None:
            from ace.reflector import Reflector
            from ace.config import ACEConfig
            config = self.config or ACEConfig()
            reflector = Reflector(
                model=config.chat_model,
                storage_path=config.get_storage_path()
            )
        
        if curator is None:
            from ace.curator import Curator
            curator = Curator(
                playbook_manager=self.playbook,
                storage_path=self.config.get_storage_path() if self.config else None
            )
        
        # Run ACE pipeline (async)
        try:
            # 1. Reflector analyzes feedback (check if it has async method)
            if hasattr(reflector.model, 'ainvoke'):
                # Use async invoke if available
                insight = await reflector.analyze_feedback(
                    chat_data=interaction_data,
                    feedback_data=feedback_data
                )
            else:
                # Fall back to sync
                insight = reflector.analyze_feedback(
                    chat_data=interaction_data,
                    feedback_data=feedback_data
                )
            
            # 2. Curator creates delta (deterministic, no async needed)
            delta = curator.process_insights(insight, feedback_data.feedback_id)
            
            # 3. Apply updates (deterministic, no async needed)
            if delta.total_operations > 0:
                success = curator.merge_delta(delta)
            else:
                success = True
                print("     No updates created (low confidence)")
            
            # 4. Update bullet counters
            used_bullets = interaction_data.get("used_bullets", [])
            
            if insight.bullet_tags:
                # Use Reflector's bullet_tags (per research paper)
                for bullet_tag in insight.bullet_tags:
                    bullet_id = bullet_tag.get("id")
                    tag = bullet_tag.get("tag", "").lower()
                    if bullet_id and tag == "helpful":
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif bullet_id and tag == "harmful":
                        self.playbook.update_counters(bullet_id, helpful=False)
            else:
                # Fallback: use rating directly (legacy behavior)
                is_positive = rating >= 4 or feedback_type == "positive"
                is_negative = rating <= 2 or feedback_type == "incorrect"
                for bullet_id in used_bullets:
                    if is_positive:
                        self.playbook.update_counters(bullet_id, helpful=True)
                    elif is_negative:
                        self.playbook.update_counters(bullet_id, helpful=False)
            
            print(f" Feedback processed successfully")
            
            return {
                "success": success,
                "insight": insight,
                "operations": delta.total_operations,
                "confidence": insight.confidence
            }
            
        except Exception as e:
            print(f" Error processing feedback: {e}")
            return {"success": False, "error": str(e)}
    
    def _trigger_auto_feedback(self):
        """Trigger automatic feedback using auto-critique."""
        if not self.last_interaction:
            return
        
        print(f"\n Auto-feedback enabled: Running auto-critique...")
        
        try:
            # Import here to avoid circular dependencies
            from ace.reflector import Reflector
            from ace.curator import Curator
            from ace.config import ACEConfig
            
            config = self.config or ACEConfig()
            reflector = Reflector(model=config.chat_model)
            curator = Curator(playbook_manager=self.playbook)
            
            # Run auto-critique (feedback_data=None triggers auto-critique)
            insight = reflector.analyze_feedback(
                chat_data=self.last_interaction,
                feedback_data=None,  # Auto-critique mode
                refine=False
            )
            
            # Only update if critique finds issues
            if insight.confidence > 0.6:
                print(f"    Auto-critique found improvement opportunity (confidence: {insight.confidence})")
                delta = curator.process_insights(insight, "auto_critique")
                
                if delta.total_operations > 0:
                    curator.merge_delta(delta)
                    print(f"    Playbook updated from auto-critique")
            else:
                print(f"    Response looks good (confidence: {insight.confidence})")
                # Mark bullets as helpful
                for bullet_id in self.last_interaction.get("used_bullets", []):
                    self.playbook.update_counters(bullet_id, helpful=True)
        
        except Exception as e:
            print(f"     Auto-feedback failed: {e}")
    
    def disable_context_injection(self):
        """Disable automatic context injection."""
        self.auto_inject = False
    
    def enable_context_injection(self):
        """Enable automatic context injection."""
        self.auto_inject = True
    
    def enable_auto_feedback(self):
        """Enable automatic feedback (auto-critique after each response)."""
        self.auto_feedback = True
        print(" Auto-feedback enabled")
    
    def disable_auto_feedback(self):
        """Disable automatic feedback (wait for manual feedback)."""
        self.auto_feedback = False
        print(" Auto-feedback disabled (manual feedback mode)")
    
    def _extract_query(self, messages: Any) -> str:
        """Extract main query from messages.
        
        Args:
            messages: Messages in various formats
            
        Returns:
            Extracted query string
        """
        # Handle different message formats
        if isinstance(messages, str):
            return messages
        
        if isinstance(messages, list):
            # Find the last user message
            for msg in reversed(messages):
                if isinstance(msg, dict):
                    if msg.get("role") == "user":
                        return msg.get("content", "")
                elif hasattr(msg, "role") and msg.role == "user":
                    return getattr(msg, "content", "")
        
        # Fallback: convert to string
        return str(messages)
    
    def _extract_response_content(self, response: Any) -> str:
        """Extract response content from agent response.
        
        Args:
            response: Agent response in various formats
            
        Returns:
            Extracted response content string
        """
        # Try to get content attribute
        if hasattr(response, "content"):
            return response.content
        
        # Try dict access
        if isinstance(response, dict) and "content" in response:
            return response["content"]
        
        # Fallback: convert to string
        return str(response)
    
    def _format_context(self, bullets: List[Any]) -> str:
        """Format bullets into context string.
        
        Args:
            bullets: List of Bullet objects
            
        Returns:
            Formatted context string
        """
        if not bullets:
            return ""
        
        context_parts = ["# ACE Playbook Context\n"]
        context_parts.append("Use the following strategies from the playbook:\n")
        
        for bullet in bullets:
            context_parts.append(bullet.to_markdown())
        
        return "\n\n".join(context_parts)
    
    def _inject_context(self, messages: Any, context: str) -> Any:
        """Inject context into system message.
        
        Args:
            messages: Original messages
            context: Context to inject
            
        Returns:
            Messages with context injected
        """
        if not context:
            return messages
        
        # Handle string messages
        if isinstance(messages, str):
            return f"{context}\n\n{messages}"
        
        # Handle list of messages
        if isinstance(messages, list):
            # Create a copy to avoid modifying original
            messages = messages.copy()
            
            # Check if first message is system
            if messages and isinstance(messages[0], dict) and messages[0].get("role") == "system":
                # Prepend to existing system message
                messages[0] = {
                    "role": "system",
                    "content": f"{context}\n\n{messages[0]['content']}"
                }
            else:
                # Insert new system message at the beginning
                messages.insert(0, {
                    "role": "system",
                    "content": context
                })
        
        return messages
    
    def __call__(self, *args, **kwargs):
        """Make ACEAgent callable like the base agent."""
        return self.invoke(*args, **kwargs)

