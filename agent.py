import asyncio
import json
import subprocess

async def main():
    proc = subprocess.Popen(
        ["python", "disk_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 1) Call get_disk_usage (Rep 1)
    request1 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "call_tool",
        "params": {
            "tool": "get_disk_usage",
            "args": {"path": "/"}
        }
    }

    proc.stdin.write(json.dumps(request1) + "\n")
    proc.stdin.flush()

    prompt = proc.stderr.readline()
    print(prompt.strip())

    proc.stdin.write("yes\n")
    proc.stdin.flush()

    response_line1 = proc.stdout.readline()
    response1 = json.loads(response_line1)
    print("Disk usage response:", response1)

    # 2) Call read_incident_log (Rep 2)
    request2 = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "call_tool",
        "params": {
            "tool": "read_incident_log",
            "args": {}
        }
    }

    proc.stdin.write(json.dumps(request2) + "\n")
    proc.stdin.flush()

    response_line2 = proc.stdout.readline()
    response2 = json.loads(response_line2)
    print("Incident log response:", response2)

asyncio.run(main())
