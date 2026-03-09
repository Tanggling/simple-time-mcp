# Simple Time MCP Server

一个极简的 MCP Server demo，用于返回当前 UTC 时间。

## MCP 服务配置

```json
{
  "mcpServers": {
    "simple-time": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/tanggling/simple-time-mcp.git", "simple-time-mcp"]
    }
  }
}
```