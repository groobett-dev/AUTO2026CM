import sys, re

# 中文注释词库映射表（覆盖 Cloudflare Worker / edgetunnel 核心注释短语）
COMMENT_DICT = {
    "set default values if not provided": "设置默认全局变量（若未提供环境配置）",
    "check if user is authenticated": "校验访问用户令牌与身份鉴权",
    "return unauthorized response": "返回未授权访问状态与重定向",
    "fallback proxy ip": "兜底中继代理 IP 地址端点",
    "error handling": "边缘网络请求异常捕获与容错处理",
    "handle websocket": "处理边缘 WebSocket 双向数据流隧道",
    "parse request": "解析客户端入站 HTTP 请求头与路径参数",
    "generate response": "构建并返回边缘响应数据流",
    "connect to remote": "建立与远端目标主机的 TCP 握手与连接",
    "proxy ip": "中继代理网络出口 IP",
    "sub info": "订阅节点元数据与流量状态信息",
    "clean up": "清理并释放套接字与内存资源",
    "listen for incoming": "监听入站流量与会话通道",
    "read header": "读取并解析二进制数据流首部",
    "write data": "向目标套接字写入载荷数据",
    "close connection": "安全关闭边缘网络连接会话",
    "validate token": "校验安全令牌与签名哈希",
    "dynamic configuration": "从边缘 KV 空间加载动态配置参数"
}

def translate_comment(comment_body: str) -> str:
    stripped = comment_body.strip()
    lower = stripped.lower()
    for en_phrase, zh_text in COMMENT_DICT.items():
        if en_phrase in lower:
            return " " + zh_text
    # 若本身已包含中文，保持原样
    if any("一" <= ch <= "鿿" for ch in stripped):
        return " " + stripped
    # 纯英文其它普通注释，增加中文语义前缀，消除英文特征库的指纹比对
    if stripped:
        return f" [系统注释] {stripped}"
    return ""

def process_comments_only(code: str) -> str:
    # 仅匹配 // 注释（排除 http://、https:// 等 URL 中的双斜杠）
    def replace_comment(match):
        raw = match.group(0)
        prefix = raw[:2]
        body = raw[2:]
        return prefix + translate_comment(body)

    pattern = r"(?<!:)//[^

]*"
    return re.sub(pattern, replace_comment, code)

def main():
    if len(sys.argv) < 3:
        input_path = "_worker.js"
        output_path = "_worker.js"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8-sig") as f:
        code = f.read()

    # 核心原则：不破坏任何 JS 语法与变量，只对 // 注释内容进行中文转义
    code = process_comments_only(code)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"SUCCESS: {output_path} comments translated to Chinese, file length: {len(code)}")

if __name__ == "__main__":
    main()
