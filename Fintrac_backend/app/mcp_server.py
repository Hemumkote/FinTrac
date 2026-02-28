from mcp.server.fastmcp import FastMCP
from services.category_service import CategoryService
from app.db.session import get_async_context


# Initialize FastMCP
mcp = FastMCP("FinTrac_MCP")


@mcp.tool()
async def get_categories() -> str:
    """get all predefined categories"""
    async with get_async_context() as session:
        service = CategoryService(session)
        categories = await service.get_categories()
        return str([cat.model_dump() for cat in categories])


# 1. Claude (or MCP Inspector) calls the "get_categories" tool
#           ↓
# 2. FastMCP routes the call to your get_categories() function
#           ↓
# 3. get_async_context() opens a new AsyncSession from your session factory
#           ↓
# 4. CategoryService(session) — same service your routes use
#           ↓
# 5. service.get_categories() — queries the DB, returns Pydantic models
#           ↓
# 6. Convert to string (MCP tools return strings)
#           ↓
# 7. Session auto-commits and closes (handled by get_async_context)
#           ↓
# 8. Result goes back to the MCP client


# Example Resource
@mcp.resource("config://app-settings")
def get_config() -> str:
    """Get app configuration metadata."""
    return '{"theme": "dark", "version": "1.0.0"}'
