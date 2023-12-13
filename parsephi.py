'''
SELECT ATTRIBUTE(S):
cust, prod, avg(quant), max(quant) 
NUMBER OF GROUPING VARIABLES(n):
0
GROUPING ATTRIBUTES(V):
cust, prod
F-VECT([F]):
1_avg_quant, 1_max_quant
SELECT CONDITION-VECT([o]):
year=2009
HAVING_CONDITION(G):
NONE
phi_operator = {
    'select' : [cust, count(ny.quant), sum(nj.quant), max(ct.quant)],
    'no_group_var' : 3,
    'group_attribute' : 'cust',
    'agg_functions' : [count(ny.quant), sum(nj.quant), max(ct.quant), avg(ny.quant)],
    'predicates' : [ny.cust = cust, ny.state = 'NY', ...],
    'having': []
}
'''

# query = open("simpleinput.txt", "r")

def parse_phi():
    query = open("simpleinput.txt", "r")
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
print(parse_phi())
# query.close()