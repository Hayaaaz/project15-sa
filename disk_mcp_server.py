import os
import json
import shutil
import sys

def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def recv():
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)

def get_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    return {
        "path": path,
        "total": total,
        "used": used,
        "free": free
    }

def read_incident_log():
    path = os.path.join("code", "sample_incident.log")
    if not os.path.exists(path):
        return {"error": "incident log not found"}
    with open(path, "r") as f:
        return {"path": path, "content": f.read()}

def main():
    while True:
        msg = recv()
        if msg is None:
            break

        if msg.get("method") == "call_tool":
            tool = msg["params"]["tool"]
            args = msg["params"].get("args", {})

            if tool == "get_disk_usage":
                sys.stderr.write("Tool get_disk_usage requires consent. Allow? (yes/no)\n")
                sys.stderr.flush()

                consent = input().strip().lower()
                if consent != "yes":
                    send({
                        "jsonrpc": "2.0",
                        "id": msg["id"],
                        "error": "User denied consent"
                    })
                    continue

                result = get_disk_usage(args["path"])
                send({
                    "jsonrpc": "2.0",
                    "id": msg["id"],
                    "result": result
                })

            elif tool == "read_incident_log":
                # read-only tool, no write path
                result = read_incident_log()
                send({
                    "jsonrpc": "2.0",
                    "id": msg["id"],
                    "result": result
                })

        else:
            send({
                "jsonrpc": "2.0",
                "id": msg.get("id"),
                "error": "Unknown method"
            })

if __name__ == "__main__":
    main()
