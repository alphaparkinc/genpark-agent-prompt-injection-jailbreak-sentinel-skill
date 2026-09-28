import sys, json
from client import AgentPromptInjectionJailbreakSentinel

def main():
    sentinel = AgentPromptInjectionJailbreakSentinel()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "scan_prompt", "description": "Scan input text for prompt injection.", "inputSchema": {"type": "object", "properties": {"user_text": {"type": "string"}}, "required": ["user_text"]}},
                        {"name": "run_benchmark_jailbreak_sentinel", "description": "Run benchmark suite.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "scan_prompt":
                    out = sentinel.scan_prompt(args.get("user_text", ""))
                elif tname == "run_benchmark_jailbreak_sentinel":
                    out = sentinel.run_benchmark_jailbreak_sentinel()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
