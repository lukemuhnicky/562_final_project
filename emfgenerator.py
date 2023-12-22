'''
Names: Phillip Anerine and Luke Muhnicky
CWIDs: 10461808 and 10467004
'''

'''
This is our generator for EMF queries. 
Unlike the MF queries, our logic closely mirrors what was provided on the PDF.
Same structure, but we incorporated more helper functions.

'''



import subprocess
from helpers import grouping_attr_to_py, add_to_groupby, predicates_to_dict, where_clause_from_predicates_to_py, predicate_clause_from_predicates_to_py, having_clause_to_py, select_to_append_py, attrs_to_items_py, emf_predicates_to_py, attrs_to_item_names
simple_input = """
SELECT ATTRIBUTE(S):
cust, prod, avg(quant), max(quant) 
NUMBER OF GROUPING VARIABLES(n):
0
GROUPING ATTRIBUTES(V):
cust, prod
F-VECT([F]):
1_avg_quant, 1_max_quant
SELECT CONDITION-VECT([o]):
year = 2009
HAVING_CONDITION(G):
NONE
"""

'''
simple phi looks like 
{
    'select': ['cust', 'prod', 'avg(quant)', 'max(quant)'], 
    'no_group_var': 0, 
    'group_attribute': ['cust', 'prod'], 
    'agg_functions': ['1_avg_quant', '1_max_quant'], 
    'predicates': ['year=2009'], 
    'having': 'NONE'
}
'''

# Parse the input in another file to get the phi structure

def generate_emf(phi, file_name):
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    #Destructureing the phi into variables that are easier for us

    #seperate the simple selections from the aggregates
    # simple_selections = [simple_phi for selection in simple_phi['select'] if '(' not in selection]
    # agg_selections = [simple_phi for selection in simple_phi['select'] if '(' in selection]

    selections = phi['select']
    group_by = phi['group_attribute']
    agg_functions = phi['agg_functions']


    '''
    simple phi looks like 
    {
        'select': ['cust', '1_sum_quant', '2_sum_quant', '3_sum_quant'], 
        'no_group_var': 3, 
        'group_attribute': ['cust'], 
        'agg_functions': ['1_avg_quant', '1_sum_quant', '2_sum_quant', '3_avg_quant', '3_sum_quant'], 
        'predicates': ["0.year = 2018", "1.state = 'NY' and 1.year = 2018", "2.state = 'NJ' and 2.year = 2018", "3.state = 'CT' and 3.year = 2018"], 
        'having': 'NONE'
    }
    '''
    #seperate the aggregates into their respective functions and generate the string
    no_grouping_vars = phi['no_group_var']
    grouping_vars = [f"{i+1}" for i in range(1,no_grouping_vars)]

    predicates_dict = predicates_to_dict(phi['predicates'])
    tracking_vars = set()
    for key in agg_functions:
        num = key.split('_')[0]
        tracking_vars.add(num)
    
    table_scans = ""
    tracking_vars = sorted(tracking_vars)
    # Number of loops = number of grouping variables.
    for num in tracking_vars:
        table_scans += f'''
    for row in data:
        grouping_attr = {grouping_attr_to_py(phi['group_attribute'])}
        {where_clause_from_predicates_to_py(predicates_dict)}
            for key in groupby:
                grouping_var = 0 
                grouping_attrs = key.split(',')
                for item in grouping_attrs:
                    if item.isnumeric():
                        grouping_attrs[grouping_attrs.index(item)] = int(item)
                # Generated code as seen in helper.py methods.
                {attrs_to_items_py(group_by, 4)}
                {emf_predicates_to_py(phi['predicates'], attrs_to_item_names(group_by), num)}
                    grouping_var = {num}
                else:
                    continue
                change_group = groupby[key]
                update_agg_value(change_group, grouping_var, row)
            '''
    # Same process as before!
    body = f"""
    # Step 1: Gather unique "groupby"s (mf_struct)
    groupby = {{}}
    for row in data:
        key = {grouping_attr_to_py(phi['group_attribute'])}
        if key not in groupby:
            groupby[key] = {{
                {add_to_groupby(agg_functions, 4)}
            }}
        else:
            pass
    # Step 2: Instead of one pass, this is now based on the number of grouping variables.
    # Iterate through and check predicates.
    {table_scans}
    # Step 3: Revise averages, just like in an MF Query
    for grouping_attr_key, grouping_attr in groupby.items():
        for agg_func_key, agg_func in grouping_attr.items():
            if 'avg' in agg_func_key:
                avg_list = groupby[grouping_attr_key][agg_func_key]
                if avg_list[1] == 0:
                    groupby[grouping_attr_key][agg_func_key] = 0
                else:
                    groupby[grouping_attr_key][agg_func_key] = avg_list[0]/avg_list[1] 
    # Step 4: Filter out table using the having clause.
        {having_clause_to_py(phi['having'])}
            _global.append({{{select_to_append_py( selections, group_by )}}})
        """

    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def update_agg_value(agg_table, grouping_variable, row):
    # First, iterate through the aggregate functions.
    for func in agg_table:
        starting_val = agg_table[func]
        # Input is labeled as (ex: 1_avg_quant), so must account for that.
        func_args = func.split('_')
        func_grouping_val = int(func_args[0])
        tracked_val = func_args[2]
        new_value = row[tracked_val]
        
        # Do NOT update if the function grouping variable is not equivalent to the grouping variable.
        if (func_grouping_val != grouping_variable):
            continue
        # Note: avg is a pair, so you need to update the sum and the count before you divide at the end.
        if func_args[1] == 'avg':
            starting_val[0] += new_value
            starting_val[1] += 1
        elif func_args[1] == 'min':
            starting_val = min(new_value, starting_val)
        elif func_args[1] == 'max':
            starting_val = max(new_value, starting_val)
        elif func_args[1] == 'sum':
            starting_val += new_value
        elif func_args[1] == 'count':
            starting_val += 1
        else: 
            ## Should not occur!
            raise Exception("Invalid aggregate function.")
        # Finally, update the value. Done!
        agg_table[func] = starting_val

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
    {body}
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code
    open(f'_output/{file_name}.py', 'w').write(tmp)
    # Execute the generated code
    subprocess.run(["python", f'{file_name}.py'])