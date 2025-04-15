from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
import httpx


# Initialize FastMCP server for Weather tools (SSE)
mcp = FastMCP("weibo_resou")

@mcp.tool()
async def hot_search(n: int = 20) -> str:
    """Get the top N Weibo hot searches (trending topics).

    Args:
        n (int, optional): The number of top hot searches to retrieve. Defaults to 20 if not specified.
    """

    url = 'https://weibo.com/ajax/side/hotSearch'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10)
            # 抛出 HTTPError 以处理非 200 状态码
            response.raise_for_status()
            data = response.json().get('data')
            if not data or not data.get('realtime'):
                return "未能成功获取微博热搜数据。"

            hostsearch = ""
            for i, rs in enumerate(data['realtime'][:n], 1):

                title = rs.get('word', '')
                label = rs.get('label_name', '')

                if label not in ['新', '爆', '沸']:
                    label = ''

                hostsearch += f"{i}. {title} {f'（{label}）' if label else ''}\n"

            # 移除末尾多余的换行符
            return hostsearch.strip()

        except httpx.HTTPError as e:
            return f"HTTP 请求错误: {e}"
        except httpx.TimeoutException:
            return "请求超时。"
        except Exception as e:
            return f"发生未知错误: {e}"


if __name__ == "__main__":
    # initialize and run the server
    mcp.run(transport='stdio')