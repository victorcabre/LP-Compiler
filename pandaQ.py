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

query = st.text_input("Query:", value="select * from countries where region_id=2")


def load_table(name):
    # Load table
    try:
        df = pd.read_csv("data/" + name + ".csv")
        return df
    except:
        st.error("Table \"" + name + "\" not found.")


# ANTLR visitor

class EvalVisitor(pandaQVisitor):

    # SELECT fields FROM table (ORDER BY)? 
    def visitSelect(self, ctx):
        # args has optional arguments (order and where)
        [_, ids, _, table, *args] = ctx.getChildren()

        # Load table 
        self.data = load_table(table.getText())
        if self.data is None: return
        
        self.df = pd.DataFrame()

        # Display table with all columns or specific columns
        if (ids.getText() == "*"):
            self.df = self.data
        else:
            self.visit(ids)
        
        # process extra arguments (order and where)
        for arg in args:
            self.visit(arg)
        
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


    def visitWhere(self, ctx: pandaQParser.WhereContext):
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
        try:
            return self.data[ctx.getText()]
        except:
            return ctx.getText()

    def visitNotBool(self, ctx: pandaQParser.NotBoolContext):
        [_, expr] = ctx.getChildren()
        return ~self.visit(expr)

    def visitFloatBool(self, ctx: pandaQParser.FloatBoolContext):
        return float(ctx.getText())
    
    def visitIntBool(self, ctx: pandaQParser.IntBoolContext):
        return int(ctx.getText())


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