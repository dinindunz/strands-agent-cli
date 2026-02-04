#!/usr/bin/env python3
"""
Real-time Knowledge Graph Visualisation Server

Serves the knowledge graph visualisation HTML file.
"""

import os
from dotenv import load_dotenv
import http.server
import socketserver

# Load environment variables
load_dotenv()

# Get server configuration from environment
graph_port = int(os.getenv("GRAPH_PORT", "8080"))

print("=" * 60)
print("COGNEE GRAPH VISUALISATION SERVER")
print("=" * 60)
print(f"\nServing visualisation on http://localhost:{graph_port}/graph_visualisation.html")
print("\nMake sure to generate the graph first by running:")
print("  python visualise_graph.py")
print("\nPress Ctrl+C to stop the server")
print("=" * 60)

# Simple HTTP server to serve the visualisation HTML
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", graph_port), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down visualisation server...")
        print("Server stopped.")
