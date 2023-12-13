import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv

"""

select cust, prod, avg(quant), max(quant) 
from sales
where year=2009 
group by cust, prod

{
'select': ['cust', 'prod', 'avg(quant)', 'max(quant)'], 
'no_group_var': 0, 
'group_attribute': ['cust', 'prod'], 
'agg_functions': ['1_avg_quant', '1_max_quant'], 
'predicates': ['year=2009'], 
'having': ['NONE']
}
"""

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def query(phi_operator):
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []

    # Table Scan 1: Get the value of 
    for row in cur:
        if row['year'] == 2009:
            _global.append(row)


        # If grouping attribute is not in table, add it to _global
        # if (...):
        #   _global.append(row)




    for row in cur:
        if row['quant'] > 10:
            _global.append(row)
    