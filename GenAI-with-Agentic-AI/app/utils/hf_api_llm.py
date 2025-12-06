"""
hf_api_llm.py
-------------
HuggingFace Inference API LLM - uses serverless API instead of local models.
Much faster, no downloads needed!
"""

import os
from openai import OpenAI
from typing import Optional


class HuggingFaceAPILLM:
    """
    LLM wrapper using HuggingFace Inference API (serverless).
    Compatible with OpenAI client interface.
    """
    
    def __init__(self, model_name: str = "meta-llama/Llama-3.2-3B-Instruct:novita", **kwargs):
        """
        Initialize HuggingFace API LLM.
        
        Args:
            model_name: Model to use from HF Hub
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
        """
        self.model_name = model_name
        self.kwargs = kwargs
        
        # Get HF token
        hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        
        if not hf_token:
            raise ValueError("HF_TOKEN or HUGGINGFACE_TOKEN environment variable is required")
        
        # Initialize OpenAI client with HuggingFace endpoint
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        
        print(f"✅ HuggingFace API LLM initialized with {model_name}")
    
    def invoke(self, prompt: str) -> str:
        """
        Generate text using HuggingFace API.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        try:
            # Handle PromptValue objects from LangChain
            if hasattr(prompt, 'text'):
                prompt_text = prompt.text
            elif hasattr(prompt, 'to_string'):
                prompt_text = prompt.to_string()
            elif isinstance(prompt, str):
                prompt_text = prompt
            else:
                prompt_text = str(prompt)
            
            # Call HuggingFace API
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                max_tokens=self.kwargs.get('max_tokens', 256),
                temperature=self.kwargs.get('temperature', 0.7),
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️ HuggingFace API error: {e}")
            return ""
    
    def __call__(self, prompt: str) -> str:
        """Direct call interface"""
        return self.invoke(prompt)
    
    def run(self, prompt: str) -> str:
        """Legacy interface"""
        return self.invoke(prompt)
    
    def predict(self, text: str) -> str:
        """Alternative interface"""
        return self.invoke(text)
