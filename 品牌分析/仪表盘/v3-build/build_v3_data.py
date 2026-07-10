# -*- coding: utf-8 -*-
"""V3 DATA 管线:5 ASIN + 品牌视图 SQP CSV -> v3_data.json。分类规则见 doc 03。"""
import csv, glob, io, json, os, re

ROOT = r'C:\Users\EDY\Downloads\搜索查询绩效报告'
OUT  = r'C:\Users\EDY\AppData\Local\Temp\claude\D--nexgaios-amazon\3813589b-7399-4352-afc4-07c1ea4f4afb\scratchpad\v3_data.json'

# ---- 组合/父体/运营 元数据(领星核实) ----
ASINS = {
  'B0DHPN1DMJ': {'model':'Shell S2','parent':'B0F4QBR9SV','op':'毛香明'},
  'B0DCZQX11P': {'model':'Shell S1','parent':'B0DCZQX11P','op':'赵健宏'},
  'B0CR1R7FKP': {'model':'Break X2','parent':'B0DHZM8P16','op':'赵健宏'},
  'B0FNCQW2K3': {'model':'Shell S3','parent':'B0FWBJ9SNP','op':'毛香明'},
  'B0CLLT85Y6': {'model':'Break X1','parent':'B0DHZM8P16','op':'赵健宏'},
}
PARENTS = {
  'B0DHZM8P16': {'name':'Break/X 家族','op':'赵健宏','main_children':['B0CR1R7FKP','B0CLLT85Y6']},
  'B0F4QBR9SV': {'name':'Shell S2 家族','op':'毛香明','main_children':['B0DHPN1DMJ']},
  'B0DCZQX11P': {'name':'Shell S1','op':'赵健宏','main_children':['B0DCZQX11P']},
  'B0FWBJ9SNP': {'name':'Shell S3 家族','op':'毛香明','main_children':['B0FNCQW2K3']},
}

# ---- 运营组合逐月毛利(领星 profit_report,已核实,2025-08~2026-05) ----
# op -> month -> {gp:毛利润, sales:销售额含税}
PROFIT = {
 '赵健宏':{'2025-08':(41471.18,798660.85),'2025-09':(18369.90,687271.56),'2025-10':(80803.20,991898.87),
          '2025-11':(175565.94,1973706.30),'2025-12':(534266.27,4142908.75),'2026-01':(-101902.95,1081320.45),
          '2026-02':(68576.49,762016.56),'2026-03':(42837.22,669373.27),'2026-04':(62935.16,464778.67),'2026-05':(194751.07,825215.20)},
 '毛香明':{'2025-08':(-12793.65,455038.26),'2025-09':(-5807.11,373773.68),'2025-10':(-6261.20,442696.84),
          '2025-11':(20801.65,727766.42),'2025-12':(116535.48,1618281.52),'2026-01':(-43389.32,288342.92),
          '2026-02':(20614.34,216308.28),'2026-03':(3463.35,203581.82),'2026-04':(24414.72,193510.28),'2026-05':(75054.72,353998.47)},
}
COMMISSION_FLOOR = 7.0  # 月度提成线 %

# ---- 关键词分类(doc 03) ----
KARA = re.compile(r'karaoke|karoke|karokee|kareoke|kareokee|karioke|caraoke', re.I)
ALLOW = ('singing machine','sing machine','ktv')
def classify(kw):
    k = kw.lower()
    relevant = bool(KARA.search(k)) or any(a in k for a in ALLOW)
    if not relevant: return None            # 不相关 -> 剔除
    is_mic = ('mic' in k or 'microphone' in k) and not ('machine' in k or 'system' in k)
    return 'mic' if is_mic else 'core'      # 配件 / 整机

def num(x):
    x = (x or '').strip().strip('"').replace(',','')
    if x in ('','-','—','N/A'): return 0.0
    try: return float(x)
    except: return 0.0

