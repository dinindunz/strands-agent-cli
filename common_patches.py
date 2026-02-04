"""
Common patches and configurations for Cognee integration.
"""

import tiktoken

# Store original function
_original_encoding_for_model = tiktoken.encoding_for_model


def apply_tiktoken_patch():
    """
    Patch tiktoken to recognise custom model names from custom gateways.

    Maps custom model names (e.g., au-text-embedding-3-large) to standard
    OpenAI model names that tiktoken recognises.
    """

    def patched_encoding_for_model(model_name: str):
        model_mappings = {
            "au-text-embedding-3-large": "text-embedding-3-large",
            "openai/au-text-embedding-3-large": "text-embedding-3-large",
        }
        mapped_model = model_mappings.get(model_name, model_name)
        return _original_encoding_for_model(mapped_model)

    tiktoken.encoding_for_model = patched_encoding_for_model
