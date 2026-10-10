import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")

# 1. 英文短语库 -> 地道中文（覆盖 Cloudflare Worker、Pages、代理协议与 Web 标准）
EN_PHRASE_DICT = {
    "convert base64 text back into a string at runtime to avoid having plaintext keywords that can be searched in the source code": "运行时把 base64 文本还原成字符串，避免源码里出现可被检索的明文关键词",
    "set default values if not provided": "⚙️ 设置默认全局环境变量（若未在面板提供配置参数）",
    "check if user is authenticated": "🔐 校验访问用户的安全令牌与身份鉴权凭证",
    "return unauthorized response": "🚫 返回未授权访问状态报文并执行安全重定向",
    "fallback proxy ip": "🌐 兜底中继代理 IP 地址端点列表",
    "error handling": "🛡️ 执行安全容错拦截与异常恢复机制",
    "handle websocket": "🔄 处理边缘 WebSocket 双向全双工数据流隧道",
    "parse request": "📡 解析客户端入站 HTTP 请求头与路由路径参数",
    "generate response": "📦 构建并返回符合规范的边缘响应数据报文",
    "connect to remote": "⚡ 建立与远端目标主机的 TCP/TLS 握手与连接",
    "proxy ip": "🌐 中继代理网络出口 IP 端点",
    "sub info": "📊 读取并生成订阅节点元数据与流量配额状态信息",
    "clean up": "🧹 清理并释放套接字描述符与系统运行内存资源",
    "listen for incoming": "🎧 监听并捕获边缘入站流量与会话传输通道",
    "read header": "📑 读取并解析二进制数据流协议首部信息",
    "write data": "📝 向目标套接字管道持续写入载荷数据包",
    "close connection": "🔒 安全终止并关闭边缘网络连接会话",
    "validate token": "🔑 校验安全访问令牌与数字签名哈希",
    "dynamic configuration": "💾 从边缘 KV 命名空间加载动态配置参数"
}

# 2. 已有中文注释智能同义改写库（换说法不改意思）
ZH_SYNONYM_DICT = {
    "返回正常响应": "向客户端回复成功状态报文",
    "处理请求": "调度并执行接入的请求流程",
    "错误处理": "执行安全容错拦截与异常恢复",
    "获取配置": "读取边缘环境变量与运行时上下文",
    "验证通过": "通过访问鉴权与安全规则校验",
    "建立连接": "建立底层网络双向传输通道",
    "关闭连接": "安全释放套接字网络连接",
    "数据转发": "执行双向数据流管道转发传输"
}

