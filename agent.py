import os
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import shell,  editor
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Set environment variables to bypass tool approval prompts
os.environ["STRANDS_NON_INTERACTIVE"] = "true"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

app = FastAPI()

agent = Agent(
    model=BedrockModel(
        model_id="apac.anthropic.claude-sonnet-4-20250514-v1:0",
    ),
    tools=[shell, editor],
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

        response_data = {"result": message_text }

        return response_data
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    print(
        f"Starting a FastAPI agent server on 0.0.0.0:8888..."
    )
    uvicorn.run(app, host="0.0.0.0", port=8888)
