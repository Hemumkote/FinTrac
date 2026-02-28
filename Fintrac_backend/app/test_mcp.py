import asyncio
import os
from mcp import ClientSession
from mcp.client.sse import sse_client

# Use port 8000 inside Docker, 8009 from host machine
MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/mcp/sse")

async def main():
    print(f"Connecting to MCP server at {MCP_URL}...")

    async with sse_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. List available tools
            tools = await session.list_tools()
            print(f"\n✅ Connected! Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f" - {tool.name}: {tool.description}")

            # 2. Call the 'get_categories' tool
            print("\n🔨 Calling 'get_categories'...")
            try:
                result = await session.call_tool("get_categories")
                
                # The result content is a list of TextContent or ImageContent
                # We expect text containing the JSON string of categories
                if result.content:
                    print("Response received:")
                    print(result.content[0].text[:200] + "...") # Print first 200 chars
                else:
                    print("Empty response.")
            except Exception as e:
                print(f"❌ Error calling tool: {e}")

            # 3. Read the 'config://app-settings' resource
            print("\n📄 Reading resource 'config://app-settings'...")
            try:
                resource = await session.read_resource("config://app-settings")
                print(f"Resource content: {resource.contents[0].text}")
            except Exception as e:
                print(f"❌ Error reading resource: {e}")

if __name__ == "__main__":
    asyncio.run(main())
