import os, urllib.request, json, ssl, base64, subprocess

UPSTREAM_REPO = "cmliu/edgetunnel"
LOCAL_FILE = "_worker.js"
RECORD_FILE = ".last_upstream_sha"
IS_DISPATCH = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. 检查上游最新 commit
req = urllib.request.Request(f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/main", headers={
    "User-Agent": "Mozilla/5.0"
})

with urllib.request.urlopen(req, context=ctx, timeout=20) as res:
    data = json.loads(res.read().decode("utf-8"))
    upstream_sha = data["sha"]
    commit_msg = data["commit"]["message"].splitlines()[0]

print(f"Upstream latest commit: {upstream_sha} ({commit_msg})")

last_sha = ""
if os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        last_sha = f.read().strip()

print(f"Recorded last SHA: {last_sha}")

has_changes = (upstream_sha != last_sha) or IS_DISPATCH

if has_changes:
    print("Changes detected or workflow dispatch triggered! Fetching upstream _worker.js...")
    file_req = urllib.request.Request(f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/main/_worker.js", headers={
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(file_req, context=ctx, timeout=30) as res:
        raw_code = res.read().decode("utf-8")

    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(raw_code)

    # 执行转换脚本
    subprocess.run(["python", "scripts/transform.py", LOCAL_FILE, LOCAL_FILE], check=True)

    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        f.write(upstream_sha)

    # 输出给 GitHub Actions
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write("has_changes=true
")
        f.write(f"upstream_sha={upstream_sha}
")
else:
    print("No upstream changes. Upstream is in sync.")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write("has_changes=false
")
