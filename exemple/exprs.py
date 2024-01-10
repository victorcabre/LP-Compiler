from antlr4 import *
from exprsLexer import exprsLexer
from exprsParser import exprsParser
from exprsVisitor import exprsVisitor
from operator import add, sub, mul, truediv, pow, eq, ne, gt, ge, lt, le




class TreeVisitor(exprsVisitor):
    def __init__(self):
        self.nivell = 0
    def visitSuma(self, ctx):
        [expressio1, operador, expressio2] = list(ctx.getChildren())
        print('  ' *  self.nivell + '+')
        self.nivell += 1
        self.visit(expressio1)
        self.visit(expressio2)
        self.nivell -= 1
    def visitResta(self, ctx):
        [expressio1, operador, expressio2] = list(ctx.getChildren())
        print('  ' *  self.nivell + '-')
        self.nivell += 1
        self.visit(expressio1)
        self.visit(expressio2)
        self.nivell -= 1
    def visitMultiplicacio(self, ctx):
        [expressio1, operador, expressio2] = list(ctx.getChildren())
        print('  ' *  self.nivell + '*')
        self.nivell += 1
        self.visit(expressio1)
        self.visit(expressio2)
        self.nivell -= 1
    def visitPotencia(self, ctx):
        [expressio1, operador, expressio2] = list(ctx.getChildren())
        print('  ' *  self.nivell + '^')
        self.nivell += 1
        self.visit(expressio1)
        self.visit(expressio2)
        self.nivell -= 1
    def visitNumero(self, ctx):
        [numero] = list(ctx.getChildren())
        print("  " * self.nivell + numero.getText())

class EvalVisitor(exprsVisitor):
    def __init__(self):
        self.vars = {}

    def int_wrapper(self, func):
        def wrapper(a, b):
            return 
        return wrapper

    def visitOpBin(self, ctx):
        operators = {
                    '+':add,
                    '-':sub,
                    '*':mul,
                    '/':truediv,
                    '^':pow,
                    '==':eq,
                    '!=':ne,
                    '>':gt,
                    '>=':ge,
                    '<':lt,
                    '<=':le,
                    }

        [expressio1, operador, expressio2] = list(ctx.getChildren())
        return operators[operador.getText()](self.visit(expressio1), self.visit(expressio2))
    def visitNumero(self, ctx):
        [numero] = list(ctx.getChildren())
        return int(numero.getText())
    def visitAssignacio(self, ctx):
        [var, _, expr] = ctx.getChildren()
        self.vars[var.getText()] = self.visit(expr)
    def visitVariable(self, ctx):
        [var] = ctx.getChildren()
        return self.vars[var.getText()]
    def visitWrite(self, ctx):
        [_, expr] = ctx.getChildren()
        print(self.visit(expr))
    def visitCondicional(self, ctx):
        [_, expr, _, statement, _] = ctx.getChildren()
        if self.visit(expr) != 0:
            self.visit(statement)
    

input_stream = StdinStream()
lexer = exprsLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = exprsParser(token_stream)
tree = parser.root()
if parser.getNumberOfSyntaxErrors() == 0:
    visitor = EvalVisitor()
    visitor.visit(tree)
else:
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))