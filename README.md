### Víctor Cabré
# LP Practice 2023-2024 Q1: PandaQ

PandaQ is a SQL interpreter based on Pandas. The interpreter offers a simple web interface, through which you can make queries and visualize the results.

## How to run PandaQ?
1. To run, you must have Streamlit, Pandas and ANTLR4 installed. You can do this using the following commands:
`pip install streamlit`, `pip install pandas`, `pip install antlr4-tool`, `pip install antlr4-python3-runtime`

2. Make sure you have unzipped `pandaQ.py` and `pandaQ.g4` to the same directory.

3. Then, generate the Parser and Lexer from the `pandaQ.g4` file. You can do this with the following command:
`antlr4 -Dlanguage=Python3 -no-listener -visitor pandaQ.g4`

4. Create a folder inside the directory and name it `data`. You can do this with `mkdir data`.

5. Put the CSV files inside the `data` folder

6. Run the program with Streamlit: `streamlit run pandaQ.py`

## How do I use the program?

The graphical interface has a main element, a text box where you can write your _queries_. You can chain several _statements_ within the same _query_.

For example, you can do:

select * from countries;

Also:

q := select first_name, last_name, job_title, department_name from
employees inner join departments on department_id=department_id
inner join jobs on job_id=job_id;

select first_name, last_name from q;

To submit the query, click anywhere outside the text box or press Ctrl+Enter. The result will appear just below the text box. If there is more than one result, they will appear in chronological order.

## Features

#### Basic Queries

select * from countries;

select first_name, last_name from employees;

#### Calculated Fields

You can make queries using the operators +, -, *, / and parentheses. You can also use one or more columns within your calculated field.

select first_name, salary, salary * (1.05 + 3) as new_salary from employees;

select salary*(10 + job_id*(4+3)) as senseSentit from employees;

#### Order by

You can sort your queries in ascending or descending order, and using different columns. The leftmost columns have priority, the rightmost ones are used to break ties. If you do not specify 'asc' or 'desc', the default is to sort in ascending order, following the SQL standard.

select * from countries order by region_id, country_name desc;

#### Where

You can filter your queries. The following operators are supported: <, =, and, not, and parentheses.

select * from employees where not (employee_id < 5 and department_id = 5);

#### Inner join

You can chain multiple inner joins:

select first_name, last_name, job_title, department_name from employees
inner join departments on department_id=department_id
inner join jobs on job_id=job_id;

#### Symbol table and plots

You can save your queries in symbols:

table := select first_name, last_name, salary, salary*1.05 as new_salary from employees where department_id = 5;

And make a graph of the result:

plot table;

Only numeric columns are plotted.

#### Subqueries

You can make queries within other queries:

select employee_id, first_name, last_name from employees where
department_id in (select department_id from departments where
location_id = 1700) order by first_name, last_name;
