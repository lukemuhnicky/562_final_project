import re


def having_clause_to_py(input_str):
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
        if word in operators:
            words[i] = operators[word]
        # Replace patterns like '1_sum_quant' with 'groupby[cust_key]['1_sum_quant']'
        elif re.match(r'\d+_[a-zA-Z_]+', word):
            words[i] = f"groupby[grouping_attr_key]['{word}']"
    return f'''if {' '.join(words)}:'''



def update_agg_value(agg_table, grouping_variable, row):
    for func in agg_table:
        starting_val = agg_table[func]
        func_args = func.split('_')
        func_grouping_val = int(func_args[0])
        tracked_val = func_args[2]
        new_value = row[tracked_val]
        
        if (func_grouping_val != grouping_variable):
            continue
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
            raise Exception("Invalid aggregate function. You are a buffoon.")
            pass
        agg_table[func] = starting_val


def grouping_attr_to_py(grouping_attrs):
    result_string = ""
    if len(grouping_attrs) == 1:
        return f"row['{grouping_attrs[0]}']"
    else:
        for index, grouping_attr in enumerate(grouping_attrs):
            if index == len(grouping_attrs) - 1:
                result_string += f"row['{grouping_attr}']"
            else:
                result_string += f'''row['{grouping_attr}'] + "," +'''
    return result_string


def add_to_groupby(agg_funcs, indentation_level):
    indent = "\t" * indentation_level
    result_string = ""
    for agg_func in agg_funcs:
        if 'avg' in agg_func:
            result_string += f''' '{agg_func}' : [0,0],\n{indent}'''
        elif 'min' in agg_func:
            result_string += f''' '{agg_func}' : float('inf'),\n0{indent}'''
        elif 'max' in agg_func:
            result_string += f''' '{agg_func}' : float('-1'),\n{indent}'''
        else:
            result_string += f''' '{agg_func}' : 0,\n{indent}'''
    return result_string


'''
year = 2018
'''

def predicates_to_dict(predicate_list):
    result_dict = {}

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
        for i, word in enumerate(predicate):
            if word in operators:
                predicate[i] = operators[word]
            # Replace patterns like '1_sum_quant' with 'groupby[cust_key]['1_sum_quant']'
            elif re.match(r'\d+.[a-zA-Z_]+', word):
                grouping_var = int(word[0])
                predicate[i] = f"row['{word[2:]}']"
        if grouping_var not in result_dict:
            result_dict[grouping_var] = f'''if {' '.join(predicate)}:'''
    return result_dict

def where_clause_from_predicates_to_py(predicate_dict):
    if predicate_dict[0]:
        return predicate_dict[0]
    else:
        return 'if True:'
    
def predicate_clause_from_predicates_to_py(predicate_dict, indentation_level):
    indent = "\t" * indentation_level
    result_string = ""
    first_done = False
    for key in predicate_dict:
        if key == 0:
            continue
        elif first_done == False: 
            result_string += f'''{predicate_dict[key]}
{indent}\tgrouping_var = {key}\n'''
            first_done = True
        else:
            result_string += f'''{indent}el{predicate_dict[key]}
{indent}\tgrouping_var = {key}\n'''
    return result_string

def select_to_append_py(select_list, grouping_vars):
    print(select_list, grouping_vars)
    result_string = f''' '{','.join(grouping_vars)}': grouping_attr_key,'''
    for selection in select_list:
        if re.match(r'\d+_[a-zA-Z_]+', selection):
            result_string += f''''{selection}':groupby[grouping_attr_key]['{selection}'],'''
    return result_string