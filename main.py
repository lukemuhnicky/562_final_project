'''
Names: Phillip Anerine and Luke Muhnicky
CWIDs: 10461808 and 10467004
'''



'''
CS 562 Final Project 
Goal - Instead of using multiple levels of "group-by" expressions and aggregate functions,
condense it into a concise notation using the "such that" clause.
'''
import inquirer
import parsephi
from mfgenerator import generate_mf
from emfgenerator import generate_emf


'''
This is where the user can select which type of query to evaluate (MF/EMF) and the
the type of input (text file, manual input).

If the user chooses a text file, then they must provide the name of the text file and the .py file
they would like to write to.

Otherwise, they will be prompted to enter the phi operators.
'''

def main(): 
    print("Welcome to the ESQL generator!")
    print("Please select the type of query you would like to generate.")
    questions = [
        inquirer.List('query_type',
                        message="What type of query would you like to generate?",
                        choices=['MF', 'EMF'],
                ),
        inquirer.List('input_type',
                    message="What kind of input would you like to use?",
                    choices=['Text file', 'Manual input'],
        )
    ]
    
    answers = inquirer.prompt(questions)
    query_type = answers['query_type']
    input_type = answers['input_type']
    phi = {}
    if input_type == 'Text file':
        txt_file = input("Please enter the name of the text file (including .txt) you would like to use: ")
        phi = parsephi.parse_phi(txt_file)
    elif input_type == 'Manual input':
        select = []
        while True:
            sel = input("Please enter selections one by one, followed by an 'Enter.' Type 'done' when you are finished: ")
            if sel == 'done':
                break
            else:
                select.append(sel)
        no_group_var = 0 
        while True: 
            try: 
                no_group_var = int(input("Please enter the number of grouping variables you would like to use: "))
                break
            except ValueError:
                print("Please enter a valid number")
        group_by = []
        while True:
            group = input("Please enter the group by attributes one by one, separated by entering. Type 'done' when you are finished: ")
            if group == 'done':
                break
            else:
                group_by.append(group)
        agg_functions = []
        while True:
            agg = input("Please enter the aggregate functions one by one, separated by entering. Type 'done' when you are finished: ")
            if agg == 'done':
                break
            else:
                agg_functions.append(agg)
        predicates = []
        while True:
            pred = input("Please enter the predicates one by one, separated by entering. If a predicate has 'and' included, please keep it on the same line. Type 'done' when you are finished: ")
            if pred == 'done':
                break
            else:
                predicates.append(pred)

        having = input("Please enter the having clause: ")
        phi = {
            'select': select,
            'no_group_var': no_group_var,
            'group_attribute': group_by,
            'agg_functions': agg_functions,
            'predicates': predicates,
            'having': having
        }
    file_name = input("Please enter the name of the file you would like to save the generated code to: ")
    
    if query_type == 'MF':
        generate_mf(phi, file_name)
    elif query_type == 'EMF':
        generate_emf(phi, file_name)

main()