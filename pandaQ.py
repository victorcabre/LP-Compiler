from antlr4 import *
from pandaQLexer import pandaQLexer
from pandaQParser import pandaQParser
from pandaQVisitor import pandaQVisitor

import streamlit as st
import pandas as pd
from pandaQVisitor import pandaQVisitor

from operator import add, sub, mul, truediv

# Streamlit components

st.subheader("Víctor Cabré Guerrero")
st.title("PandaQ")

query = st.text_input("Query:", value="select country_name, country_id, country_id as c from countries")


def load_table(name):
    # Load table
    try:
        df = pd.read_csv("data/" + name + ".csv")
        return df
    except:
        st.error("Table \"" + name + "\" not found.")


# ANTLR visitor

class EvalVisitor(pandaQVisitor):

    # SELECT fields FROM table
    def visitSelect(self, ctx):
        if ctx.getChildCount() == 5:
            [_, ids, _, table, order] = ctx.getChildren()
        else:
            [_, ids, _, table] = ctx.getChildren()
            order = None

        # Load table 
        self.data = load_table(table.getText())
        if self.data is None: return
        
        self.df = pd.DataFrame()

        # Display table with all columns or specific columns
        if (ids.getText() == "*"):
            self.df = self.data
        else:
            self.visit(ids)
        
        if order is not None:
            self.visit(order)
        
        st.write("Result:", self.df)


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


    def visitCalculatedColumn(self, ctx: pandaQParser.CalculatedColumnContext):
        [expr, _, columnName] = ctx.getChildren()
        
        self.df[columnName.getText()] = self.visit(expr)

    def visitOpBin(self, ctx: pandaQParser.OpBinContext):
        [expr1, operator, expr2] = ctx.getChildren()

        operators = {
                    '+':add,
                    '-':sub,
                    '*':mul,
                    '/':truediv
        }
        
        return operators[operator.getText()](self.visit(expr1), self.visit(expr2))
    
    def visitFloat(self, ctx: pandaQParser.FloatContext):
        return float(ctx.getText())
    
    def visitInt(self, ctx: pandaQParser.IntContext):
        return int(ctx.getText())

    def visitCalculatedName(self, ctx: pandaQParser.CalculatedNameContext):
        return self.data[ctx.getText()]
    
    def visitOrder(self, ctx: pandaQParser.OrderContext):
        if ctx.getChildCount() == 3:
            [_, column, order] = ctx.getChildren()
            asc = order.getText() == 'asc'
        else:
            [_, column] = ctx.getChildren()
            asc = True

        if column.getText() not in self.df.columns:
            st.error(f"Incorrect column \"{column.getText()}\" in ORDER BY statement")
            return
        
        if asc:
            self.df = self.df.sort_values(axis=0, by=column.getText(), ascending=True)
        else:
            self.df = self.df.sort_values(axis=0, by=column.getText(), ascending=False)
        
        
    
    

# Main script
input_stream = InputStream(query)
lexer = pandaQLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = pandaQParser(token_stream)
tree = parser.root()

if parser.getNumberOfSyntaxErrors() == 0:
    visitor = EvalVisitor()
    visitor.visit(tree)
else:
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))
    st.error("Syntax error.")