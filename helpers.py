def where_to_python(where_clause):
    #input is like year=2009
    """
    Takes a where clause and converts it to python code
    """
    operators = {
        '=': '==',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>='
    }
    where_clause = where_clause.split()
    print(where_clause)
    operator = operators[where_clause[1]]
    return f"if row['{where_clause[0]}'] {operator} {where_clause[2]}:"