#!/usr/bin/env python3
"""
Visualize the Cognee knowledge graph.

This script generates an interactive HTML visualization of the knowledge graph
showing entities and their relationships.
"""

import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Monkey-patch tiktoken
import tiktoken
_original_encoding_for_model = tiktoken.encoding_for_model

def patched_encoding_for_model(model_name: str):
    model_mappings = {
        "au-text-embedding-3-small": "text-embedding-3-small",
        "au-text-embedding-3-large": "text-embedding-3-large",
        "openai/au-text-embedding-3-small": "text-embedding-3-small",
        "openai/au-text-embedding-3-large": "text-embedding-3-large",
    }
    mapped_model = model_mappings.get(model_name, model_name)
    return _original_encoding_for_model(mapped_model)

tiktoken.encoding_for_model = patched_encoding_for_model

# Configure Cognee to use project directory (same as agent.py)
import cognee
project_cognee_dir = os.path.join(os.getcwd(), ".cognee_system")
cognee.config.system_root_directory(project_cognee_dir)

async def visualize():
    """Generate an interactive HTML visualization of the knowledge graph"""
    print("=" * 60)
    print("COGNEE KNOWLEDGE GRAPH VISUALIZATION")
    print("=" * 60)

    output_file = "graph_visualization.html"

    try:
        print(f"\nGenerating visualization...")
        print(f"Output file: {output_file}")

        # Generate the visualization
        await cognee.visualize_graph(destination_file_path=output_file)

        print(f"\n✓ Visualization created successfully!")
        print(f"\nTo view the graph:")
        print(f"  1. Open {output_file} in your browser")
        print(f"  2. Or run: open {output_file}")
        print(f"\nThe visualization shows:")
        print(f"  - Entities (nodes): Organizations, Industries, Contracts, etc.")
        print(f"  - Relationships (edges): IS_A, OPERATES_IN, HAS_VALUE, etc.")

    except Exception as e:
        print(f"\n✗ Error generating visualization: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(visualize())
