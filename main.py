import json
import sys
import time

def list_tools():
    return [{
        "name": "get_current_time",
        "description": "获取当前服务器时间（UTC）",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }]

def call_tool(name, arguments):
    if name == "get_current_time":
        return {"result": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}
    return {"error": "Unknown tool"}

if __name__ == "__main__":
    # 强制 utf-8 输出，避免编码问题
    sys.stdout.reconfigure(encoding='utf-8')
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id", 0)
            }
            
            method = req.get("method")
            if method == "tools/list":
                resp["result"] = {"tools": list_tools()}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                resp["result"] = call_tool(name, args)
            else:
                resp["error"] = {"code": -32601, "message": "Method not found"}
            
            # 压缩输出：无空格、无换行、无转义
            print(json.dumps(resp, ensure_ascii=False, separators=(',', ':')))
            sys.stdout.flush()
        
        except Exception:
            # 异常时只输出最小 error，不打印 traceback
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32000, "message": "Internal error"}
            }, separators=(',', ':')))
            sys.stdout.flush()