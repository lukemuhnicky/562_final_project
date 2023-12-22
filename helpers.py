import re

'''
Names: Phillip Anerine and Luke Muhnicky
CWIDs: 10461808 and 10467004
'''


'''
This converts a having clause phi operator into Python code.
Input - Having clause from phi operator
Output - Generated Python code 
(ex: groupby[grouping_attr_key]['1_sum_quant'] > 2 * groupby[grouping_attr_key]['2_sum_quant'] or groupby[grouping_attr_key]['1_avg_quant'] > groupby[grouping_attr_key]['3_avg_quant'] )
'''

def having_clause_to_py(input_str):
    ## No input? Set to 'if True:' to signify no having clause. 
    if input_str == 'NONE':
        return 'if True:'
    
    operators = {
        '=': '==',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>='
    }
    words = input_str.split()
    for i, word in enumerate(words):
        # Convert to operators
        if word in operators:
            words[i] = operators[word]
        # Replace patterns like '1_sum_quant' with 'groupby[cust_key]['1_sum_quant']'
        elif re.match(r'\d+_[a-zA-Z_]+', word):
            words[i] = f"groupby[grouping_attr_key]['{word}']"
    return f'''if {' '.join(words)}:'''


'''
Given a groupby key, we update their corresponding aggregates for a certain row.
Input - groupby key, # grouping variable, row that needs to be changed.
Output - Nothing, it just updates the value.
'''

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

'''
Converts grouping attributes in the phi operator into Python code.
Input - Grouping attributes from the phi operator
Output - A result string that contains all the grouping attributes in Python format.
Ex: ["cust", "prod"] -> "str(row['cust']), str(row['prod'])"

'''

def grouping_attr_to_py(grouping_attrs):
    result_string = ""
    if len(grouping_attrs) == 1:
        ## Base case -> no comma needed
        return f"str(row['{grouping_attrs[0]}'])"
    else:
        for index, grouping_attr in enumerate(grouping_attrs):
            if index == len(grouping_attrs) - 1:
            ## Last grouping attribute? Close the string.
                result_string += f"str(row['{grouping_attr}'])"
            else:
            ## Otherwise, add the argument and comma and move on.
                result_string += f'''str(row['{grouping_attr}']) + "," +'''
    return result_string

'''
When we populate our groupby (essentially, our MFStruct), we add our initial values.
Input: aggregate functions and the indentation level (set to 4)
Output: The initial values of our groupby struct, indented properly!
'''


def add_to_groupby(agg_funcs, indentation_level):
    indent = "    " * indentation_level
    result_string = ""
    for agg_func in agg_funcs:
        ## First elem in array is the sum and the second is the count. Then, sum/count to produce the average.
        if 'avg' in agg_func:
            result_string += f''' '{agg_func}' : [0,0],\n{indent}'''
        ## Max value in Python. I sure hope no one purchased infinity values.
        elif 'min' in agg_func:
            result_string += f''' '{agg_func}' : float('inf'),\n{indent}'''
        elif 'max' in agg_func:
            result_string += f''' '{agg_func}' : float('-1'),\n{indent}'''
        ## For count and sum
        else:
            result_string += f''' '{agg_func}' : 0,\n{indent}'''
    return result_string


'''
year = 2018
'''

'''
Given a list of predicates, produces a dictionary with corresponding to Python code. 
Input - A list of predicates from the phi operator
Output - Corresponding dictionary

Example - 
{0: "if row['year'] == 2018"
 1: (...)}
'''

def predicates_to_dict(predicate_list):
    result_dict = {}

    # First, split by space
    for predicate in predicate_list:
        predicate = predicate.split(' ')
        operators = {
            '=': '==',
            '<>': '!=',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>='
        }
        grouping_var = 0
        # (Almost) similar process to the having clause
        for i, word in enumerate(predicate):
            if word in operators:
                predicate[i] = operators[word]
        # Use RegEx format for matching with predicates like '1.quant'
            elif re.match(r'\d+.[a-zA-Z_]+', word):
                grouping_var = int(word[0])
                predicate[i] = f"row['{word[2:]}']"
        # If the corresponding grouping variable is not in the dictionary, add it!
        if grouping_var not in result_dict:
            result_dict[grouping_var] = f'''if {' '.join(predicate)}:'''
    return result_dict

'''
Returns the 0 (where clause) predicate in the dictionary. Otherwise, it returns 'if True'
meaning there is no where clause.
'''
def where_clause_from_predicates_to_py(predicate_dict):
    if 0 in predicate_dict:
        return predicate_dict[0]
    else:
        return 'if True:'
    
