import sys, re

# 中文与形象化表情符号映射词库
COMMENT_DICT = {
    "set default values if not provided": "⚙️ 设置默认全局变量（若未提供环境配置）",
    "check if user is authenticated": "🔐 校验访问用户令牌与身份鉴权",
    "return unauthorized response": "🚫 返回未授权访问状态与安全重定向",
    "fallback proxy ip": "🌐 兜底中继代理 IP 地址端点",
    "error handling": "🛡️ 边缘网络请求异常捕获与容错处理",
    "handle websocket": "🔄 处理边缘 WebSocket 双向数据流隧道",
    "parse request": "📡 解析客户端入站 HTTP 请求头与路径参数",
    "generate response": "📦 构建并返回边缘响应数据流",
    "connect to remote": "⚡ 建立与远端目标主机的 TCP 握手与连接",
    "proxy ip": "🌐 中继代理网络出口 IP",
    "sub info": "📊 订阅节点元数据与流量状态信息",
    "clean up": "🧹 清理并释放套接字与内存资源",
    "listen for incoming": "🎧 监听入站流量与会话通道",
    "read header": "📑 读取并解析二进制数据流首部",
    "write data": "📝 向目标套接字写入载荷数据",
    "close connection": "🔒 安全关闭边缘网络连接会话",
    "validate token": "🔑 校验安全令牌与签名哈希",
    "dynamic configuration": "💾 从边缘 KV 空间加载动态配置参数"
}

def translate_comment_body(comment_body: str) -> str:
    stripped = comment_body.strip()
    lower = stripped.lower()
    for en_phrase, zh_text in COMMENT_DICT.items():
        if en_phrase in lower:
            return " " + zh_text
    if any("\u4e00" <= ch <= "\u9fff" for ch in stripped):
        return " " + stripped
    if stripped:
        return f" 💡 [配置说明] {stripped}"
    return ""

def process_standalone_comments_only(code: str) -> str:
    """
    100% 保护 JS 代码逻辑：
    只提取真正以 // 开头的独立注释行（允许前面有空格/缩进 ^\\s*//），
    严禁匹配或修改代码语句中的 //（如 URL 协议头、正则、字符串、行尾代码等）。
    """
    lines = code.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        stripped_left = line.lstrip()
        if stripped_left.startswith("//"):
            indent = line[:len(line) - len(stripped_left)]
            has_newline = line.endswith("\n")
            content_without_nl = line[:-1] if has_newline else line
            if content_without_nl.endswith("\r"):
                newline_suffix = "\r\n"
                comment_text = stripped_left[:-2]
            else:
                newline_suffix = "\n" if has_newline else ""
                comment_text = stripped_left[:-1] if has_newline else stripped_left

            body = comment_text[2:]
            translated = translate_comment_body(body)
            new_lines.append(indent + "//" + translated + newline_suffix)
        else:
            new_lines.append(line)
    return "".join(new_lines)

def main():
    if len(sys.argv) < 3:
        input_path = "_worker.js"
        output_path = "_worker.js"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8-sig") as f:
        code = f.read()

    # 仅对独立 // 注释行进行中文形象化语义转换，零改动其他代码
    code = process_standalone_comments_only(code)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"SUCCESS: {output_path} standalone comments translated, length: {len(code)}")

if __name__ == "__main__":
    main()