def read_csv(path):
    rows = list(csv.reader(io.open(path, encoding='utf-8-sig')))
    return rows[2:]  # 跳过 第1行元数据 + 第2行列名

def month_of(path):
    m = re.search(r'Month_(\d{4})_(\d{2})_\d{2}', path)
    return '%s-%s' % (m.group(1), m.group(2))

# 列映射(品牌/ASIN 同位): sv=2, mkt_imp=3,my_imp=4, mkt_clk=6,my_clk=8, mkt_atc=15,my_atc=17, mkt_ord=24,my_ord=26
# share: imp=5,clk=9,atc=18,ord=27 ; price: 大盘购买中位=28, 自己购买中位=29
C = dict(sv=2, mkt_imp=3,my_imp=4,imp_sh=5, mkt_clk=6,clk_rt=7,my_clk=8,clk_sh=9,
         mkt_atc=15,atc_rt=16,my_atc=17,atc_sh=18, mkt_ord=24,ord_rt=25,my_ord=26,ord_sh=27,
         pm=28, pmine=29)

def aggregate(rows):
    """返回 {core:{...}, wide:{...}} 聚合;并回传逐词(相关词)记录。"""
    out = {'core':None,'wide':None}
    n_all = len(rows); sv_all = sum(num(r[C['sv']]) for r in rows if r)
    for uni in ('core','wide'):
        acc = dict(mkt_sv=0,mkt_imp=0,my_imp=0,mkt_clk=0,my_clk=0,mkt_atc=0,my_atc=0,mkt_ord=0,my_ord=0,n_kw=0)
        for r in rows:
            if not r or len(r) < 30: continue
            cls = classify(r[C['sv']-2] if False else r[0])
            if cls is None: continue
            if uni=='core' and cls!='core': continue
            acc['n_kw'] += 1
            acc['mkt_sv']  += num(r[C['sv']])
            acc['mkt_imp'] += num(r[C['mkt_imp']]); acc['my_imp'] += num(r[C['my_imp']])
            acc['mkt_clk'] += num(r[C['mkt_clk']]); acc['my_clk'] += num(r[C['my_clk']])
            acc['mkt_atc'] += num(r[C['mkt_atc']]); acc['my_atc'] += num(r[C['my_atc']])
            acc['mkt_ord'] += num(r[C['mkt_ord']]); acc['my_ord'] += num(r[C['my_ord']])
        def sh(a,b): return round(a/b*100,4) if b else None
        acc['n_all']=n_all; acc['sv_all']=round(sv_all)
        acc['imp_share']=sh(acc['my_imp'],acc['mkt_imp']); acc['clk_share']=sh(acc['my_clk'],acc['mkt_clk'])
        acc['atc_share']=sh(acc['my_atc'],acc['mkt_atc']); acc['ord_share']=sh(acc['my_ord'],acc['mkt_ord'])
        acc['clk_rate']=sh(acc['mkt_clk'],acc['mkt_sv']); acc['atc_rate']=sh(acc['mkt_atc'],acc['mkt_sv']); acc['ord_rate']=sh(acc['mkt_ord'],acc['mkt_sv'])
        for k in ('mkt_sv','mkt_imp','my_imp','mkt_clk','my_clk','mkt_atc','my_atc','mkt_ord','my_ord'): acc[k]=round(acc[k])
        out[uni]=acc
    return out

def kw_series_row(r):
    return dict(sv=round(num(r[C['sv']])), od=round(num(r[C['mkt_ord']])),
                bi=num(r[C['imp_sh']]), bc=num(r[C['clk_sh']]), ba=num(r[C['atc_sh']]), bo=num(r[C['ord_sh']]),
                pm=num(r[C['pm']]) or None, pmine=num(r[C['pmine']]) or None)

# ---- 主流程 ----
DATA = {'meta':{}, 'aggregate':{'brand':{}, 'asin':{}}, 'keywords':[], 'asin_keywords':{}, 'profit':{}}

