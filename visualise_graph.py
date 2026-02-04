#!/usr/bin/env python3
"""
Generate Knowledge Graph Visualisation

Creates an interactive HTML visualisation of the knowledge graph.
Note: The agent must be stopped before running this (Kuzu database lock).
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Apply common patches
from common_patches import apply_tiktoken_patch

apply_tiktoken_patch()

# Configure Cognee BEFORE any operations - must set data directory first
import cognee

project_cognee_dir = os.path.join(os.getcwd(), ".cognee_system")
os.makedirs(project_cognee_dir, exist_ok=True)

# Configure cognee to use project directory
cognee.config.data_root_directory(project_cognee_dir)

print(f"Using Cognee database from: {project_cognee_dir}")

import asyncio

async def visualise():
    """Generate an interactive HTML visualisation of the knowledge graph"""
    print("=" * 60)
    print("COGNEE KNOWLEDGE GRAPH VISUALISATION")
    print("=" * 60)

    output_file = "graph_visualisation.html"

    try:
        print(f"\nGenerating visualisation...")
        print(f"Output file: {output_file}")

        # Generate the visualisation
        await cognee.visualize_graph(destination_file_path=output_file)

        print(f"\n✓ Visualisation created successfully!")
        print(f"\nTo view the graph:")
        print(f"  1. Open {output_file} in your browser")
        print(f"  2. Or run: open {output_file}")
        print(f"\nThe visualisation shows:")
        print(f"  - Entities (nodes): Organisations, Industries, Contracts, etc.")
        print(f"  - Relationships (edges): IS_A, OPERATES_IN, HAS_VALUE, etc.")

    except Exception as e:
        print(f"\n✗ Error generating visualisation: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(visualise())