class JSLexerCommentRewriter:
    def __init__(self, phrase_dict=None, zh_synonym_dict=None):
        self.phrase_dict = phrase_dict or EN_PHRASE_DICT
        self.zh_synonym_dict = zh_synonym_dict or ZH_SYNONYM_DICT

    def rewrite_comment_text(self, text: str) -> str:
        stripped = text.strip()
        lower = stripped.lower()

        # 优先匹配英文短语
        for en_key, zh_val in self.phrase_dict.items():
            if en_key in lower:
                return " " + zh_val

        # 中文同义智能改写
        res = stripped
        matched_zh = False
        for zh_key, zh_syn in self.zh_synonym_dict.items():
            if zh_key in res:
                res = res.replace(zh_key, zh_syn)
                matched_zh = True
        if matched_zh:
            return " " + res

        # 如果已经是其他中文，则保持
        if any("\u4e00" <= ch <= "\u9fff" for ch in stripped):
            return " " + stripped

        # 兜底英文说明文本
        if stripped:
            return f" 💡 [配置说明] {stripped}"
        return ""

    def process(self, code: str) -> str:
        length = len(code)
        i = 0
        output = []
        state = "NORMAL"
        prev_non_ws = None

        while i < length:
            ch = code[i]
            nxt = code[i + 1] if i + 1 < length else ""

            if state == "NORMAL":
                if ch == '"':
                    state = "DOUBLE_QUOTE"
                    output.append(ch)
                    i += 1
                elif ch == "'":
                    state = "SINGLE_QUOTE"
                    output.append(ch)
                    i += 1
                elif ch == "`":
                    state = "TEMPLATE_LITERAL"
                    output.append(ch)
                    i += 1
                elif ch == "/" and nxt == "/":
                    # 词法状态机精准捕获真正的单行注释！
                    i += 2
                    comment_chars = []
                    while i < length and code[i] not in ("\r", "\n"):
                        comment_chars.append(code[i])
                        i += 1
                    raw_comment = "".join(comment_chars)
                    rewritten = self.rewrite_comment_text(raw_comment)
                    output.append("//" + rewritten)
                elif ch == "/" and nxt == "*":
                    output.append("/*")
                    i += 2
                    while i < length:
                        if code[i] == "*" and (i + 1 < length and code[i + 1] == "/"):
                            output.append("*/")
                            i += 2
                            break
                        output.append(code[i])
                        i += 1
                elif ch == "/":
                    is_regex = False
                    if prev_non_ws in (None, "=", "(", "[", "{", ",", ";", "!", "?", ":", "&", "|", "~", "^", "+", "-", "*", "%", "<", ">"):
                        is_regex = True
                    if is_regex:
                        state = "REGEX"
                        output.append(ch)
                        i += 1
                    else:
                        output.append(ch)
                        prev_non_ws = ch
                        i += 1
                else:
                    output.append(ch)
                    if not ch.isspace():
                        prev_non_ws = ch
                    i += 1

            elif state == "DOUBLE_QUOTE":
                output.append(ch)
                if ch == "\\":
                    if i + 1 < length:
                        output.append(code[i + 1])
                        i += 2
                    else:
                        i += 1
                elif ch == '"':
                    state = "NORMAL"
                    prev_non_ws = '"'
                    i += 1
                else:
                    i += 1

            elif state == "SINGLE_QUOTE":
                output.append(ch)
                if ch == "\\":
                    if i + 1 < length:
                        output.append(code[i + 1])
                        i += 2
                    else:
                        i += 1
                elif ch == "'":
                    state = "NORMAL"
                    prev_non_ws = "'"
                    i += 1
                else:
                    i += 1

            elif state == "TEMPLATE_LITERAL":
                output.append(ch)
                if ch == "\\":
                    if i + 1 < length:
                        output.append(code[i + 1])
                        i += 2
                    else:
                        i += 1
                elif ch == "`":
                    state = "NORMAL"
                    prev_non_ws = "`"
                    i += 1
                elif ch == "$" and nxt == "{":
                    output.append("{")
                    i += 2
                    brace_count = 1
                    sub_chars = []
                    while i < length and brace_count > 0:
                        sub_c = code[i]
                        if sub_c == "{" and code[i-1] != "\\":
                            brace_count += 1
                        elif sub_c == "}" and code[i-1] != "\\":
                            brace_count -= 1
                            if brace_count == 0:
                                i += 1
                                break
                        sub_chars.append(sub_c)
                        i += 1
                    sub_processed = self.process("".join(sub_chars))
                    output.append(sub_processed + "}")
                else:
                    i += 1

            elif state == "REGEX":
                output.append(ch)
                if ch == "\\":
                    if i + 1 < length:
                        output.append(code[i + 1])
                        i += 2
                    else:
                        i += 1
                elif ch == "/":
                    i += 1
                    while i < length and code[i].isalpha():
                        output.append(code[i])
                        i += 1
                    state = "NORMAL"
                    prev_non_ws = "/"
                else:
                    i += 1

        return "".join(output)

def verify_cf_entrypoints(code: str) -> bool:
    """
    自动化预检 Cloudflare 入口点兼容性：
    1. ES Module: export default { async fetch(request, env, ctx) }
    2. Pages Functions: export async function onRequest / onRequestGet / onRequestPost
    3. Classic Service Worker: addEventListener('fetch', ...)
    """
    patterns = [
        r"export\s+default\s*\{",
        r"export\s+async\s+function\s+onRequest",
        r"addEventListener\s*\(\s*['\"]fetch['\"]"
    ]
    for p in patterns:
        if re.search(p, code):
            return True
    return False

def fix_upstream_ast_const(code: str) -> str:
    # 修复上游变量重复赋值 AST 瑕疵，杜绝 esbuild Cannot assign to constant
    return re.sub(r"\bconst\b", "let", code)

def main():
    if len(sys.argv) < 3:
        input_path = "Vless_workers_pages/_worker.js"
        output_path = "Vless_workers_pages/_worker.js"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8-sig") as f:
        code = f.read()

    # 1. 语法级状态机纯注释改写
    rewriter = JSLexerCommentRewriter()
    code = rewriter.process(code)

    # 2. 修复 const 赋值语法
    code = fix_upstream_ast_const(code)

    # 3. 入口与语法预检
    is_valid_entry = verify_cf_entrypoints(code)
    print(f"Cloudflare 入口特征检测通过: {is_valid_entry}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"SUCCESS: {output_path} 处理完成，字符数: {len(code)}")

if __name__ == "__main__":
    main()
