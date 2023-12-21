'''
example input:
SELECT ATTRIBUTE(S):
cust, 0_sum_quant, 1_sum_quant, 2_sum_quant, 3_sum_quant
NUMBER OF GROUPING VARIABLES(n):
3
GROUPING ATTRIBUTES(V):
cust
F-VECT([F]):
0_sum_quant, 1_avg_quant, 1_sum_quant, 2_sum_quant, 3_avg_quant, 3_sum_quant
SELECT CONDITION-VECT([o]):
0.year = 2018, 1.state = 'NY' and 1.year = 2018, 2.state = 'NJ' and 2.year = 2018, 3.state = 'CT' and 3.year = 2018
HAVING_CONDITION(G):
1_sum_quant > 2 * 2_sum_quant or 1_avg_quant > 3_avg_quant

example output:
phi_operator = {
    'select': ['cust', '1_sum_quant', '2_sum_quant', '3_sum_quant'], 
    'no_group_var': 3, 
    'group_attribute': ['cust'], 
    'agg_functions': ['1_avg_quant', '1_sum_quant', '2_sum_quant', '3_avg_quant', '3_sum_quant'], 
    'predicates': ["0.year = 2018", "1.state = 'NY' and 1.year = 2018", "2.state = 'NJ' and 2.year = 2018", "3.state = 'CT' and 3.year = 2018"], 
    'having': '1_sum_quant > 2 * 2_sum_quant or 1_avg_quant > 3_avg_quant'
}
'''


def parse_phi(file_location):
    query = open(file_location, "r")
    phi_operator = {
        'select': None,
        'no_group_var' : None, 
        'group_attribute': None,
        'agg_functions' : None,
        'predicates' : None,
        'having': None
    }
    # Iterates through a dictionary
    for attribute in phi_operator:
        query.readline() # Skips over each line
        raw_line = query.readline().strip()
        # phi_operator[attribute] = query.readline().strip()
        if attribute == 'no_group_var':
            phi_operator[attribute] = int(raw_line)
        elif attribute != 'having': 
            clauses = raw_line.split(',')
            for idx, item in enumerate(clauses):
                clauses[idx] = item.strip()
            phi_operator[attribute] = clauses
        else:
            phi_operator[attribute] = raw_line
    query.close()
    return phi_operator

# query = open("simpleinput.txt", "r")

# print(phi_operator)
# query.close()