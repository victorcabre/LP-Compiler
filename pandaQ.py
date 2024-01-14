from antlr4 import *
from pandaQLexer import pandaQLexer
from pandaQParser import pandaQParser
from pandaQVisitor import pandaQVisitor

import streamlit as st
import pandas as pd

from operator import add, sub, mul, truediv

# Streamlit components

st.subheader("Víctor Cabré Guerrero")
st.title("PandaQ")  

query = st.text_area("Query:", value="select * from countries where not region_id=1 and not region_id=3;")


def load_table(name):
    # Load table
    try:
        df = pd.read_csv("data/" + name + ".csv")
        return df
    except:
        st.error("Table \"" + name + "\" not found.")


# ANTLR visitor

class EvalVisitor(pandaQVisitor):
    def __init__(self):
        super().__init__()
        self.is_subquery = False

    # SELECT fields FROM table
    def visitSelect(self, ctx):
        # args has optional arguments (order, where, join)
        [_, ids, _, table, *args] = ctx.getChildren()

        # Load table: first check if it's in symbol table, otherwise load from csv
        if table.getText() in st.session_state:
            self.data = st.session_state[table.getText()].copy()
        else:
            self.data = load_table(table.getText())
            if self.data is None: return
        
        self.df = pd.DataFrame()        

        # process argument "inner join"
        for arg in args:
            if "inner join" in arg.getText():
                self.visit(arg)

        # Display table with all columns or specific columns
        if (ids.getText() == "*"):
            self.df = self.data
        else:
            self.visit(ids)
        
        # process extra arguments (order and where)
        for arg in args:
            if "inner join" not in arg.getText():
                self.visit(arg)
        
        if (not self.is_subquery):
            st.write("Result:", self.df)

        self.is_subquery = False


    def visitIdentifier(self, ctx):
        [id] = ctx.getChildren()
        return id.getText()
    
    def visitColumnList(self, ctx):
        #Check that column names are in dataframe
        for token in ctx.getChildren():
            if token.getText() != ',':
                # Visit every column (calculated or not)
                self.visit(token)
            

    def visitColumnName(self, ctx: pandaQParser.ColumnNameContext):
        columnName = ctx.getText()
        if (columnName not in self.data.columns):
            st.error("Error: Incorrect column name/s")
            return
        
        self.df[columnName] = self.data[columnName]

    # Calculated column functions

    def visitCalculatedColumn(self, ctx: pandaQParser.CalculatedColumnContext):
        [expr, _, columnName] = ctx.getChildren()
        
        self.df[columnName.getText()] = self.visit(expr)

    def visitOpBin(self, ctx: pandaQParser.OpBinContext):
        [expr1, operator, expr2] = ctx.getChildren()

        operators = {
                    '+': add,
                    '-': sub,
                    '*': mul,
                    '/': truediv
        }
        
        return operators[operator.getText()](self.visit(expr1), self.visit(expr2))
    
    def visitFloat(self, ctx: pandaQParser.FloatContext):
        return float(ctx.getText())
    
    def visitInt(self, ctx: pandaQParser.IntContext):
        return int(ctx.getText())

    def visitCalculatedName(self, ctx: pandaQParser.CalculatedNameContext):
        return self.data[ctx.getText()]
    

    # ORDER BY functions

    def visitOrder(self, ctx: pandaQParser.OrderContext):
        columnList = [] # List of column names
        ascDescList = [] # True if asc
        for child in ctx.getChildren():
            if child.getText() not in ['order by', ',']:
                columnName, ascDesc = self.visit(child)
                columnList.append(columnName)
                ascDescList.append(ascDesc)

        for column in columnList:
            if column not in self.df.columns:
                st.error(f"Incorrect column \"{column}\" in ORDER BY statement")
                return
            
        self.df = self.df.sort_values(axis=0, by=columnList, ascending=ascDescList)

    def visitOrderColumnAscDesc(self, ctx: pandaQParser.OrderColumnAscDescContext):
        if ctx.getChildCount() == 2:
            [column, order] = ctx.getChildren()
            return column.getText(), order.getText() == 'asc'
        else:
            [column] = ctx.getChildren()
            return column.getText(), True


    def visitWhereCond(self, ctx:pandaQParser.WhereCondContext):
        [_, cond] = ctx.getChildren()
        self.df = self.df.loc[self.visit(cond)]

    def visitOpBinBool(self, ctx: pandaQParser.OpBinBoolContext):
        operators = {
            '<': lambda x, y: x < y,
            '=': lambda x, y: x == y,
            'and': lambda x, y: x & y,
        }
        [expr1, operator, expr2] = ctx.getChildren()
        return operators[operator.getText()](self.visit(expr1), self.visit(expr2))

    def visitNameBool(self, ctx: pandaQParser.NameBoolContext):
        if ctx.getText() in self.df.columns:
            return self.df[ctx.getText()]
        elif ctx.getText() in self.data.columns:
            return self.data[ctx.getText()]
        else:
            return ctx.getText()

    def visitNotBool(self, ctx: pandaQParser.NotBoolContext):
        [_, expr] = ctx.getChildren()
        return ~self.visit(expr)

    def visitFloatBool(self, ctx: pandaQParser.FloatBoolContext):
        return float(ctx.getText())
    
    def visitIntBool(self, ctx: pandaQParser.IntBoolContext):
        return int(ctx.getText())
    


    def visitJoin(self, ctx: pandaQParser.JoinContext):
        [_, table, _, col1, _, col2] = ctx.getChildren()

        other_df = load_table(table.getText())
        self.data = pd.merge(self.data, other_df, left_on=col1.getText(), right_on=col2.getText(), how='inner')

    def visitAssignment(self, ctx: pandaQParser.AssignmentContext):
        [name, _, select] = ctx.getChildren()
        self.visit(select)
        st.session_state[name] = self.df.copy()

    def visitPlot(self, ctx:pandaQParser.PlotContext):
        [_, id] = ctx.getChildren()

        if id.getText() not in st.session_state:
            st.error(f"Table {id.getText()} is not in the symbol table.")
            return
        
        df = st.session_state[id]
        df_numeric = df.select_dtypes(exclude=['object'])
        st.line_chart(df_numeric)

    def visitWhereIn(self, ctx:pandaQParser.WhereInContext):
        [_, id, _, _, select, _] = ctx.getChildren()

        self.is_subquery = True
        
        # visit subquery statement and get result
        original_df = self.df.copy()
        original_data = self.data.copy()
        self.visit(select)

        subquery_df = self.df.copy()
        self.df = original_df
        self.data = original_data

        self.df = self.data[self.data[id.getText()].isin(subquery_df.iloc[:,0].tolist())][original_df.columns]


# Main script
input_stream = InputStream(query)
lexer = pandaQLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = pandaQParser(token_stream)
tree = parser.root()

if parser.getNumberOfSyntaxErrors() == 0:
    visitor = EvalVisitor()
    visitor.visit(tree)
    print(tree.toStringTree(recog=parser))
else:
    print(parser.getNumberOfSyntaxErrors(), 'syntax errors.')
    print(tree.toStringTree(recog=parser))
    st.error("Syntax error (make sure to use ';' at the end of a statement)")