# 品牌视图
brand_files = sorted(glob.glob(os.path.join(ROOT,'IKARAO品牌视图','*.csv')))
months = []
kw_map = {}  # kw -> {cls, series}
for f in brand_files:
    mo = month_of(f); months.append(mo)
    rows = read_csv(f)
    DATA['aggregate']['brand'][mo] = aggregate(rows)
    for r in rows:
        if not r or len(r) < 30: continue
        cls = classify(r[0])
        if cls is None: continue
        e = kw_map.setdefault(r[0], {'kw':r[0],'cls':cls,'series':{}})
        e['series'][mo] = kw_series_row(r)
months = sorted(set(months))
DATA['keywords'] = list(kw_map.values())

# ASIN 视图
for asin in ASINS:
    files = sorted(glob.glob(os.path.join(ROOT, asin, '*.csv')))
    DATA['aggregate']['asin'][asin] = {}
    akw = {}
    for f in files:
        mo = month_of(f); rows = read_csv(f)
        DATA['aggregate']['asin'][asin][mo] = aggregate(rows)
        for r in rows:
            if not r or len(r) < 30: continue
            if classify(r[0]) is None: continue
            e = akw.setdefault(r[0], {'kw':r[0],'series':{}})
            e['series'][mo] = dict(sv=round(num(r[C['sv']])), od=round(num(r[C['mkt_ord']])),
                                   ai=num(r[C['imp_sh']]), ao=num(r[C['ord_sh']]),
                                   pm=num(r[C['pm']]) or None, pmine=num(r[C['pmine']]) or None)
    DATA['asin_keywords'][asin] = list(akw.values())

# 利润(运营组合逐月 + 派生)
prof = {'floor':COMMISSION_FLOOR, 'ops':{}}
for op, ms in PROFIT.items():
    om = {}
    for mo,(gp,sales) in ms.items():
        om[mo] = dict(gp=round(gp,2), sales=round(sales,2), margin=round(gp/sales*100,2) if sales else None)
    prof['ops'][op] = om
DATA['profit'] = prof

DATA['meta'] = dict(months=months, brand='Ikarao', asins=ASINS, parents=PARENTS,
                    note='份额=Σ捕获÷Σ大盘(量级加权);core=整机(karaoke词根含错拼∪{singing machine,ktv}−麦克风配件);wide=全部相关;price(pm/pmine)=col28/29 购买中位价(干净,逐词).')

with io.open(OUT,'w',encoding='utf-8') as fp:
    json.dump(DATA, fp, ensure_ascii=False, separators=(',',':'))

# ---- 校验:2026-06 品牌 ----
b = DATA['aggregate']['brand']['2026-06']
print('months:', len(months), months[0],'->',months[-1])
print('brand kw count:', len(DATA['keywords']))
print('2026-06 brand n_all=%d sv_all=%d' % (b['core']['n_all'], b['core']['sv_all']))
print('  core: n_kw=%d mkt_sv=%d ord_share=%.2f%%' % (b['core']['n_kw'], b['core']['mkt_sv'], b['core']['ord_share']))
print('  wide: n_kw=%d mkt_sv=%d ord_share=%.2f%%' % (b['wide']['n_kw'], b['wide']['mkt_sv'], b['wide']['ord_share']))
print('  wide占sv_all=%.2f%%' % (b['wide']['mkt_sv']/b['core']['sv_all']*100))
a = DATA['aggregate']['asin']['B0DHPN1DMJ']['2026-06']['core']
print('2026-06 S2 core: my_ord=%d ord_share=%.2f%%' % (a['my_ord'], a['ord_share']))
print('file size KB:', round(os.path.getsize(OUT)/1024))
for asin in ASINS: print('  asin', asin, 'months', len(DATA['aggregate']['asin'][asin]), 'kw', len(DATA['asin_keywords'][asin]))
