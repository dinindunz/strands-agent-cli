#!/usr/bin/env python3
"""
Real-time Knowledge Graph Visualization Server

Runs a live visualization server that shows the knowledge graph in real-time.
Can run alongside the agent without database locks.
"""

import os
from dotenv import load_dotenv
import signal
import sys

# Load environment variables
load_dotenv()

# Apply common patches
from common_patches import apply_tiktoken_patch

apply_tiktoken_patch()

# Configure Cognee to use project directory (same as agent.py)
import cognee
from cognee.api.v1.visualize.start_visualization_server import visualization_server

project_cognee_dir = os.path.join(os.getcwd(), ".cognee_system")
cognee.config.system_root_directory(project_cognee_dir)

# Get server configuration from environment
graph_port = int(os.getenv("GRAPH_PORT"))

print("=" * 60)
print("COGNEE REAL-TIME GRAPH VISUALIZATION SERVER")
print("=" * 60)
print(f"\nDatabase: {project_cognee_dir}/databases")
print(f"Starting visualization server on http://localhost:{graph_port}")
print("\nThe graph will update automatically as your agent adds new data!")
print("\nPress Ctrl+C to stop the server")
print("=" * 60)

# Start the visualization server
shutdown_fn = visualization_server(port=graph_port)


# Handle graceful shutdown
def signal_handler(sig, frame):
    print("\n\nShutting down visualization server...")
    if shutdown_fn:
        shutdown_fn()
    print("Server stopped.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Keep the server running
try:
    signal.pause()
except AttributeError:
    # Windows doesn't have signal.pause(), so use an alternative
    import time

    while True:
        time.sleep(1)
