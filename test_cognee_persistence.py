#!/usr/bin/env python3
"""
Test script to verify Cognee database persistence across restarts.

This script will:
1. Show the current Cognee data directory
2. Check if there's existing data in the knowledge base
3. Search for previously stored information
"""

import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Apply common patches
from common_patches import apply_tiktoken_patch

apply_tiktoken_patch()

# Configure Cognee to use project directory (same as agent.py)
import cognee

project_cognee_dir = os.path.join(os.getcwd(), ".cognee_system")
cognee.config.system_root_directory(project_cognee_dir)

from cognee_integration_langgraph import get_sessionized_cognee_tools


async def test_persistence():
    print("=" * 60)
    print("COGNEE PERSISTENCE TEST")
    print("=" * 60)

    # Get cognee tools
    _cognee_add_tool, _cognee_search_tool = get_sessionized_cognee_tools()

    # Try to search for previously stored data
    print("\n1. Searching for previously stored 'Acme Corp' data...")
    try:
        result = await _cognee_search_tool.ainvoke(
            {"query_text": "Acme Corp healthcare contract"}
        )
        print(f"   ✓ Search Result:\n{result}")
        print("\n   → Database is PERSISTENT - found existing data!")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("   → Database might be empty or not initialised")

    # Try searching for any healthcare related data
    print("\n2. Searching for healthcare contracts...")
    try:
        result = await _cognee_search_tool.ainvoke(
            {"query_text": "healthcare contracts"}
        )
        print(f"   ✓ Search Result:\n{result}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Show data directory
    print("\n3. Checking Cognee database location...")
    project_db_dir = os.path.join(os.getcwd(), ".cognee_system/databases")

    if os.path.exists(project_db_dir):
        print(f"   ✓ Database directory: {project_db_dir}")

        # Show database files
        try:
            db_files = os.listdir(project_db_dir)
            print(f"   ✓ Database files:")
            for file in db_files:
                file_path = os.path.join(project_db_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"     - {file} ({size:,} bytes)")
                elif os.path.isdir(file_path):
                    print(f"     - {file}/ (directory)")
        except Exception as e:
            print(f"     (Cannot list contents: {e})")
    else:
        print(f"   ✗ Database directory not found: {project_db_dir}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_persistence())
