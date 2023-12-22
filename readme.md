# 562_final_project

This is our final project in CS 562 (Database Management Systems II). We implemeneted the basics of MF and EMF queries,
and a generator that writes them. Put your inputs in the \_input (or put them through the comand line) and you can see the
output files \_output.

Inputs MUST be in this form for MF
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
1_sum_quant > 2 \* 2_sum_quant or 1_avg_quant > 3_avg_quant

and like this for EMF
SELECT ATTRIBUTE(S):
cust, 1_sum_quant, 2_sum_quant
NUMBER OF GROUPING VARIABLES(n):
2
GROUPING ATTRIBUTES(V):
cust, prod
F-VECT([F]):
1_sum_quant, 2_sum_quant
SELECT CONDITION-VECT([o]):
0.year = 2017, 1.cust = cust and 2.prod = prod, 2.cust = cust and 2.prod <> prod
HAVING_CONDITION(G):
NONE

This project uses Python version 3.11.4, and requires pip for its packages. https://pip.pypa.io/en/stable/installation/
Once you have pip installed, you can install the requirements by using
pip install -r requirements.txt

Make sure you have a PostgreSQL database you can connect to, locally or a network, and change the values in the .env file
to the name, user, and password of the database. Then, run the createtable.sql query on your database to populate it with
the data we used for this project.

Then you can run the main.py file.
