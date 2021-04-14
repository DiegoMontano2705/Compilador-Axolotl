# Generated from teamplusplus.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .teamplusplusParser import teamplusplusParser
else:
    from teamplusplusParser import teamplusplusParser

# This class defines a complete generic visitor for a parse tree produced by teamplusplusParser.

class teamplusplusVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by teamplusplusParser#programa.
    def visitPrograma(self, ctx:teamplusplusParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#comentario.
    def visitComentario(self, ctx:teamplusplusParser.ComentarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#programaAux.
    def visitProgramaAux(self, ctx:teamplusplusParser.ProgramaAuxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#dec_vars.
    def visitDec_vars(self, ctx:teamplusplusParser.Dec_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#form_vars.
    def visitForm_vars(self, ctx:teamplusplusParser.Form_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#form_vars_aux.
    def visitForm_vars_aux(self, ctx:teamplusplusParser.Form_vars_auxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#clases.
    def visitClases(self, ctx:teamplusplusParser.ClasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#funciones.
    def visitFunciones(self, ctx:teamplusplusParser.FuncionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#tipo.
    def visitTipo(self, ctx:teamplusplusParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#tipo_simple.
    def visitTipo_simple(self, ctx:teamplusplusParser.Tipo_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#tipo_retorno.
    def visitTipo_retorno(self, ctx:teamplusplusParser.Tipo_retornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#parametros.
    def visitParametros(self, ctx:teamplusplusParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#tipo_compuesto.
    def visitTipo_compuesto(self, ctx:teamplusplusParser.Tipo_compuestoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#var.
    def visitVar(self, ctx:teamplusplusParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#asign_vars.
    def visitAsign_vars(self, ctx:teamplusplusParser.Asign_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#llamada_fun.
    def visitLlamada_fun(self, ctx:teamplusplusParser.Llamada_funContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#retorno_fun.
    def visitRetorno_fun(self, ctx:teamplusplusParser.Retorno_funContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#lectura.
    def visitLectura(self, ctx:teamplusplusParser.LecturaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#lecturaaux.
    def visitLecturaaux(self, ctx:teamplusplusParser.LecturaauxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#escritura.
    def visitEscritura(self, ctx:teamplusplusParser.EscrituraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#escrituraAux.
    def visitEscrituraAux(self, ctx:teamplusplusParser.EscrituraAuxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#decision.
    def visitDecision(self, ctx:teamplusplusParser.DecisionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#estatutosAux.
    def visitEstatutosAux(self, ctx:teamplusplusParser.EstatutosAuxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#rep_condicional.
    def visitRep_condicional(self, ctx:teamplusplusParser.Rep_condicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#rep_no_condicional.
    def visitRep_no_condicional(self, ctx:teamplusplusParser.Rep_no_condicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#estatutos.
    def visitEstatutos(self, ctx:teamplusplusParser.EstatutosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#exp.
    def visitExp(self, ctx:teamplusplusParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#m_exp.
    def visitM_exp(self, ctx:teamplusplusParser.M_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#t.
    def visitT(self, ctx:teamplusplusParser.TContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by teamplusplusParser#f.
    def visitF(self, ctx:teamplusplusParser.FContext):
        return self.visitChildren(ctx)



del teamplusplusParser