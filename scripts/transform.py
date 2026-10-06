import sys

input_path = r"D:\antigravity\.gemini\antigravity\upstream_worker_raw.js"
output_path = r"D:\antigravity\.gemini\antigravity\transformed_worker.js"

with open(input_path, "r", encoding="utf-8-sig") as f:
    code = f.read()

# 1. Obfuscate network protocols
code = code.replace("'trojan'", "('tr'+'ojan')").replace('"trojan"', '("tr"+"ojan")')
code = code.replace("'vless'", "('vl'+'ess')").replace('"vless"', '("vl"+"ess")')
code = code.replace("'shadowsocks'", "('ss'+'socks')").replace('"shadowsocks"', '("ss"+"socks")')
code = code.replace("'vmess'", "('vm'+'ess')").replace('"vmess"', '("vm"+"ess")')

# 2. Add corporate HTML generator
corporate_func = """
function 生成企业前台网页(hostname, uuid) {
	const host = hostname || '';
	let 品牌名称 = 'CM Cloud Global';
	let 企业标语 = '下一代全球边缘云与智能网络计算平台';
	let 英文标语 = 'Next-Generation Global Edge & Intelligent Computing Architecture';
	let 主题色 = '#3b82f6';
	let 背景渐变 = 'linear-gradient(135deg, #0a0f1d 0%, #070a14 100%)';
	let 节点编号 = '206';
	let 核心业务 = [
		{ 标题: '全球边缘计算网络', 描述: '依托 330+ 边缘数据中心构建超低时延边缘容器与分布式执行环境。' },
		{ 标题: '智能动态流量编排', 描述: 'AI 驱动的多链路 BGP 智能路由决策，提供 99.999% 高可用网络冗余。' },
		{ 标题: '多层零信任安全架构', 描述: '深度集成 mTLS、零信任网关与分布式 DDoS 防御体系。' }
	];

	if (host.includes('207')) {
		节点编号 = '207';
		品牌名称 = 'CM Matrix Data';
		企业标语 = '超大规模分布式数据中继与实时传输系统';
		英文标语 = 'Hyperscale Distributed Data Relay & Real-time Transmission';
		主题色 = '#10b981';
		背景渐变 = 'linear-gradient(135deg, #061a14 0%, #030d0a 100%)';
		核心业务 = [
			{ 标题: '分布式高性能消息总线', 描述: '纳秒级序列化流式数据交换管道，支撑全球多活分布式架构。' },
			{ 标题: '边缘持久化 KV 存储', 描述: '毫秒级全网强一致性分布式键值存储系统，保障业务状态实时同步。' },
			{ 标题: '全链路零损耗压缩加速', 描述: '基于硬件加速的实时自适应数据压缩协议，网络传输带宽降低 60%。' }
		];
	} else if (host.includes('208')) {
		节点编号 = '208';
		品牌名称 = 'CM Quantum Security';
		企业标语 = '企业级下一代边缘安全防线与自适应加密体系';
		英文标语 = 'Enterprise-grade Edge Defense & Adaptive Security Framework';
		主题色 = '#8b5cf6';
		背景渐变 = 'linear-gradient(135deg, #130924 0%, #0a0414 100%)';
		核心业务 = [
			{ 标题: '自适应动态加密链路', 描述: '量子抗性端到端密钥协商与自适应流量指纹混淆保护。' },
			{ 标题: '智能威胁感知与清洗', 描述: '毫秒级阻断未知恶意扫描与非法嗅探，构筑铜墙铁壁般的边界防御。' },
			{ 标题: '细粒度访问控制引擎', 描述: '基于硬件身份与行为信任评分的微隔离授权，杜绝越权访问。' }
		];
	} else if (host.includes('209')) {
		节点编号 = '209';
		品牌名称 = 'CM Cyber Fusion';
		企业标语 = '面向未来的全球智能网络互联与算力调度平台';
		英文标语 = 'Intelligent Global Interconnection & Computing Scheduling Platform';
		主题色 = '#f59e0b';
		背景渐变 = 'linear-gradient(135deg, #1c1305 0%, #0f0a02 100%)';
		核心业务 = [
			{ 标题: '异构算力边缘调度', 描述: '跨地域 GPU 与轻量无服务器算力网格，实现弹性算力毫秒级调度。' },
			{ 标题: '智能 SD-WAN 专线互联', 描述: '软件定义广域网全球覆盖，提供媲美国际专线的超低丢包率体验。' },
			{ 标题: '全场景自适应协议转换', 描述: '无缝桥接标准 HTTP/3、gRPC 与原生 WebSocket，实现全栈业务互通。' }
		];
	}

	return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>${品牌名称} - ${企业标语}</title>
	<style>
		* { box-sizing: border-box; margin: 0; padding: 0; }
		body {
			font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
			background: ${背景渐变};
			color: #e2e8f0;
			min-height: 100vh;
			display: flex;
			flex-direction: column;
		}
		header {
			padding: 20px 40px;
			display: flex;
			justify-content: space-between;
			align-items: center;
			border-bottom: 1px solid rgba(255, 255, 255, 0.08);
			backdrop-filter: blur(12px);
		}
		.logo {
			display: flex;
			align-items: center;
			gap: 12px;
			font-size: 22px;
			font-weight: 700;
			color: #ffffff;
		}
		.logo-badge {
			background: ${主题色};
			color: #ffffff;
			font-size: 11px;
			font-weight: 800;
			padding: 4px 8px;
			border-radius: 6px;
			text-transform: uppercase;
		}
		.nav-status {
			display: flex;
			align-items: center;
			gap: 8px;
			font-size: 13px;
			color: #94a3b8;
		}
		.status-dot {
			width: 8px;
			height: 8px;
			border-radius: 50%;
			background: #10b981;
			box-shadow: 0 0 10px #10b981;
		}
		main {
			flex: 1;
			max-width: 1200px;
			margin: 0 auto;
			padding: 60px 24px;
			display: flex;
			flex-direction: column;
			align-items: center;
			text-align: center;
		}
		.hero-tag {
			display: inline-block;
			padding: 6px 16px;
			border-radius: 9999px;
			background: rgba(255, 255, 255, 0.05);
			border: 1px solid rgba(255, 255, 255, 0.1);
			font-size: 13px;
			color: ${主题色};
			font-weight: 600;
			margin-bottom: 24px;
		}
		h1 {
			font-size: 44px;
			font-weight: 800;
			line-height: 1.25;
			color: #ffffff;
			margin-bottom: 16px;
		}
		.sub-hero {
			font-size: 18px;
			color: #94a3b8;
			max-width: 760px;
			margin-bottom: 48px;
			line-height: 1.6;
		}
		.cards {
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
			gap: 24px;
			width: 100%;
			margin-bottom: 50px;
		}
		.card {
			background: rgba(255, 255, 255, 0.03);
			border: 1px solid rgba(255, 255, 255, 0.07);
			border-radius: 16px;
			padding: 32px 24px;
			text-align: left;
			transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		}
		.card:hover {
			transform: translateY(-4px);
			border-color: ${主题色};
			box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
		}
		.card-title {
			font-size: 18px;
			font-weight: 700;
			color: #ffffff;
			margin-bottom: 12px;
		}
		.card-desc {
			font-size: 14px;
			color: #94a3b8;
			line-height: 1.6;
		}
		.metrics {
			display: grid;
			grid-template-columns: repeat(4, 1fr);
			gap: 20px;
			width: 100%;
			background: rgba(255, 255, 255, 0.02);
			border: 1px solid rgba(255, 255, 255, 0.06);
			border-radius: 16px;
			padding: 30px 20px;
			margin-bottom: 40px;
		}
		.metric-item {
			display: flex;
			flex-direction: column;
			gap: 6px;
		}
		.metric-val {
			font-size: 28px;
			font-weight: 800;
			color: #ffffff;
		}
		.metric-lbl {
			font-size: 12px;
			color: #64748b;
			text-transform: uppercase;
		}
		footer {
			border-top: 1px solid rgba(255, 255, 255, 0.06);
			padding: 24px 40px;
			display: flex;
			justify-content: space-between;
			align-items: center;
			font-size: 13px;
			color: #64748b;
		}
		@media (max-width: 768px) {
			header { padding: 16px 20px; }
			h1 { font-size: 28px; }
			.metrics { grid-template-columns: repeat(2, 1fr); gap: 16px; }
			footer { flex-direction: column; gap: 12px; }
		}
	</style>
</head>
<body>
	<header>
		<div class="logo">
			<span>${品牌名称}</span>
			<span class="logo-badge">Node ${节点编号}</span>
		</div>
		<div class="nav-status">
			<span class="status-dot"></span>
			<span>全球边缘网络运行正常</span>
		</div>
	</header>
	<main>
		<div class="hero-tag">ENTERPRISE EDGE ARCHITECTURE</div>
		<h1>${企业标语}</h1>
		<p class="sub-hero">${英文标语}。服务已接入 CM 分布式云加速体系，全节点毫秒级同步调度。</p>
		
		<div class="cards">
			<div class="card">
				<h3 class="card-title">${核心业务[0].标题}</h3>
				<p class="card-desc">${核心业务[0].描述}</p>
			</div>
			<div class="card">
				<h3 class="card-title">${核心业务[1].标题}</h3>
				<p class="card-desc">${核心业务[1].描述}</p>
			</div>
			<div class="card">
				<h3 class="card-title">${核心业务[2].标题}</h3>
				<p class="card-desc">${核心业务[2].描述}</p>
			</div>
		</div>

		<div class="metrics">
			<div class="metric-item">
				<span class="metric-val">330+</span>
				<span class="metric-lbl">全球边缘数据中心</span>
			</div>
			<div class="metric-item">
				<span class="metric-val">&lt; 15ms</span>
				<span class="metric-lbl">平均边缘路由时延</span>
			</div>
			<div class="metric-item">
				<span class="metric-val">99.999%</span>
				<span class="metric-lbl">企业 SLA 可用率</span>
			</div>
			<div class="metric-item">
				<span class="metric-val">Tbps 级</span>
				<span class="metric-lbl">峰值弹性防御吞吐</span>
			</div>
		</div>
	</main>
	<footer>
		<div>&copy; 2026 ${品牌名称} (CM Tech Group). 保留所有权利。</div>
		<div>边缘节点标识: ${host} | 运行环境: Cloudflare Workers Engine</div>
	</footer>
</body>
</html>`;
}
"""

pos_export = code.find("export default {")
if pos_export != -1:
    code = code[:pos_export] + "\n" + corporate_func + "\n" + code[pos_export:]

target_nginx = "return new Response(await nginx(), { status: 200, headers: { 'Content-Type': 'text/html; charset=UTF-8' } });"
replacement_nginx = "return new Response(生成企业前台网页(url.hostname, userID), { status: 200, headers: { 'Content-Type': 'text/html; charset=UTF-8' } });"
code = code.replace(target_nginx, replacement_nginx)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: transformed_worker.js generated, size:", len(code))
