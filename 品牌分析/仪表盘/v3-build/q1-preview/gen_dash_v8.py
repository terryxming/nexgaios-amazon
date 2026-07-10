# -*- coding: utf-8 -*-
"""V3 仪表盘 v8: 全局外壳(1440px+吸顶Tab) + Q1样板(6层模板+图表规范) + Q2-Q6占位。按架构契约。"""
import json, io
S=r'C:\Users\EDY\AppData\Local\Temp\claude\D--nexgaios-amazon\ac0b4daa-c9bf-4bf5-bce0-fed60a21c3ff\scratchpad'
d=json.load(open(S+r'\q1_v6_data.json',encoding='utf-8'))
months=d['months']; lxd=d['lx']; sv_stb=d['sv_stb']; od_stb=d['od_stb']
mm=['%02d'%m for m in range(1,13)]
lx2025=[lxd['2025-'+m] for m in mm]
lx2026=[lxd.get('2026-'+m) for m in mm[:6]]+[None]*6
sv2025=[None]+sv_stb[0:11]; sv2026=sv_stb[11:17]+[None]*6
od2025=[None]+od_stb[0:11]; od2026=od_stb[11:17]+[None]*6
DATA=json.dumps({'lx2025':lx2025,'lx2026':lx2026,'sv2025':sv2025,'sv2026':sv2026,'od2025':od2025,'od2026':od2026},ensure_ascii=False)

