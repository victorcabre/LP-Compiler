// Generated from /home/victor/Documents/LP/PracticaCompilador/exemple/exprs.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link exprsParser}.
 */
public interface exprsListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link exprsParser#root}.
	 * @param ctx the parse tree
	 */
	void enterRoot(exprsParser.RootContext ctx);
	/**
	 * Exit a parse tree produced by {@link exprsParser#root}.
	 * @param ctx the parse tree
	 */
	void exitRoot(exprsParser.RootContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignacio}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterAssignacio(exprsParser.AssignacioContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignacio}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitAssignacio(exprsParser.AssignacioContext ctx);
	/**
	 * Enter a parse tree produced by the {@code write}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterWrite(exprsParser.WriteContext ctx);
	/**
	 * Exit a parse tree produced by the {@code write}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitWrite(exprsParser.WriteContext ctx);
	/**
	 * Enter a parse tree produced by the {@code condicional}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterCondicional(exprsParser.CondicionalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code condicional}
	 * labeled alternative in {@link exprsParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitCondicional(exprsParser.CondicionalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numero}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumero(exprsParser.NumeroContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numero}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumero(exprsParser.NumeroContext ctx);
	/**
	 * Enter a parse tree produced by the {@code opBin}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterOpBin(exprsParser.OpBinContext ctx);
	/**
	 * Exit a parse tree produced by the {@code opBin}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitOpBin(exprsParser.OpBinContext ctx);
	/**
	 * Enter a parse tree produced by the {@code variable}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterVariable(exprsParser.VariableContext ctx);
	/**
	 * Exit a parse tree produced by the {@code variable}
	 * labeled alternative in {@link exprsParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitVariable(exprsParser.VariableContext ctx);
}