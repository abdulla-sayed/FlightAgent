import asyncio
from datetime import date

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

model = OllamaModel(
    "qwen3:8b", provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

toolset = MCPToolset(
    StdioTransport(command="flightagent-mcp", args=[], keep_alive=False)
)

agent = Agent(
    model,
    toolsets=[toolset],
    model_settings={"temperature": 0},
    instructions="You are a flight assistant. Always use the provided tools to answer; never describe a tool call in text.",
)


@agent.instructions
def inject_current_date() -> str:
    today = date.today().strftime("%A, %B %d, %Y")
    return f"Today's date is {today}. Use this if needed."


async def main():
    async with agent:
        result = await agent.run(
            "What is the nearest upcoming flight from Dubai to LHR? and render it as well please."
        )
        print(result.output)


asyncio.run(main())
