import re
def where_to_python(where_clause):
    #input is like year = 2009
    operators = {
        '=': '==',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>='
    }
    where_clause = where_clause.split()
    operator = operators[where_clause[1]]
    return f"if row['{where_clause[0]}'] {operator} {where_clause[2]}:"


def having_to_python(input_str):
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
            words[i] = f"groupby[cust_key]['{word}']"
    return ' '.join(words)

print(having_to_python("1_sum_quant > 2 * 2_sum_quant or 1_avg_quant > 3_avg_quant"))

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
