"""
local_llm.py
------------
Local LLM using HuggingFace transformers pipeline.
Supports both Flan-T5 and Llama models.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import Optional
import os

# Singleton to avoid reloading models
_llm_pipeline = None
_model_name = None
_is_llama = False


def get_local_llm(model_name: Optional[str] = None):
    """
    Returns a local HuggingFace pipeline for text generation.
    Model is downloaded once and cached locally.
    
    Args:
        model_name: Model to use (default: flan-t5-base for speed)
    
    Returns:
        Pipeline that can be called like: llm("question")
    """
    global _llm_pipeline, _model_name, _is_llama
    
    # Check if model changed - force reload
    if model_name and model_name != _model_name:
        print(f"🔄 Model change: {_model_name} -> {model_name}")
        _llm_pipeline = None
        _model_name = model_name
    elif model_name:
        _model_name = model_name
    
    # Set default if no model specified
    if not _model_name:
        _model_name = "google/flan-t5-base"
    
    if _llm_pipeline is None:
        print(f"🔄 Loading local model: {_model_name} (first time may download ~3GB)...")
        
        # Check if it's a Llama model
        _is_llama = "llama" in _model_name.lower()
        
        # Get HuggingFace token if available
        hf_token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
        
        if _is_llama:
            # Use text-generation for Llama models with better parameters
            _llm_pipeline = pipeline(
                "text-generation",
                model=_model_name,
                max_new_tokens=512,  # Allow longer responses
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,  # Prevent repetition
                device=-1,  # CPU (use 0 for GPU)
                token=hf_token,
                pad_token_id=50256  # Set pad token
            )
        else:
            # Use text2text-generation for Flan-T5 models
            _llm_pipeline = pipeline(
                "text2text-generation",
                model=_model_name,
                max_length=512,
                do_sample=False,
                device=-1,
                token=hf_token
            )
        
        print(f"✅ Model loaded successfully!")
    
    return _llm_pipeline


class LocalLLM:
    """
    LangChain-compatible wrapper for local HuggingFace pipeline.
    Can be used as drop-in replacement for HuggingFaceHub.
    """
    
    def __init__(self, model_name: str = "google/flan-t5-base", **kwargs):
        self.model_name = model_name
        self.pipeline = get_local_llm(model_name)
        self.kwargs = kwargs
    
    def __call__(self, prompt) -> str:
        """Direct call interface"""
        return self.invoke(prompt)
    
    def invoke(self, prompt) -> str:
        """LangChain 1.x invoke interface"""
        # Handle PromptValue objects from LangChain prompts
        if hasattr(prompt, 'text'):
            prompt_text = prompt.text
        elif hasattr(prompt, 'to_string'):
            prompt_text = prompt.to_string()
        elif isinstance(prompt, str):
            prompt_text = prompt
        else:
            prompt_text = str(prompt)
        
        # Check if using Llama model
        global _is_llama
        
        if _is_llama:
            # For Llama models, extract only the generated text (not the prompt)
            result = self.pipeline(
                prompt_text, 
                max_new_tokens=self.kwargs.get('max_length', 512),
                return_full_text=False,
                truncation=True
            )
            if result and len(result) > 0:
                generated = result[0]['generated_text'].strip()
                # Clean up Llama special tokens that might leak through
                generated = generated.replace('<|eot_id|>', '').replace('<|end_header_id|>', '').strip()
            else:
                generated = ""
        else:
            # For Flan-T5 models
            result = self.pipeline(prompt_text, max_length=self.kwargs.get('max_length', 512))
            generated = result[0]['generated_text'].strip() if result else ""
        
        return generated
    
    def run(self, prompt: str) -> str:
        """Legacy run interface (deprecated but still works)"""
        return self.invoke(prompt)
    
    def predict(self, text: str) -> str:
        """Alternative interface"""
        return self.invoke(text)
