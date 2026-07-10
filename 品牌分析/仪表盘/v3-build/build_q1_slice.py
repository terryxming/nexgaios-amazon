# -*- coding: utf-8 -*-
"""构建 V3 Q1 垂直切片(定稿版):两层结构(顶层白话+展开审计层)、修正口径、术语tooltip、
   KPI去重、年对年可辨(实心圆/空心方+端点标注+markArea)、篮子覆盖率披露。"""
import json, io, os

HERE  = os.path.dirname(os.path.abspath(__file__))          # 品牌分析/仪表盘/v3-build
DASH  = os.path.dirname(HERE)                                # 品牌分析/仪表盘
SLICE = os.path.join(HERE, 'q1_slice_data.json')
OUT   = os.path.join(DASH, '07_V3_Q1切片.html')            # 与 echarts.min.js 同目录(相对引用)
Q1 = json.load(io.open(SLICE, encoding='utf-8'))

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ikarao · V3 切片 · Q1 市场与季节</title>
<script src="echarts.min.js"></script>
<style>
  :root{
    --bg:#eef1f5;--panel:#fff;--ink:#18202e;--muted:#4d5766;--line:#e3e8ef;--line2:#eef2f7;
    --brand:#2f6df6;--good:#0f9d76;--bad:#d0453b;--warn:#c9691a;
    --demand:#0072B2;--order:#009E73;
    --data:#e8f0ff;--data-ink:#1f5fd6;--exp:#fff2e2;--exp-ink:#a85c12;
    --shadow:0 1px 3px rgba(20,30,50,.08),0 1px 2px rgba(20,30,50,.04);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.65;
    font-family:"Segoe UI",-apple-system,"Microsoft YaHei","PingFang SC",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1440px;width:100%;margin:0 auto;padding:22px 28px 64px}
  header.top{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;flex-wrap:wrap;
    padding:18px 24px;background:linear-gradient(120deg,#22335a,#33527f);color:#fff;border-radius:12px;box-shadow:var(--shadow)}
  header.top h1{font-size:22px;margin:0}
  header.top .sub{font-size:14px;opacity:.88;margin-top:6px}
  .seg-lab{font-size:14px;opacity:.85;margin-bottom:5px}
  .seg{display:inline-flex;background:#ffffff22;border-radius:9px;padding:3px;gap:2px}
  .seg button{font-size:14px;padding:7px 15px;border:0;background:transparent;color:#fff;border-radius:7px;cursor:pointer;opacity:.82}
  .seg button.on{background:#fff;color:var(--ink);opacity:1;font-weight:600}
  .seg button:focus-visible{outline:2px solid #fff;outline-offset:2px}
  section.mod{margin-top:20px;background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);overflow:hidden}
  .mhead{padding:15px 24px;border-bottom:1px solid var(--line2);display:flex;align-items:center;gap:12px;flex-wrap:wrap}
  .mhead .q{font-size:14px;font-weight:800;color:#fff;background:var(--brand);border-radius:6px;padding:4px 10px}
  .mhead h2{font-size:18px;margin:0}
  .badge-basis{font-size:14px;color:var(--muted);background:var(--line2);border:1px solid var(--line);border-radius:8px;padding:4px 12px;margin-left:auto}
  .mbody{padding:20px 24px}
  .sec-lab{font-size:15px;font-weight:700;color:var(--ink);margin:24px 0 10px;padding-left:10px;border-left:3px solid var(--brand)}
  .term{border-bottom:1px dashed var(--muted);cursor:help}
  .headline{background:#fafcff;border:1px solid var(--line);border-left:4px solid var(--brand);border-radius:10px;padding:18px 22px}
  .headline .concl{font-size:21px;font-weight:800;line-height:1.45;display:block;margin-bottom:10px}
  .headline .detail{font-size:15px;line-height:1.9;color:#313b49}
  .headline .cav{font-size:13.5px;color:var(--muted);margin-top:8px}
  .headline b{color:var(--ink)}
  .up{color:var(--good);font-weight:700}.down{color:var(--bad);font-weight:700}
  .kpirow{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:16px}
  @media(max-width:900px){.kpirow{grid-template-columns:repeat(2,1fr)}}
  .kpi{background:#fafcff;border:1px solid var(--line);border-radius:12px;padding:14px 16px}
  .kpi.hero{border-color:#bcd2ff;background:#f5f9ff}
  .kpi .lab{font-size:14px;color:var(--muted)}
  .kpi .val{font-size:24px;font-weight:800;margin-top:4px;line-height:1.2}
  .kpi .sub{font-size:14px;color:var(--muted);margin-top:4px}
  .charts{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:14px}
  @media(max-width:900px){.charts{grid-template-columns:1fr}}
  .chart-card{border:1px solid var(--line);border-radius:12px;padding:14px 16px}
  .chart-card h3{font-size:15px;margin:0 0 2px}
  .chart-card .cap{font-size:14px;color:var(--muted);margin-bottom:6px}
  .ech{width:100%;height:260px}
  .combined{font-size:15px;font-weight:600;color:var(--ink);background:#fff8ee;border:1px solid #f0dcc0;border-radius:8px;padding:12px 16px;margin-top:14px}
  .acts{display:flex;flex-direction:column;gap:12px}
  .act{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
  .act .act-head{display:flex;align-items:center;gap:10px;margin-bottom:6px}
  .act .act-title{font-size:15px;font-weight:700}
  .act .act-body{font-size:14px;line-height:1.75;color:#313b49}
  .tag{flex:none;font-size:14px;font-weight:700;padding:3px 10px;border-radius:6px}
  .tag.data{background:var(--data);color:var(--data-ink)}.tag.exp{background:var(--exp);color:var(--exp-ink)}
  .audit{margin-top:18px;border:1px solid var(--line);border-radius:12px;background:#fbfcfe}
  .audit>summary{font-size:15px;font-weight:700;color:var(--brand);cursor:pointer;padding:14px 18px;list-style:none;user-select:none}
  .audit>summary::-webkit-details-marker{display:none}
  .audit>summary::before{content:"▸ ";}
  .audit[open]>summary::before{content:"▾ ";}
  .audit .abox{padding:0 18px 16px;font-size:14px;line-height:1.9}
  .audit h4{font-size:14.5px;margin:14px 0 4px;color:var(--ink)}
  .audit ul{margin:6px 0;padding-left:22px}.audit li{margin:3px 0}
  .audit .k{color:var(--ink);font-weight:700}
  .foot{margin-top:20px;font-size:14px;color:var(--muted);line-height:1.8;border-top:1px solid var(--line);padding-top:14px}
  .foot b{color:var(--ink)}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <h1>Ikarao · 卡拉OK市场 增长仪表盘 <span style="opacity:.6;font-size:15px">V3 切片</span></h1>
      <div class="sub">品牌 <b>Ikarao</b> · 美国站 <span class="term" title="SQP＝亚马逊官方的“搜索查询绩效”报告(Search Query Performance),本页所有数据的来源:每个关键词在整个市场的搜索/点击/加购/成交,以及我们品牌拿到的部分。">SQP</span> · Q1 市场与季节 · <span id="rng"></span></div>
    </div>
    <div>
      <div class="seg-lab">市场口径 <span class="term" title="两种统计范围。核心整机:只算“卡拉OK整机”类搜索词(剔掉麦克风等配件词);宽口径:把所有相关词都算进来。切换会改变下面所有数字。">(?)</span></div>
      <div class="seg" id="segUni">
        <button data-v="core" class="on">核心整机</button>
        <button data-v="wide">宽口径</button>
      </div>
    </div>
  </header>

  <section class="mod" id="Q1">
    <div class="mhead">
      <span class="q">Q1</span><h2>市场在增长吗？季节性多强？</h2>
      <span class="badge-basis" id="basis"></span>
    </div>
    <div class="mbody">
      <div class="headline" id="headline"></div>
      <div class="kpirow" id="kpis"></div>

      <div class="sec-lab">趋势图 · 今年 vs 去年(逐月)</div>
      <div class="charts">
        <div class="chart-card"><h3>大盘搜索量（整个市场的搜索次数）</h3><div class="cap">横轴 1—12 月；实线圆点＝2026、虚线方点＝2025；阴影＝本报告对比的上半年</div><div class="ech" id="ch-demand"></div></div>
        <div class="chart-card"><h3>大盘成交量（整个市场的下单数）</h3><div class="cap">横轴 1—12 月；实线圆点＝2026、虚线方点＝2025；阴影＝本报告对比的上半年</div><div class="ech" id="ch-order"></div></div>
      </div>
      <div class="combined" id="combined"></div>

      <div class="sec-lab">解读与建议</div>
      <div class="acts" id="acts"></div>

      <details class="audit" id="audit">
        <summary>展开审计 · 每个数字怎么来的、为什么这么比</summary>
        <div class="abox" id="auditbox"></div>
      </details>

      <div class="foot" id="foot"></div>
    </div>
  </section>
</div>

<script>
const Q1 = __Q1DATA__;
const MONTHS = Q1.months;
let S = { uni:'core' };
const el = id => document.getElementById(id);
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const fmtK = n => Math.abs(n)>=1e6 ? (n/1e6).toFixed(2)+'M' : Math.abs(n)>=1e3 ? Math.round(n/1e3)+'k' : Math.round(n);
const fmtInt = n => Math.round(n).toLocaleString('en-US');
const g = (uni,ym) => Q1[uni][ym] || null;
const arrow = d => d>0?'▲':d<0?'▼':'▬';
const cl = d => d>0?'up':d<0?'down':'';
const pctTxt = d => (d>=0?'+':'−')+Math.abs(d).toFixed(1)+'%';
const ppTxt  = d => (d>=0?'+':'−')+Math.abs(d).toFixed(2)+'pp';
const T = (term,tip) => '<span class="term" title="'+tip.replace(/"/g,'&quot;')+'">'+term+'</span>';

function sumH1(uni, yr, field){ let s=0; for(let m=2;m<=6;m++){const r=g(uni,yr+'-'+String(m).padStart(2,'0')); if(r) s+=r[field];} return s; }
function calc(){
  const u=S.uni, D=Q1.derived[u];
  const sv25=sumH1(u,'2025','mkt_sv'), sv26=sumH1(u,'2026','mkt_sv');
  const od25=sumH1(u,'2025','mkt_ord'), od26=sumH1(u,'2026','mkt_ord');
  const my25=sumH1(u,'2025','my_ord'), my26=sumH1(u,'2026','my_ord');
  const sh25=od25?my25/od25*100:0, sh26=od26?my26/od26*100:0;
  return {sv25,sv26,od25,od26,my25,my26,sh25,sh26,
    svYoY:(sv26/sv25-1)*100, odYoY:(od26/od25-1)*100, myYoY:(my26/my25-1)*100, shPP:sh26-sh25, D};
}

/* ===== 徽标 + 头条(两行:结论 + 明细) ===== */
function renderBasis(){
  el('basis').textContent = '口径：'+(S.uni==='core'?'核心整机':'宽口径')+' · 上半年同比';
}
function renderHeadline(){
  const c=calc();
  const shareTip='购买份额＝我们品牌卖出量 ÷ 整个市场卖出量。3.43%→4.60% 是涨了 1.18 个百分点(不是 1.18%)。';
  const cvrTip='市场转化率＝整个市场“下单数 ÷ 搜索次数”。它掉了,说明搜的人里真买的比例在下降。';
  el('headline').innerHTML =
    '<span class="concl">搜索在涨、成交在缩——但我们逆势抢到了更多份额。</span>'+
    '<div class="detail">整个市场：'+T('搜索次数','大盘搜索量＝所有卖家在这些关键词上被搜到的总次数')+' <b>'+fmtInt(c.sv26)+
    '</b>（同比 <span class="'+cl(c.svYoY)+'">'+arrow(c.svYoY)+pctTxt(c.svYoY)+'</span>），可'+T('成交','下单/卖出量')+
    '却只有 <b>'+fmtInt(c.od26)+'</b>（同比 <span class="'+cl(c.odYoY)+'">'+arrow(c.odYoY)+pctTxt(c.odYoY)+
    '</span>）——<b>搜的人更多、真买的人却更少</b>（'+T('市场转化率',cvrTip)+' '+c.D.cvr25.toFixed(2)+'%→<b>'+c.D.cvr26.toFixed(2)+
    '%</b>）。而我们品牌自己：'+T('成交单量','我们品牌卖出的台数')+' '+fmtInt(c.my25)+'→<b>'+fmtInt(c.my26)+
    '</b>（<span class="'+cl(c.myYoY)+'">'+arrow(c.myYoY)+pctTxt(c.myYoY)+'</span>），'+T('购买份额',shareTip)+' '+
    c.sh25.toFixed(2)+'%→<b>'+c.sh26.toFixed(2)+'%</b>（<span class="'+cl(c.shPP)+'">'+ppTxt(c.shPP)+
    '</span>）——<b>在缩量的市场里，我们卖得更多、占的比例更高</b>。'+
    '</div><div class="cav">口径：上半年＝2 月至 6 月，共 5 个对照月（缺 2025 年 1 月、不含 11—12 月旺季），结论方向性看待。详细推导见下方「展开审计」。</div>';
}

/* ===== KPI(去重:与头条互补,不复读) ===== */
function renderKpis(){
  const c=calc();
  const cards=[
    {hero:1,lab:T('品牌成交单量','我们品牌卖出的台数(上半年合计)'),val:fmtInt(c.my26)+' 单',sub:'同比 <span class="'+cl(c.myYoY)+'">'+pctTxt(c.myYoY)+'</span>'},
    {lab:T('我们的购买份额','品牌卖出 ÷ 全市场卖出'),val:c.sh26.toFixed(2)+'%',sub:'同比 <span class="'+cl(c.shPP)+'">'+ppTxt(c.shPP)+'</span>'},
    {lab:T('市场转化率','全市场:下单数 ÷ 搜索次数'),val:c.D.cvr26.toFixed(2)+'%',sub:'同比 <span class="'+cl(c.D.cvr_pp)+'">'+ppTxt(c.D.cvr_pp)+'</span>（搜索转成交在变难）'},
    {lab:'2025 Q4 → 2026 目标',val:fmtInt(c.D.q4floor)+'→'+fmtInt(c.D.q4target),sub:'品牌 11+12 月：去年地板 → 按 +25% 外推目标'},
  ];
  el('kpis').innerHTML=cards.map(k=>'<div class="kpi'+(k.hero?' hero':'')+'"><div class="lab">'+k.lab+'</div><div class="val">'+k.val+'</div><div class="sub">'+k.sub+'</div></div>').join('');
}

/* ===== ECharts 年对年(实心圆2026/空心方2025 + 端点标注 + H1 markArea) ===== */
let charts={};
function yoySeries(uni,field,color){
  const y25=[],y26=[];
  for(let m=1;m<=12;m++){const k=String(m).padStart(2,'0');const a=g(uni,'2025-'+k),b=g(uni,'2026-'+k);
    y25.push(a?a[field]:null);y26.push(b?b[field]:null);}
  return [
    {name:'2025',type:'line',data:y25,connectNulls:false,symbol:'rect',symbolSize:8,
     lineStyle:{type:'dashed',width:2,color:color},itemStyle:{color:'#fff',borderColor:color,borderWidth:2},
     endLabel:{show:true,formatter:'2025',color:color,fontSize:13,fontWeight:'bold'},emphasis:{focus:'series'}},
    {name:'2026',type:'line',data:y26,connectNulls:false,symbol:'circle',symbolSize:8,
     lineStyle:{type:'solid',width:2.8,color:color},itemStyle:{color:color},
     endLabel:{show:true,formatter:'2026',color:color,fontSize:13,fontWeight:'bold'},emphasis:{focus:'series'},
     markArea:{silent:true,itemStyle:{color:'rgba(47,109,246,0.06)'},data:[[{xAxis:'2',name:'对比区'},{xAxis:'6'}]],label:{show:false}}},
  ];
}
function drawChart(id,field,color,unit){
  let c=charts[id];
  if(!c){c=charts[id]=echarts.init(el(id)); new ResizeObserver(()=>c.resize()).observe(el(id));}
  c.setOption({
    textStyle:{fontSize:14},
    grid:{left:52,right:44,top:22,bottom:28},
    tooltip:{trigger:'axis',textStyle:{fontSize:14},valueFormatter:v=>v==null?'—':fmtInt(v)+unit},
    xAxis:{type:'category',data:['1','2','3','4','5','6','7','8','9','10','11','12'],boundaryGap:false,
      axisLabel:{fontSize:14,color:css('--muted'),formatter:v=>v+'月'},axisLine:{lineStyle:{color:css('--line')}}},
    yAxis:{type:'value',axisLabel:{fontSize:14,color:css('--muted'),formatter:v=>fmtK(v)},splitLine:{lineStyle:{color:css('--line2')}}},
    series:yoySeries(S.uni,field,color)
  },true);
}
function renderCharts(){
  drawChart('ch-demand','mkt_sv',css('--demand'),'');
  drawChart('ch-order','mkt_ord',css('--order'),' 单');
  const c=calc();
  el('combined').innerHTML='<b>把两张图合起来看：</b>左图（搜索）实线在往上、右图（成交）实线在往下——<b>一升一降，就是"搜的人更多、买的人更少"的背离</b>。灰色阴影是本报告对比的上半年（2—6 月），年底那座高峰是圣诞旺季（见下方第 3 条建议）。';
}

/* ===== 解读(顶层简洁:数据/建议双标签拆开) ===== */
function renderActs(){
  const c=calc();
  const acts=[
    {tag:'数据支撑',title:'"背离"是事实：搜索涨、成交跌，转化在变难',
     body:'整个市场搜索同比 '+pctTxt(c.svYoY)+'、成交却 '+pctTxt(c.odYoY)+'；每次搜索转成下单的比例（市场转化率）从 '+c.D.cvr25.toFixed(2)+'% 掉到 '+c.D.cvr26.toFixed(2)+'%。这是本模块最该警惕的信号。'},
    {tag:'专家建议',title:'先拆成因，别急着加投放',
     body:'成交转弱可能是价格战／头部集中，也可能是儿童等"泛需求"把搜索量灌高了（这些人不买成人机）。先查清是哪种，再决定动作——而不是先砸广告买更多流量。'},
    {tag:'专家建议',title:'+25% 是真涨，但别过读',
     body:'品牌成交同比 '+pctTxt(c.myYoY)+'，同季逐月速度对比也是 +25%（不是虚高）。但 2025 上半年是品牌爬坡期、基数低，涨幅有一部分来自低基数；而 '+c.D.rr26+' 台/月仍是淡季速度，旺季目标要更高。'},
    {tag:'专家建议',title:'下半年动作绑季节性',
     body:'12 月是全年绝对峰值：搜索约为上半年月均的 '+c.D.decSvX.toFixed(1)+' 倍、成交约 '+c.D.decOdX.toFixed(1)+' 倍。备货与广告预算须在 10 月前就位。以去年 Q4 品牌成交 '+fmtInt(c.D.q4floor)+' 单为地板、按 +25% 外推约 '+fmtInt(c.D.q4target)+' 单为目标。'},
  ];
  el('acts').innerHTML=acts.map(a=>'<div class="act"><div class="act-head"><span class="tag '+(a.tag==='数据支撑'?'data':'exp')+'">'+a.tag+'</span><span class="act-title">'+a.title+'</span></div><div class="act-body">'+a.body+'</div></div>').join('');
}

/* ===== 审计层(每个数字的推导 + 为什么这么比) ===== */
function renderAudit(){
  const c=calc(),D=c.D;
  el('auditbox').innerHTML=
   '<h4>① 这份报告在比哪段时间</h4>'+
   '<ul><li>"上半年同比" = <span class="k">2026 年 2—6 月</span> 对比 <span class="k">2025 年 2—6 月</span>，共 5 个对照月。</li>'+
   '<li>缺 2025 年 1 月（去年数据不全），且不含 11—12 月旺季——所以是"淡季 5 个月"的方向性对比，别当精确定论。</li></ul>'+
   '<h4>② 头条数字怎么算的</h4>'+
   '<ul><li>大盘搜索同比 = 2026H1 '+fmtInt(c.sv26)+' ÷ 2025H1 '+fmtInt(c.sv25)+' − 1 = <span class="k">'+pctTxt(c.svYoY)+'</span></li>'+
   '<li>大盘成交同比 = '+fmtInt(c.od26)+' ÷ '+fmtInt(c.od25)+' − 1 = <span class="k">'+pctTxt(c.odYoY)+'</span></li>'+
   '<li>品牌成交同比 = '+fmtInt(c.my26)+' ÷ '+fmtInt(c.my25)+' − 1 = <span class="k">'+pctTxt(c.myYoY)+'</span></li>'+
   '<li>购买份额 = 品牌成交 ÷ 大盘成交（按每个词的体量加权）：'+c.sh25.toFixed(2)+'% → '+c.sh26.toFixed(2)+'%（'+ppTxt(c.shPP)+'）</li></ul>'+
   '<h4>③ "背离"到底是什么</h4>'+
   '<ul><li>市场转化率 = 大盘成交 ÷ 大盘搜索：2025H1 <span class="k">'+D.cvr25.toFixed(2)+'%</span> → 2026H1 <span class="k">'+D.cvr26.toFixed(2)+'%</span>（'+ppTxt(D.cvr_pp)+'）。</li>'+
   '<li>搜索涨、成交跌，本质是"每次搜索转成购买的比例"在下降——很可能是儿童等泛需求把搜索量灌高了，但这些人不买成人机。</li></ul>'+
   '<h4>④ +25% 该怎么看（为什么别过读）</h4>'+
   '<ul><li>+25% = 同期同比（2026H1 品牌 '+fmtInt(c.my26)+' ÷ 2025H1 '+fmtInt(c.my25)+'）。</li>'+
   '<li>同季逐月速度：2026H1 <span class="k">'+D.rr26+' 台/月</span> vs 2025H1 <span class="k">'+D.rr25+' 台/月</span> = 也是 +25%——说明不是虚高。</li>'+
   '<li>但 2025 上半年是品牌爬坡期、基数低，+25% 有一部分来自低基数；'+D.rr26+' 台/月仍是淡季速度，旺季目标要更高。</li>'+
   '<li>⚠ 注意别踩的坑：不要拿 2026 淡季的 '+D.rr26+' 台/月 去比 2025 下半年（旺季前爬坡）的更高速度——那是不同季节，会假显"萎缩"。同季比才对。</li></ul>'+
   '<h4>⑤ 季节峰值倍数（同年口径）</h4>'+
   '<ul><li>2025 年 12 月 ÷ 2025 上半年月均 = 搜索 <span class="k">'+D.decSvX.toFixed(2)+'×</span>、成交 <span class="k">'+D.decOdX.toFixed(2)+'×</span>。分子分母同年（勿用今年上半年做分母，会算出不同的倍数）。</li></ul>'+
   '<h4>⑥ 这个对比可靠吗（篮子覆盖率）</h4>'+
   '<ul><li>SQP 每月上榜的关键词会换血，跨月直接相加有风险。这份上半年同比落在<span class="k">稳定篮子</span>上：<span class="k">'+D.basket.stable_n+' 个核心词</span>在两年的 2—6 月都稳定出现，覆盖了 2026 上半年成交的 <span class="k">'+D.basket.cov_pct+'%</span>——所以对比可靠，换血主要影响长尾（约 '+(100-D.basket.cov_pct).toFixed(1)+'% 成交）。</li></ul>';
}

function rerenderAll(){ renderBasis(); renderHeadline(); renderKpis(); renderCharts(); renderActs(); renderAudit();
  el('foot').innerHTML='<b>口径说明。</b>'+T('份额','品牌捕获量÷全市场量')+'＝品牌卖出 ÷ 全市场卖出（按词体量加权）；<b>核心整机</b>＝含 karaoke 词根（含错拼，并入 singing machine／ktv）、剔除麦克风等配件词，<b>宽口径</b>＝全部相关词。同比只有 2026 年 2—6 月能对上 2025 同月（缺 2025-01），不含 11—12 月旺季，方向性看待。稳定篮子覆盖 2026 上半年成交约 '+calc().D.basket.cov_pct+'%。切换上方"市场口径"，头条、图表、指标、审计层全部同步重算。'; }
function init(){
  el('rng').textContent = MONTHS[0]+' ~ '+MONTHS[MONTHS.length-1];
  el('segUni').querySelectorAll('button').forEach(b=> b.onclick=()=>{
    S.uni=b.dataset.v; el('segUni').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b)); rerenderAll();
  });
  rerenderAll();
  window.addEventListener('resize',()=>Object.values(charts).forEach(c=>c.resize()));
}
init();
</script>
</body>
</html>
'''

HTML = HTML.replace('__Q1DATA__', json.dumps(Q1, ensure_ascii=False, separators=(',',':')))
io.open(OUT,'w',encoding='utf-8').write(HTML)
print('written', OUT, 'bytes', os.path.getsize(OUT))