'''
(FOR MF QUERIES ONLY) outputs the Python code for each predicate
Input - The predicate dictionary (ex: {1: 'if row['state'] == NJ and row['year'] == 2018}), indentation level for proper generation
Output - The generated string that will go through each predicate.

Example:
            if row['state'] == 'NJ' and row['year'] == 2018:
                grouping_var = 1
            elif row['state'] == 'CT' and row['year'] == 2018:
                grouping_var = 2
            elif row['state'] == 'NY' and row['year'] == 2018:
                grouping_var = 3
'''
    
def predicate_clause_from_predicates_to_py(predicate_dict, indentation_level):
    indent = "    " * indentation_level
    result_string = ""
    first_done = False
    for key in predicate_dict:
        ## 0 signifies the where clause or general aggregates without specific attributes, and it throws an error.
        if key == 0:
            continue
        ## First is just an if statement
        elif first_done == False: 
            result_string += f'''{predicate_dict[key]}
{indent}    grouping_var = {key}\n'''
            first_done = True
        else:
        ## Once the first is done, start adding elif statements.
            result_string += f'''{indent}el{predicate_dict[key]}
{indent}    grouping_var = {key}\n'''
    return result_string

'''
Given a select list and grouping variables, return the generated Python code that is used for _global.append()
Input - select list from the phi operator, grouping attributes from the phi operator
Output - The code that is used for _global.append()
Ex: 'cust': grouping_attr_key, '0_sum_quant': groupby[grouping_attr_key]['0_sum_quant'],'1_sum_quant': groupby[grouping_attr_key]['1_sum_quant']}
'''

def select_to_append_py(select_list, grouping_attrs):
    # The first attribute will always be the "groupby" key.
    result_string = f''' '{','.join(grouping_attrs)}': grouping_attr_key,'''
    for selection in select_list:
        if re.match(r'\d+_[a-zA-Z_]+', selection):
    # The rest of the values are in the multilevel groupby dictionary.
            result_string += f''''{selection}':groupby[grouping_attr_key]['{selection}'],'''
    return result_string

'''
(FOR EMF QUERIES ONLY) Given a list of group by attributes, converts it into Python code which will help for the EMF predicates.
Ex: item_cust = grouping_attrs[0]
    item_month = grouping_attrs[1]
'''

def attrs_to_items_py(group_by, indentation_level):
    indent = "    " * indentation_level
    result_string = ""
    ## Simple iteration
    for idx,attr in enumerate(group_by):
        result_string+=f'''item_{attr} = grouping_attrs[{idx}]\n{indent}'''
    return result_string

'''
(FOR EMF QUERIES ONLY) Second parameter for the emf_predicates_to_py function below
'''
def attrs_to_item_names(group_by):
    result_list = []
    for item in group_by: 
        result_list.append(f'''item_{item}''')
    return result_list

'''
(FOR EMF QUERIES ONLY) This code converts the EMF predicates to generated Python code.
Input - list of predicates from the phi operator, list of attrs_to_items, and the grouping variable.
Output - All the EMF predicates.
Example: if item_cust == row['cust'] and item_month < row['month']:
            grouping_var = 1
'''

def emf_predicates_to_py(predicate_list, attrs_to_items_py, grouping_var):
    # Case for case = 0
    if grouping_var == '0': 
        result_string = f'''if '''
        for idx, item in enumerate(attrs_to_items_py):
            result_string += f'''{item} == row['{item[5:]}']'''
            if not (idx == len(attrs_to_items_py) -1):
                result_string += ' and '
            else: 
                result_string += ':'
        return result_string
    # Account for additional operators
    else: 
        operators = {
        '=': '==',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>='
        }
        words = ""
        for predicates in predicate_list: 
            splitted = predicates.split()
            for word in splitted:
                if f'''{grouping_var}.''' in word:
                    words = predicates
                    break
        words = words.split()
        for i, word in enumerate(words):
            if word in operators:
                words[i] = operators[word]
            # Replace patterns like '1.cust' with item_cust
            elif re.match(r'\d+.[a-zA-Z_]+', word):
                parts = word.split('.')
                if parts[1] not in attrs_to_items_py:
                    words[i] = f'''row['{word[2:]}']'''
                else:
                    words[i] = f" item_{word[2:]} "
            # Replace non 1.cust and non 'and' words with row['cust']
            elif (word != 'and' and word != 'or'):
                for item in attrs_to_items_py:
                    if word in item:
                        words[i] = f" item_{word} "
                        break
                    

        return f'''if {' '.join(words)}:'''