import argparse
import asyncio
from typing import Any

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


def format_content_items(items: list[Any]) -> list[str]:
    formatted: list[str] = []
    for item in items:
        text = getattr(item, "text", None)
        if text is not None:
            formatted.append(text)
        else:
            formatted.append(repr(item))
    return formatted


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/sse")
    args = parser.parse_args()

    async with sse_client(args.url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init_result = await session.initialize()
            print(f"Connected to server: {init_result.serverInfo.name}")

            tools_result = await session.list_tools()
            print("Tools:", ", ".join(str(tool.name) for tool in tools_result.tools))

            resources_result = await session.list_resources()
            print("Resources:", ", ".join(str(resource.uri) for resource in resources_result.resources))

            ping_result = await session.call_tool("ping")
            print("ping ->", format_content_items(ping_result.content))

            add_result = await session.call_tool("add", {"a": 2, "b": 3})
            print("add(2, 3) ->", format_content_items(add_result.content))

            resource_result = await session.read_resource("info://server")
            for content in resource_result.contents:
                text = getattr(content, "text", None)
                if text is not None:
                    print("info://server ->")
                    print(text)


if __name__ == "__main__":
    asyncio.run(main())
