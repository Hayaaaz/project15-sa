import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "local-ops-server": {
                "type": "stdio",
                "command": "python",
                "args": ["disk_mcp_server.py"],
            }
        },
        allowed_tools=["mcp__local-ops-server__*"],
    )

    async for message in query(
        prompt="what's disk usage on / ?",
        options=options,
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
