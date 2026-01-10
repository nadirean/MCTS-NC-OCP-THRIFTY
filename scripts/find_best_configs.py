import csv
mx_pps=(0,None)
mx_bq=(0,None)
with open('report/summary_by_config.csv','r',encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        mpps=float(row['mean_playouts_per_second'])
        mbq=float(row['mean_best_q'])
        if mpps>mx_pps[0]: mx_pps=(mpps,(row['n_trees'],row['n_playouts']))
        if mbq>mx_bq[0]: mx_bq=(mbq,(row['n_trees'],row['n_playouts']))
print('max mean playouts/s',mx_pps)
print('max mean best_q',mx_bq)