HTML=r'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ikarao V3 增长仪表盘</title><script src="echarts.min.js"></script>
<style>
:root{--bg:#eef1f5;--panel:#fff;--ink:#18202e;--muted:#5b6675;--line:#e3e8ef;--line2:#eef2f7;--brand:#2f6df6;--good:#0f9d76;--bad:#d0453b;--warn:#b96a12;--us:#0f9d76;--mkt:#5b6b8c;--mkt-l:#aab4c8;--data:#e8f0ff;--data-ink:#1f5fd6;--exp:#fff2e2;--exp-ink:#a85c12;--shadow:0 1px 3px rgba(20,30,50,.08);--r:14px;--s1:8px;--s2:16px;--s3:24px;--s4:32px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.65;font-family:"Segoe UI",-apple-system,"Microsoft YaHei","PingFang SC",Roboto,Arial,sans-serif;font-variant-numeric:tabular-nums}
.wrap{max-width:1440px;margin:0 auto;padding:0 40px 72px}
/* 全局头 */
header.top{padding:22px 30px;margin-top:24px;background:linear-gradient(120deg,#22335a,#33527f);color:#fff;border-radius:var(--r);box-shadow:var(--shadow)}
header.top h1{font-size:23px;margin:0}
header.top .sub{font-size:13.5px;opacity:.9;margin-top:8px;line-height:1.7}
.src{display:inline-block;font-size:11px;font-weight:700;color:#fff;border-radius:4px;padding:1px 6px;margin-left:3px;vertical-align:1px;letter-spacing:.3px}
.src.sqp{background:var(--mkt)}.src.lx{background:var(--us)}
/* 吸顶 Tab */
nav.tabs{position:sticky;top:0;z-index:20;margin-top:var(--s2);padding:8px;background:rgba(255,255,255,.92);backdrop-filter:blur(6px);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);display:flex;gap:4px;flex-wrap:wrap}
nav.tabs button{font-size:14px;font-weight:600;padding:9px 16px;border:0;background:transparent;color:var(--muted);border-radius:8px;cursor:pointer}
nav.tabs button.on{background:var(--brand);color:#fff}
nav.tabs button:not(.on):hover{background:var(--line2);color:var(--ink)}
/* 模块通用 */
section.q{display:none;margin-top:var(--s3)}
section.q.on{display:block}
.qhead{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:var(--s2)}
.qhead .qn{font-size:14px;font-weight:800;color:#fff;background:var(--brand);border-radius:6px;padding:4px 11px}
.qhead h2{font-size:20px;margin:0}
.qhead .badge{font-size:13px;color:var(--muted);background:var(--line2);border:1px solid var(--line);border-radius:8px;padding:4px 12px;margin-left:auto}
.concl{background:#f6f9ff;border:1px solid #cfe0f7;border-left:5px solid var(--brand);border-radius:var(--r);padding:22px 28px;font-size:24px;font-weight:800;line-height:1.5;box-shadow:var(--shadow)}
.concl .g{color:var(--good)}.concl .lead{display:block;font-size:15.5px;font-weight:500;color:#333e4d;margin-top:10px;line-height:1.8}
.kpirow{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s2);margin-top:var(--s3)}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow)}
.kpi .lab{font-size:13px;color:var(--muted)}
.kpi .val{font-size:25px;font-weight:800;margin-top:5px;line-height:1.1}.val.g{color:var(--good)}.val.b{color:var(--bad)}.val.n{color:var(--ink)}
.kpi .sub{font-size:12.5px;color:var(--muted);margin-top:4px}
.slab{font-size:16px;font-weight:800;margin:var(--s3) 0 var(--s2);padding-left:11px;border-left:4px solid var(--brand)}
.charts{display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s2)}
.chart-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
.chart-card h3{font-size:14.5px;margin:0 0 2px}.chart-card .cap{font-size:12px;color:var(--muted);margin-bottom:2px}
.ech{width:100%;height:250px}
.ntab{border-collapse:collapse;width:100%;margin-top:var(--s2);font-size:14px;background:var(--panel);box-shadow:var(--shadow);border-radius:8px;overflow:hidden}
.ntab th,.ntab td{border:1px solid var(--line);padding:9px 14px;text-align:center}
.ntab th{background:#f3f6fb;font-weight:700}.ntab td:first-child,.ntab th:first-child{text-align:left}
.ntab tr.new td{background:#fff8ee}.ntab tr.tot td{background:#f7f9fc;font-weight:600}
.ntab .cap{font-size:13px;color:var(--muted);padding:8px 14px;text-align:left;background:#fbfcfe}
.hl{color:var(--bad);font-weight:800}.rd{color:var(--bad);font-weight:700}
.acts{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s2)}
.act{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow)}
.act .ah{display:flex;align-items:center;gap:8px;margin-bottom:7px}
.act .chip{font-size:12px;font-weight:700;padding:3px 9px;border-radius:6px}
.act .chip.d{background:var(--data);color:var(--data-ink)}.act .chip.e{background:var(--exp);color:var(--exp-ink)}
.act .at{font-size:15px;font-weight:700}.act .ab{font-size:14px;line-height:1.7;color:#313b49}
.audit{margin-top:var(--s3);border:1px solid var(--line);border-radius:12px;background:var(--panel);box-shadow:var(--shadow)}
.audit>summary{font-size:15px;font-weight:700;color:var(--brand);cursor:pointer;padding:15px 22px;list-style:none;user-select:none;border-radius:12px}
.audit>summary:hover{background:#f5f9ff}.audit>summary::-webkit-details-marker{display:none}.audit>summary::before{content:"▸ "}.audit[open]>summary::before{content:"▾ "}
.audit .abox{padding:0 22px 18px;font-size:14px;line-height:1.9;columns:2;column-gap:40px}
.audit h4{font-size:14.5px;margin:14px 0 4px;break-after:avoid}.audit ul{margin:5px 0;padding-left:22px}.audit li{margin:3px 0}.audit .k{font-weight:700}
.ph{background:var(--panel);border:1px dashed var(--line);border-radius:var(--r);padding:60px 30px;text-align:center;color:var(--muted);font-size:16px}
</style></head><body><div class="wrap">
<header class="top"><h1>Ikarao · 卡拉OK机（美国亚马逊）· V3 增长决策仪表盘</h1>
<div class="sub">数据窗口 <b>2025-02 ~ 2026-06</b>｜同比=跟去年同期比 · 环比=看今年逐月走势｜来源：市场用亚马逊搜索报告<span class="src sqp">SQP</span>，真实销量用后台实盘<span class="src lx">领星</span>（两把尺口径不同、不相互对账）</div></header>

<nav class="tabs" id="nav">
<button data-q="q1" class="on">Q1 市场与季节</button><button data-q="q2">Q2 我们在赢份额吗</button><button data-q="q3">Q3 五款角色</button>
<button data-q="q4">Q4 漏斗漏点</button><button data-q="q5">Q5 抢词守词</button><button data-q="q6">Q6 增长与护栏</button></nav>

<!-- ============ Q1 ============ -->
<section class="q on" id="q1">
<div class="qhead"><span class="qn">Q1</span><h2>市场在增长吗？我们呢？</h2><span class="badge">口径：可比老词（同一批词）· 今年 2–6 月同比</span></div>

<div class="concl">搜索侧市场<b>没在扩张</b>——可比口径（只比同一批词）下需求持平、成交仍在收缩；但<span class="g">我们逆势增长 24.6%</span>，从对手手里抢下更多份额。
<span class="lead">核心判断：不是市场变大带动我们，而是我们在不增长的盘子里靠份额与旺季做出真实增量。诚实边界：三份报告只有"搜索侧"、领星只有我们自己，全品类真实总量拿不到，对市场只能保守假设"不增长"。</span></div>

<div class="kpirow">
<div class="kpi"><div class="lab">市场搜索需求（可比）<span class="src sqp">SQP</span></div><div class="val n">−0.9%</div><div class="sub">同比 · 持平略降</div></div>
<div class="kpi"><div class="lab">市场成交（可比）<span class="src sqp">SQP</span></div><div class="val b">−7.6%</div><div class="sub">同比 · 收缩</div></div>
<div class="kpi"><div class="lab">我们真实销量<span class="src lx">领星</span></div><div class="val g">+24.6%</div><div class="sub">13,758 → 17,146 台</div></div>
<div class="kpi"><div class="lab">我们搜索侧份额<span class="src sqp">SQP</span></div><div class="val n">3.07→3.77%</div><div class="sub">+0.70 个百分点</div></div>
</div>

<div class="slab">图表 · 逐月走势（同比看两线差、环比看走势；默认停上半年，可拖看旺季）</div>
<div class="charts">
<div class="chart-card"><h3>我们真实销量<span class="src lx">领星</span></h3><div class="cap">台 · 2025 vs 2026（今年止 6 月）</div><div class="ech" id="c-lx"></div></div>
<div class="chart-card"><h3>市场搜索需求（可比老词）<span class="src sqp">SQP</span></h3><div class="cap">搜索次数 · 2025 vs 2026</div><div class="ech" id="c-sv"></div></div>
<div class="chart-card"><h3>市场成交（可比老词）<span class="src sqp">SQP</span></h3><div class="cap">搜索侧成交 · 2025 vs 2026</div><div class="ech" id="c-od"></div></div>
</div>
<table class="ntab">
<tr><th>新增需求拆解（可比口径会漏掉的换血/长尾词）<span class="src sqp">SQP</span></th><th>搜索量 同比</th><th>成交 同比</th><th>转化率（2026 当期）</th></tr>
<tr><td>老词（可比 · 去年今年都在榜，171 个）</td><td>−0.9%</td><td class="rd">−7.6%</td><td>2.4%</td></tr>
<tr class="new"><td>非稳定篮子词（换血 / 长尾）</td><td>+133%</td><td>+0.8%</td><td><span class="hl">0.9%</span></td></tr>
<tr class="tot"><td>全部词（全榜合计）</td><td>+13.4%</td><td class="rd">−6.8%</td><td>2.1%</td></tr>
<tr><td class="cap" colspan="4">换血/长尾词是"高搜索、低转化"的泛流量（多 45.8 万次搜索、成交只多 56 单）。无论看老词还是全榜，市场真实成交都在缩；"搜索 +13.4%"全由这批不转化的词撑起。</td></tr>
</table>

<div class="slab">解读要点</div>
<div class="acts">
<div class="act"><div class="ah"><span class="chip d">数据支撑</span><span class="at">搜索侧市场未扩张</span></div><div class="ab">可比老词成交 −7.6%、全榜 −6.8%、换血词转化率仅 0.9%<span class="src sqp">SQP</span>。搜索侧的量没有真实变大，全品类真实总量三源都拿不到——<b>不宜把"市场自然增长"作为下半年资源规划前提。</b></div></div>
<div class="act"><div class="ah"><span class="chip e">专家建议</span><span class="at">不追高搜索低转化的新词</span></div><div class="ab">+133% 的新增搜索是泛流量、几乎不成交，追它=为不转化的曝光付费。例外只有明确产品缺口（如儿童款），属新产品线立项、非现有词加投。</div></div>
<div class="act"><div class="ah"><span class="chip e">专家建议</span><span class="at">增量靠份额与旺季</span></div><div class="ab">市场不增长，增量来自份额（自然优化）+ 旺季（去年 Q4 卖 35,298 台<span class="src lx">领星</span>、淡季 6–7 倍）。库存预算旺季前置；抢词/漏斗/护栏在 Q2–Q6，目标量在 Q6 定，此处不拍板。</div></div>
</div>

<details class="audit"><summary>审计 · 口径、算法与局限（可追溯原始数据）</summary><div class="abox">
<h4>① 两个来源、两把尺（禁止对账）</h4><ul>
<li><span class="k">SQP</span>：市场搜索/成交，仅统计"经搜索结果页"的动作，系统小于真实总量。</li>
<li><span class="k">领星</span>：我们全渠道真实成交（毛口径、未扣退货）。</li>
<li>二者不可相加/相除对账：市场搜索侧 −7.6% 与我们真实 +24.6% 是两把尺；我方 SQP 归因成交也只 +13.6%，同样≠领星、非互证。</li></ul>
<h4>② 老词/换血长尾/全榜（2–6 月同比）</h4><ul>
<li>老词=去年今年 2–6 月均在榜的 171 词，覆盖同期搜索侧成交 90.3%：搜索 −0.9%、成交 −7.6%。</li>
<li>换血/长尾=全榜减老词残差（两年都有值）：搜索 +133%、成交 +0.8%、转化率 0.9%。</li></ul>
<h4>③ 季节与环比</h4><ul>
<li>去年 Q4 领星真实 35,298 台；12 月 18,542 台 ≈ 淡季单月（约 2,800）的 6–7 倍。</li>
<li>今年上半年逐月：1 月 3,964 → 3 月 2,503（谷底）→ 6 月 4,855，先跌后涨为季节常态 + 主动提价减促。</li></ul>
<h4>④ 讲不了 / 不回答</h4><ul>
<li>缺去年 1 月市场数据（SQP 自 2025-02）；无全行业真实销量，"市场"结论均限"搜索侧"。</li>
<li>Q1 只答"市场与我们、今年比去年"；下半年投放/备货量在 Q6 统一定。</li>
<li>份额升幅约 ¾ 我们绝对量真涨、¼ 市场成交池缩的分母效应（成色见 Q2）。</li></ul>
</div></details>
</section>

<section class="q" id="q2"><div class="qhead"><span class="qn">Q2</span><h2>我们在赢份额吗？</h2></div><div class="ph">待建 · 将套用与 Q1 相同的 6 层模板（结论 / 关键指标 / 图表 / 解读要点 / 审计）</div></section>
<section class="q" id="q3"><div class="qhead"><span class="qn">Q3</span><h2>五款产品各扮什么角色？</h2></div><div class="ph">待建 · 5-ASIN 角色矩阵</div></section>
<section class="q" id="q4"><div class="qhead"><span class="qn">Q4</span><h2>转化漏斗漏在哪？</h2></div><div class="ph">待建 · SQP 漏斗 × 搜索目录自家漏斗</div></section>
<section class="q" id="q5"><div class="qhead"><span class="qn">Q5</span><h2>该抢哪些词、守哪些词？</h2></div><div class="ph">待建 · SQP 份额 × 热门搜索词竞品 ASIN</div></section>
<section class="q" id="q6"><div class="qhead"><span class="qn">Q6</span><h2>增长打法与 7% 利润护栏</h2></div><div class="ph">待建 · SQP 机会 × 领星运营组合毛利</div></section>
</div>

<script>
const D=__DATA__;const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const fmt=n=>n==null?'':Math.round(n).toLocaleString('en-US');const kfmt=v=>v>=1000?Math.round(v/1000)+'k':v;
const MON=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
const charts=[];
function line2(id,y25,y26,color,unit){
 const c=echarts.init(document.getElementById(id));charts.push(c);
 c.setOption({textStyle:{fontSize:12},grid:{left:46,right:14,top:30,bottom:44},legend:{data:['去年 2025','今年 2026'],top:2,itemWidth:22,itemHeight:8,textStyle:{fontSize:12}},
  tooltip:{trigger:'axis',valueFormatter:v=>v==null?'—':fmt(v)+unit},
  xAxis:{type:'category',data:MON,boundaryGap:false,axisLabel:{fontSize:11,color:css('--muted')}},
  yAxis:{type:'value',axisLabel:{fontSize:11,color:css('--muted'),formatter:kfmt},splitLine:{lineStyle:{color:css('--line2')}}},
  dataZoom:[{type:'inside',startValue:0,endValue:5},{type:'slider',startValue:0,endValue:5,bottom:8,height:16,textStyle:{fontSize:10,color:css('--muted')},fillerColor:'rgba(47,109,246,0.08)',handleStyle:{color:'#fff',borderColor:css('--brand')}}],
  series:[{name:'去年 2025',type:'line',data:y25,connectNulls:false,symbol:'circle',symbolSize:4,lineStyle:{type:'dashed',width:1.8,color:'#b3bcc9'},itemStyle:{color:'#b3bcc9'}},
   {name:'今年 2026',type:'line',data:y26,connectNulls:false,symbol:'circle',symbolSize:5,lineStyle:{width:2.6,color:color},itemStyle:{color:color}}]});
}
line2('c-lx',D.lx2025,D.lx2026,css('--us'),' 台');
line2('c-sv',D.sv2025,D.sv2026,css('--mkt'),' 次');
line2('c-od',D.od2025,D.od2026,css('--mkt'),' 单');
// tab 切换
document.getElementById('nav').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 document.querySelectorAll('#nav button').forEach(x=>x.classList.toggle('on',x===b));
 document.querySelectorAll('section.q').forEach(s=>s.classList.toggle('on',s.id===b.dataset.q));
 if(b.dataset.q==='q1')charts.forEach(c=>c.resize());});
window.addEventListener('resize',()=>charts.forEach(c=>c.resize()));
</script></body></html>'''
HTML=HTML.replace('__DATA__',DATA)
OUT=r'D:\nexgaios-amazon\品牌分析\仪表盘\07_Q1_稳定篮子预览.html'
io.open(OUT,'w',encoding='utf-8').write(HTML)
print('written',OUT,'bytes',len(HTML))
