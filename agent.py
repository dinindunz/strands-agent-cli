import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import shell, editor
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Apply common patches
from common_patches import apply_tiktoken_patch

apply_tiktoken_patch()

# Configure Cognee to use project directory for database storage
import cognee

# Set database location to project directory instead of Python site-packages
project_cognee_dir = os.path.join(os.getcwd(), ".cognee_system")
cognee.config.system_root_directory(project_cognee_dir)

print(f"Cognee database location: {project_cognee_dir}/databases")

from cognee_integration_langgraph import get_sessionized_cognee_tools

app = FastAPI()

# Get cognee tools (will use the configured project directory)
_cognee_add_tool, _cognee_search_tool = get_sessionized_cognee_tools()


@tool
async def add_to_knowledge_base(data: str) -> str:
    """Store information in the knowledge base for later retrieval.

    Args:
        data: The information to store in the knowledge base

    Returns:
        Confirmation message about the stored information
    """
    try:
        # LangChain tools require async invocation
        result = await _cognee_add_tool.ainvoke({"data": data})
        return f"Successfully stored information: {result}"
    except Exception as e:
        return f"Error storing information: {str(e)}"


@tool
async def search_knowledge_base(query: str) -> str:
    """Search previously stored information from the knowledge base.

    Args:
        query: The search query to find relevant information

    Returns:
        Search results from the knowledge base
    """
    try:
        # LangChain tools require async invocation
        result = await _cognee_search_tool.ainvoke({"query_text": query})
        return str(result)
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


agent = Agent(
    model=OpenAIModel(
        client_args={
            "base_url": os.getenv("LLM_ENDPOINT"),
            "api_key": os.getenv("LLM_API_KEY"),
        },
        model_id=os.getenv("LLM_MODEL").split("/")[-1],
    ),
    tools=[shell, editor, add_to_knowledge_base, search_knowledge_base],
)


class InvokeRequest(BaseModel):
    prompt: str


@app.post("/invoke")
async def invoke_agent(request: InvokeRequest):
    """Invoke the agent with a prompt"""
    try:
        result = agent(request.prompt)
        message_text = result.message.get("content", [{}])[0].get(
            "text", str(result.message)
        )

        response_data = {"result": message_text}

        return response_data
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT"))
    print(f"Starting a FastAPI agent server on 0.0.0.0:{port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
