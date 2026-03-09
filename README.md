# Simple Time MCP Demo

极简 MCP Server，返回当前 UTC 时间。

## MCP 服务配置

```json
{
  "mcpServers": {
    "simple-time": {
      "command": "uvx",
      "args": ["simple-time-mcp@latest"]
    }
  }
}