import pandas as pd
import os
os.makedirs('report/tables', exist_ok=True)
df = pd.read_csv('results/ocp_thrifty_summary.csv')
summary = df.groupby(['n_trees','n_playouts']).agg(
    mean_playouts_per_second=('playouts_per_second','mean'),
    std_playouts_per_second=('playouts_per_second','std'),
    mean_best_q=('best_q','mean'),
    std_best_q=('best_q','std'),
    trials=('trial','count')
).reset_index().sort_values(['n_trees','n_playouts'])
summary.to_csv('report/summary_by_config.csv', index=False)
# Create LaTeX table snippet (tabular) with mean +/- std for playouts/sec and best_q
with open('report/tables/summary_table.tex','w',encoding='utf-8') as f:
    f.write('% Auto-generated table: mean ± std for playouts/sec and best_q\n')
    f.write('\\begin{tabular}{rrrrr}\n')
    f.write('\\toprule\n')
    f.write('n_trees & n_playouts & playouts/s (mean $\\pm$ std) & best_q (mean $\\pm$ std) & trials\\\\\n')
    f.write('\\midrule\n')
    for _,r in summary.iterrows():
        f.write(f"{int(r['n_trees'])} & {int(r['n_playouts'])} & {r['mean_playouts_per_second']:.0f} $\\pm$ {r['std_playouts_per_second']:.0f} & {r['mean_best_q']:.4f} $\\pm$ {r['std_best_q']:.4f} & {int(r['trials'])} \\\\n")
    f.write('\\bottomrule\n')
    f.write('\\end{tabular}\n')
print('Wrote report/summary_by_config.csv and report/tables/summary_table.tex')
