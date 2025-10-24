"""
ModelFallbackMiddleware - Automatic model failover for ACE Framework.
"""

from typing import List, Optional, Any, Dict
import logging
from dataclasses import dataclass

from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)


@dataclass
class FallbackConfig:
    """Configuration for model fallback."""
    primary_model: str
    fallback_models: List[str]
    max_retries: int = 3
    timeout: int = 30


class ModelFallbackMiddleware:
    """
    Middleware for automatic model fallover in ACE Framework.
    
    Provides robust error handling and automatic failover to backup models
    when the primary model fails or is unavailable.
    """
    
    def __init__(
        self,
        primary_model: str,
        fallback_models: List[str],
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the fallback middleware.
        
        Args:
            primary_model: Primary model identifier
            fallback_models: List of fallback model identifiers
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
        """
        self.config = FallbackConfig(
            primary_model=primary_model,
            fallback_models=fallback_models,
            max_retries=max_retries,
            timeout=timeout
        )
        
        # Create model instances
        self.models = self._create_models()
        self.current_model = self.models[0]  # Start with primary
        
        logger.info(f"ModelFallbackMiddleware initialized with {len(self.models)} models")
    
    def _create_models(self) -> List[BaseLanguageModel]:
        """Create model instances for all configured models."""
        models = []
        all_models = [self.config.primary_model] + self.config.fallback_models
        
        for model_name in all_models:
            try:
                model = self._create_model(model_name)
                models.append(model)
                logger.info(f"Created model: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to create model {model_name}: {e}")
                continue
        
        if not models:
            raise RuntimeError("No working models available!")
        
        return models
    
    def _create_model(self, model_name: str) -> BaseLanguageModel:
        """Create a single model instance."""
        if model_name.startswith("openai:"):
            model_id = model_name.split(":", 1)[1]
            return ChatOpenAI(
                model=model_id,
                timeout=self.config.timeout
            )
        elif model_name.startswith("anthropic:"):
            model_id = model_name.split(":", 1)[1]
            return ChatAnthropic(
                model=model_id,
                timeout=self.config.timeout
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    
    def invoke_with_fallback(
        self,
        messages: List[Any],
        **kwargs
    ) -> Any:
        """
        Invoke model with automatic fallback.
        
        Args:
            messages: Input messages
            **kwargs: Additional model parameters
            
        Returns:
            Model response
            
        Raises:
            RuntimeError: If all models fail
        """
        last_error = None
        
        for attempt in range(self.config.max_retries):
            for i, model in enumerate(self.models):
                try:
                    logger.info(f"Attempting model {i+1}/{len(self.models)} (attempt {attempt+1})")
                    response = model.invoke(messages, **kwargs)
                    
                    # Update current model if successful
                    self.current_model = model
                    logger.info(f"Model {i+1} succeeded")
                    return response
                    
                except Exception as e:
                    logger.warning(f"Model {i+1} failed: {e}")
                    last_error = e
                    continue
        
        # All models failed
        logger.error("All models failed!")
        raise RuntimeError(f"All models failed. Last error: {last_error}")
    
    def get_working_model(self) -> BaseLanguageModel:
        """
        Get a working model (tries all models until one works).
        
        Returns:
            Working model instance
            
        Raises:
            RuntimeError: If no models are working
        """
        for model in self.models:
            try:
                # Test the model with a simple request
                test_messages = [{"role": "user", "content": "Hello"}]
                model.invoke(test_messages)
                logger.info("Found working model")
                return model
            except Exception as e:
                logger.warning(f"Model test failed: {e}")
                continue
        
        raise RuntimeError("No working models available!")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about configured models."""
        return {
            "total_models": len(self.models),
            "primary_model": self.config.primary_model,
            "fallback_models": self.config.fallback_models,
            "current_model": str(self.current_model),
            "max_retries": self.config.max_retries,
            "timeout": self.config.timeout
        }
    
    def test_all_models(self) -> Dict[str, bool]:
        """
        Test all configured models.
        
        Returns:
            Dictionary mapping model names to availability status
        """
        results = {}
        all_models = [self.config.primary_model] + self.config.fallback_models
        
        for i, model_name in enumerate(all_models):
            try:
                model = self.models[i]
                test_messages = [{"role": "user", "content": "Test"}]
                model.invoke(test_messages)
                results[model_name] = True
                logger.info(f"Model {model_name}:  Working")
            except Exception as e:
                results[model_name] = False
                logger.warning(f"Model {model_name}:  Failed - {e}")
        
        return results
