
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
                 '1_sum_quant' : 0,
                 '2_sum_quant' : 0,
                
            }
        else:
            pass   
    
    for row in data:
        grouping_attr = str(row['cust']) + "," +str(row['prod'])
        if row['year'] == 2017:
            for key in groupby:
                grouping_var = 0 
                grouping_attrs = key.split(',')
                for item in grouping_attrs:
                    if item.isnumeric():
                        grouping_attrs[grouping_attrs.index(item)] = int(item)
                item_cust = grouping_attrs[0]
                item_prod = grouping_attrs[1]
                
                if row['cust'] ==  item_cust  and row['prod'] ==  item_prod :
                    grouping_var = 1
                else:
                    continue
                change_group = groupby[key]
                update_agg_value(change_group, grouping_var, row)
            
    for row in data:
        grouping_attr = str(row['cust']) + "," +str(row['prod'])
        if row['year'] == 2017:
            for key in groupby:
                grouping_var = 0 
                grouping_attrs = key.split(',')
                for item in grouping_attrs:
                    if item.isnumeric():
                        grouping_attrs[grouping_attrs.index(item)] = int(item)
                item_cust = grouping_attrs[0]
                item_prod = grouping_attrs[1]
                
                if row['cust'] ==  item_cust  and row['prod'] !=  item_prod :
                    grouping_var = 2
                else:
                    continue
                change_group = groupby[key]
                update_agg_value(change_group, grouping_var, row)
            
    for grouping_attr_key, grouping_attr in groupby.items():
        for agg_func_key, agg_func in grouping_attr.items():
            if 'avg' in agg_func_key:
                avg_list = groupby[grouping_attr_key][agg_func_key]
                if avg_list[1] == 0:
                    groupby[grouping_attr_key][agg_func_key] = 0
                else:
                    groupby[grouping_attr_key][agg_func_key] = avg_list[0]/avg_list[1] 
        if True:
            _global.append({ 'cust,prod': grouping_attr_key,'1_sum_quant':groupby[grouping_attr_key]['1_sum_quant'],'2_sum_quant':groupby[grouping_attr_key]['2_sum_quant'],})
        
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    