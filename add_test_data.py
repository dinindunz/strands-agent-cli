#!/usr/bin/env python3
"""Add test data to the knowledge graph"""

import requests
import json

url = "http://localhost:8888/invoke"

# Test data to add
test_data = "Please store this information in the knowledge base: Contract signed with Acme Corp - Industry: Healthcare, Contract Value: $1.2M"

print("Sending test data to agent...")
response = requests.post(url, json={"prompt": test_data})

if response.status_code == 200:
    result = response.json()
    print("\n✓ Response from agent:")
    print(json.dumps(result, indent=2))
else:
    print(f"\n✗ Error: {response.status_code}")
    print(response.text)
