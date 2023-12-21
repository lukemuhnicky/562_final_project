
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
from helpers import update_agg_value

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def query():
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    data = cur.fetchall()
    
    _global = []
    
    groupby = {}
    for row in data:
        key = str(row['cust'])
        if key not in groupby:
            groupby[key] = {
                 '0_sum_quant' : 0,
                 '1_avg_quant' : [0,0],
                 '2_sum_quant' : 0,
                 '3_sum_quant' : 0,
                
            }
        else:
            pass        
    for row in data:
        grouping_attr = str(row['cust'])
        if row['year'] == 2018:
            grouping_var = 0 
            if row['state'] == 'NY' and row['year'] == 2018:
                grouping_var = 1
            elif row['state'] == 'NJ' and row['year'] == 2018:
                grouping_var = 2
            elif row['state'] == 'CT' and row['year'] == 2018 :
                grouping_var = 3

        else:
            continue
        change_group = groupby[grouping_attr]
        update_agg_value(change_group, 0, row)
        if grouping_var != 0:
            update_agg_value(change_group, grouping_var, row)
            
            
    for grouping_attr_key, grouping_attr in groupby.items():
        for agg_func_key, agg_func in grouping_attr.items():
            if 'avg' in agg_func_key:
                avg_list = groupby[grouping_attr_key][agg_func_key]
                if avg_list[1] == 0:
                    groupby[grouping_attr_key][agg_func_key] = 0
                else:
                    groupby[grouping_attr_key][agg_func_key] = avg_list[0]/avg_list[1] 
        if groupby[grouping_attr_key]['1_sum_quant'] > 2 * groupby[grouping_attr_key]['2_sum_quant'] or groupby[grouping_attr_key]['1_avg_quant'] > groupby[grouping_attr_key]['3_avg_quant']:
            _global.append({ 'cust': grouping_attr_key,'0_sum_quant':groupby[grouping_attr_key]['0_sum_quant'],'1_sum_quant':groupby[grouping_attr_key]['1_sum_quant'],'2_sum_quant':groupby[grouping_attr_key]['2_sum_quant'],'3_sum_quant':groupby[grouping_attr_key]['3_sum_quant'],})
        
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    