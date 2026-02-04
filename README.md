# Cognee POC - Agent with Knowledge Graph Memory

An AI agent powered by Strands with persistent memory using Cognee's knowledge graph capabilities.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure. Set your LLM and Embedding provider details.

## Usage

### Start the Agent Server

```bash
python agent.py
```

The server will start on `http://localhost:8888`

### Test with Chat Client

```bash
python chat_client.py
```

**Example - Store Information**:
```
You: Contract signed with Acme Corp - Industry: Healthcare, Contract Value: $1.2M
Agent: [Stores the information in the knowledge graph]
```

**Example - Retrieve Information**:
```
You: What healthcare contracts do we have?
Agent: [Searches the knowledge graph and returns relevant contracts]
```

### Visualising the Knowledge Graph

Run visualisation server to view the graph:

```bash
# The agent must be stopped before running this (Kuzu database lock)
python visualise_graph.py

# Start the graph visualisation server
python graph_server.py

# Open in browser
# Visit: http://localhost:8889/graph_visualisation.html
```

## Knowledge Graph

Cognee automatically extracts entities and relationships from stored information:

**Example Input**:
```
"Acme Corp signed a $1.2M healthcare contract"
```

**Extracted Entities**:
- Organisation: "Acme Corp"
- Industry: "Healthcare"
- Contract: "Acme Corp contract"
- Status: "Signed"
- MonetaryValue: "$1.2M"

**Relationships**:
- Acme Corp � IS_A � Organisation
- Acme Corp � OPERATES_IN � Healthcare
- Contract � HAS_VALUE � $1.2M
- Contract � HAS_STATUS � Signed

### What the Visualisation Shows

- **Nodes**: Entities (Organisations, Industries, Contracts, Monetary Values, etc.)
- **Edges**: Relationships (IS_A, OPERATES_IN, HAS_VALUE, HAS_STATUS, etc.)
- **Interactive**: Click and drag nodes, zoom in/out to explore connections

## Database Storage

Cognee stores the knowledge graph database in your project directory:

```
.cognee_system/
└── databases/
    ├── cognee_db              # Relational database (SQLite)
    ├── cognee_graph_kuzu      # Knowledge graph (Kuzu)
    ├── cognee_graph_kuzu.wal  # Write-ahead log
    └── cognee.lancedb/        # Vector embeddings (LanceDB)
```

**Database Location**: `.cognee_system/databases/`

**Persistence**: The database persists across agent restarts. All stored knowledge remains available unless you delete the `.cognee_system` directory.

**Testing Persistence**: Run `python test_cognee_persistence.py` to verify the database connection and check what data is stored.

## License

MIT
