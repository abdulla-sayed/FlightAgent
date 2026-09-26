import asyncio
import os
from datetime import date
from pathlib import Path

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

os.environ["PYDANTIC_AI_NO_BANNER"] = "1"

model = OllamaModel(
    "qwen3:8b", provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

toolset = MCPToolset(
    StdioTransport(command="flightagent-mcp", args=[], keep_alive=False)
)


prompt_path = Path(__file__).resolve().parent / "prompts" / "system.md"
prompt_text = prompt_path.read_text(encoding="utf-8")

agent = Agent(
    model,
    toolsets=[toolset],
    model_settings={"temperature": 0},
    instructions=prompt_text,
)


@agent.instructions
def inject_current_date() -> str:
    today = date.today().strftime("%A, %B %d, %Y")
    return f"Today's date is {today}. Use this if needed."


user_input = ""


async def main():
    chat_history = []

    async with agent:
        while True:
            try:
                user_input = input("You: ").strip()

            except (KeyboardInterrupt, EOFError):
                print("Terminating...")
                break

            if not user_input:
                continue
            result = await agent.run(user_input, message_history=chat_history)
            chat_history = result.all_messages()
            print(f"Agent: {result.output}")


asyncio.run(main())
