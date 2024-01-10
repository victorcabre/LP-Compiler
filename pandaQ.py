from antlr4 import *
from pandaQLexer import pandaQLexer
from pandaQParser import pandaQParser
from pandaQVisitor import pandaQVisitor

import streamlit as st
import pandas as pd
from pandaQVisitor import pandaQVisitor

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
        [_, ids, _, table] = ctx.getChildren()

        # Load table
        df = load_table(table.getText())
        if df is None: return
        
        # Display table with all columns or specific columns
        if (ids.getText() == "*"):
            st.write("Result:", df)
        else:
            columns = self.visit(ids)
            #Check that column names are in dataframe
            for column in columns:
                if (column not in df.columns):
                    st.error("Error: Incorrect column name/s")
                    return

            st.write("Result:", df[columns])
    
    def visitIdentifier(self, ctx):
        [id] = ctx.getChildren()
        return id.getText()
    
    def visitColumnList(self, ctx):
        list = []
        for token in ctx.getChildren():
            # if token.getText() != ',':
            #     list.append(token.getText())
            self.visit(token)
        return list
    

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