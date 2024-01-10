# Generated from exprs.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .exprsParser import exprsParser
else:
    from exprsParser import exprsParser

# This class defines a complete generic visitor for a parse tree produced by exprsParser.

class exprsVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by exprsParser#root.
    def visitRoot(self, ctx:exprsParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#assignacio.
    def visitAssignacio(self, ctx:exprsParser.AssignacioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#write.
    def visitWrite(self, ctx:exprsParser.WriteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#condicional.
    def visitCondicional(self, ctx:exprsParser.CondicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#numero.
    def visitNumero(self, ctx:exprsParser.NumeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#opBin.
    def visitOpBin(self, ctx:exprsParser.OpBinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exprsParser#variable.
    def visitVariable(self, ctx:exprsParser.VariableContext):
        return self.visitChildren(ctx)



del exprsParser