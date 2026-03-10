import json
import sys
import time

def list_tools():
    return [{
        "name": "get_current_time",
        "description": "获取当前服务器时间（UTC）",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }]

def call_tool(name, arguments):
    if name == "get_current_time":
        result_text = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        return {
            "content": [{"type": "text", "text": result_text}],
            "isError": False
        }
    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
            "isError": True
        }

def main():
    # 强制使用 utf-8 输出，避免编码问题
    sys.stdout.reconfigure(encoding='utf-8')
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id", 0)
            resp = {
                "jsonrpc": "2.0",
                "id": req_id
            }
            
            method = req.get("method")
            if method == "tools/list":
                resp["result"] = {"tools": list_tools()}
            
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                if not tool_name:
                    resp["result"] = {
                        "content": [{"type": "text", "text": "Missing tool name"}],
                        "isError": True
                    }
                else:
                    resp["result"] = call_tool(tool_name, tool_args)
            
            else:
                resp["error"] = {"code": -32601, "message": "Method not found"}
            
            # 输出最紧凑的 JSON（无空格、无转义、无多余换行）
            print(json.dumps(resp, ensure_ascii=False, separators=(',', ':')))
            sys.stdout.flush()
        
        except json.JSONDecodeError:
            # JSON 解析失败时返回标准错误
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32700, "message": "Parse error"}
            }, separators=(',', ':')))
            sys.stdout.flush()
        
        except Exception:
            # 其他异常统一返回 Internal error
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32000, "message": "Internal server error"}
            }, separators=(',', ':')))
            sys.stdout.flush()

if __name__ == "__main__":
    main()