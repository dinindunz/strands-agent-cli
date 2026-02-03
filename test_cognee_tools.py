#!/usr/bin/env python3
"""Test script to debug cognee tools integration"""

import asyncio
from cognee_integration_langgraph import get_sessionized_cognee_tools

async def test_tools():
    print("Getting cognee tools...")
    add_tool, search_tool = get_sessionized_cognee_tools()

    print(f"\nAdd tool type: {type(add_tool)}")
    print(f"Add tool name: {add_tool.name if hasattr(add_tool, 'name') else 'N/A'}")
    print(f"Add tool: {add_tool}")

    print(f"\nSearch tool type: {type(search_tool)}")
    print(f"Search tool name: {search_tool.name if hasattr(search_tool, 'name') else 'N/A'}")

    # Test add tool
    print("\n" + "="*50)
    print("Testing add_tool...")
    print("="*50)

    try:
        # Try different invocation methods
        test_data = "Test information: Company ABC, Value $100k"

        print(f"\nMethod 1: .invoke() with dict")
        try:
            result = add_tool.invoke({"data": test_data})
            print(f"Success: {result}")
        except Exception as e:
            print(f"Failed: {type(e).__name__}: {e}")

        print(f"\nMethod 2: .invoke() with string directly")
        try:
            result = add_tool.invoke(test_data)
            print(f"Success: {result}")
        except Exception as e:
            print(f"Failed: {type(e).__name__}: {e}")

        print(f"\nMethod 3: ainvoke() with dict (async)")
        try:
            result = await add_tool.ainvoke({"data": test_data})
            print(f"Success: {result}")
        except Exception as e:
            print(f"Failed: {type(e).__name__}: {e}")

        print(f"\nMethod 4: ainvoke() with string directly (async)")
        try:
            result = await add_tool.ainvoke(test_data)
            print(f"Success: {result}")
        except Exception as e:
            print(f"Failed: {type(e).__name__}: {e}")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tools())
