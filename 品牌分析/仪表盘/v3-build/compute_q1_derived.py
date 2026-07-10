# -*- coding: utf-8 -*-
"""算 Q1 派生口径:市场CVR、同季run-rate、同年季节倍数、Q4目标区间、稳定篮子覆盖率。
   并把 basket 覆盖率写进 q1_slice_data.json。"""
import json, io

D = json.load(io.open(r'C:\Users\EDY\AppData\Local\Temp\claude\D--nexgaios-amazon\3813589b-7399-4352-afc4-07c1ea4f4afb\scratchpad\v3_data.json', encoding='utf-8'))
SLICE = r'C:\Users\EDY\AppData\Local\Temp\claude\D--nexgaios-amazon\3813589b-7399-4352-afc4-07c1ea4f4afb\scratchpad\q1_slice_data.json'
bc = D['aggregate']['brand']
H1 = lambda yr: ['%d-%02d'%(yr,m) for m in range(2,7)]

def block(uni):
    def s(yr,f): return sum(bc[m][uni][f] for m in H1(yr) if m in bc)
    sv25,sv26 = s(2025,'mkt_sv'), s(2026,'mkt_sv')
    od25,od26 = s(2025,'mkt_ord'), s(2026,'mkt_ord')
    my25,my26 = s(2025,'my_ord'), s(2026,'my_ord')
    cvr25, cvr26 = od25/sv25*100, od26/sv26*100
    rr25, rr26 = my25/5, my26/5           # 同季 run-rate(2-6月)
    dec = bc['2025-12'][uni]
    decSvX = dec['mkt_sv']/(sv25/5); decOdX = dec['mkt_ord']/(od25/5)  # 同年:2025-12 ÷ 2025 H1均
    q4floor = bc['2025-11'][uni]['my_ord'] + bc['2025-12'][uni]['my_ord']
    q4target = q4floor*(my26/my25)        # 按 H1 增速外推
    return dict(cvr25=round(cvr25,2),cvr26=round(cvr26,2),cvr_pp=round(cvr26-cvr25,2),
                rr25=round(rr25),rr26=round(rr26),decSvX=round(decSvX,2),decOdX=round(decOdX,2),
                q4floor=round(q4floor),q4target=round(q4target))

# 稳定篮子覆盖率:core词在 2025H1 与 2026H1 各出现≥4/5月;覆盖 = 其 2026H1 大盘成交 / 全部core词 2026H1 大盘成交
def basket(uni):
    kws = D['keywords']
    want = (lambda e: True) if uni=='wide' else (lambda e: e['cls']=='core')
    def present(e, yr):
        return sum(1 for m in H1(yr) if m in e['series'])
    tot_od = 0.0; stable_od = 0.0; stable_n = 0; all_n = 0
    for e in kws:
        if not want(e): continue
        od26 = sum(e['series'][m]['od'] for m in H1(2026) if m in e['series'])
        if any(m in e['series'] for m in H1(2026)): all_n += 1
        tot_od += od26
        if present(e,2025)>=4 and present(e,2026)>=4:
            stable_od += od26; stable_n += 1
    return dict(stable_n=stable_n, all_n=all_n, cov_pct=round(stable_od/tot_od*100,1) if tot_od else 0)

out = {}
for uni in ('core','wide'):
    d = block(uni); b = basket(uni)
    out[uni] = {**d, 'basket':b}
    print(uni, '| CVR %.2f%%->%.2f%% (%.2fpp) | 同季run-rate %d->%d/月 | 季节倍数(同年) 搜%.2fx/成%.2fx | Q4 地板%d 目标≈%d | 稳定篮子 %d词 覆盖成交%.1f%%(全%d词)'
          % (d['cvr25'],d['cvr26'],d['cvr_pp'],d['rr25'],d['rr26'],d['decSvX'],d['decOdX'],d['q4floor'],d['q4target'],b['stable_n'],b['cov_pct'],b['all_n']))

# 写进 q1_slice_data(加 derived 块)
sl = json.load(io.open(SLICE, encoding='utf-8'))
sl['derived'] = out
io.open(SLICE,'w',encoding='utf-8').write(json.dumps(sl, ensure_ascii=False, separators=(',',':')))
print('q1_slice_data.json 已更新(加 derived 块)')
