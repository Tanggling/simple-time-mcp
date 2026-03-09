# main.py
import json
import sys
import time
from typing import Dict, Any

def list_tools() -> list:
    return [
        {
            "name": "get_current_time",
            "description": "获取当前服务器时间（UTC）",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        }
    ]

def call_tool(name: str, arguments: Dict[str, Any]) -> Dict:
    if name == "get_current_time":
        return {"result": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}
    return {"error": "Unknown tool"}

def main():
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
            if req.get("type") == "list_tools":
                print(json.dumps({"tools": list_tools()}))
            elif req.get("type") == "call_tool":
                result = call_tool(req["name"], req.get("arguments", {}))
                print(json.dumps({"result": result}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()   # 保持兼容直接 python main.py