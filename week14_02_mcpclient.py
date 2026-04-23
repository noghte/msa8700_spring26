import asyncio
from fastmcp import Client

client = Client("http://10.250.77.111:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("get_brand_stats", {"brand_name": name})
        print(result)

asyncio.run(call_tool("Samsung"))