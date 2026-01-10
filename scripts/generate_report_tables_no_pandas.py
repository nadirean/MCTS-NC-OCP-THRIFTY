import csv, os, math
os.makedirs('report/tables', exist_ok=True)
from collections import defaultdict
agg = defaultdict(lambda: {'playouts_per_second':[], 'best_q':[], 'count':0})
with open('results/ocp_thrifty_summary.csv','r',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (int(row['n_trees']), int(row['n_playouts']))
        try:
            pps = float(row['playouts_per_second'])
        except:
            pps = float('nan')
        try:
            bq = float(row['best_q'])
        except:
            bq = float('nan')
        agg[key]['playouts_per_second'].append(pps)
        agg[key]['best_q'].append(bq)
        agg[key]['count'] += 1
# write summary csv
with open('report/summary_by_config.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['n_trees','n_playouts','mean_playouts_per_second','std_playouts_per_second','mean_best_q','std_best_q','trials'])
    for k in sorted(agg.keys()):
        pps_list = agg[k]['playouts_per_second']
        bq_list = agg[k]['best_q']
        def mean_std(lst):
            lst2 = [x for x in lst if not (x!=x)]
            if not lst2:
                return (float('nan'), float('nan'))
            m = sum(lst2)/len(lst2)
            var = sum((x-m)**2 for x in lst2)/len(lst2) if len(lst2)>1 else 0.0
            return (m, math.sqrt(var))
        pmean, pstd = mean_std(pps_list)
        bmean, bstd = mean_std(bq_list)
        w.writerow([k[0], k[1], f"{pmean:.6f}", f"{pstd:.6f}", f"{bmean:.6f}", f"{bstd:.6f}", agg[k]['count']])
# Create LaTeX table snippet
with open('report/tables/summary_table.tex','w',encoding='utf-8') as f:
    f.write('% Auto-generated table: mean ± std for playouts/sec and best_q\n')
    f.write('\\begin{tabular}{rrrrr}\n')
    f.write('\\toprule\n')
    f.write('n_trees & n_playouts & playouts/s (mean $\\pm$ std) & best_q (mean $\\pm$ std) & trials\\\\\n')
    f.write('\\midrule\n')
    for k in sorted(agg.keys()):
        pmean, pstd = mean_std(agg[k]['playouts_per_second'])
        bmean, bstd = mean_std(agg[k]['best_q'])
        trials = agg[k]['count']
        f.write(f"{k[0]} & {k[1]} & {int(round(pmean))} $\\pm$ {int(round(pstd))} & {bmean:.4f} $\\pm$ {bstd:.4f} & {trials} \\\\n")
    f.write('\\bottomrule\n')
    f.write('\\end{tabular}\n')
print('Wrote report/summary_by_config.csv and report/tables/summary_table.tex (no pandas)')
