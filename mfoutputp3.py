
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
        key = str(row['cust']) + "," +str(row['prod'])
        if key not in groupby:
            groupby[key] = {
                 '1_min_quant' : float('inf'),
                 '1_max_quant' : float('-1'),
                 '2_min_quant' : float('inf'),
                 '2_max_quant' : float('-1'),
                
            }
        else:
            pass        
    for row in data:
        grouping_attr = str(row['cust']) + "," +str(row['prod'])
        if True:
            grouping_var = 0 
            if row['year'] == 2018 and row['state'] == 'PA':
                grouping_var = 1
            elif row['year'] == 2018 and row['state'] == 'NJ':
                grouping_var = 2

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
        if groupby[grouping_attr_key]['1_min_quant'] > groupby[grouping_attr_key]['2_min_quant']:
            _global.append({ 'cust,prod': grouping_attr_key,'1_min_quant':groupby[grouping_attr_key]['1_min_quant'],'1_max_quant':groupby[grouping_attr_key]['1_max_quant'],'2_min_quant':groupby[grouping_attr_key]['2_min_quant'],'2_max_quant':groupby[grouping_attr_key]['2_max_quant'],})
        
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    