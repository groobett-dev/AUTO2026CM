import os, urllib.request, json, ssl, subprocess

UPSTREAM_REPO = "cmliu/edgetunnel"
LOCAL_FILE = "_worker.js"
RECORD_FILE = ".last_upstream_sha"
IS_DISPATCH = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

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

# 核心安全控制：定时检测（schedule）仅在上游代码发生真实变更（upstream_sha != last_sha）时才触发部署；上游不更新则不拉取、不推送、不每天报错
has_changes = (upstream_sha != last_sha) or IS_DISPATCH

gh_output = os.environ.get("GITHUB_OUTPUT")

if has_changes:
    print("Changes detected or manual workflow dispatch! Fetching upstream _worker.js...")
    file_req = urllib.request.Request(f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/main/_worker.js", headers={
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(file_req, context=ctx, timeout=30) as res:
        raw_code = res.read().decode("utf-8")

    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(raw_code)

    # 仅对 // 注释进行中文语义转换，不混淆代码语法
    subprocess.run(["python", "scripts/transform.py", LOCAL_FILE, LOCAL_FILE], check=True)

    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        f.write(upstream_sha)

    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write("has_changes=true
")
            f.write(f"upstream_sha={upstream_sha}
")
else:
    print("============================================================")
    print("上游代码未修改（Commit 无变化），保持同步，不拉取，不推送，不向 Cloudflare 部署。")
    print("============================================================")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write("has_changes=false
")
