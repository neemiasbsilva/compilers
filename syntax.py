from pip._internal import operations
from sly import Parser
from lexer import LexerAnalysis
from anytree import Node, RenderTree
from anytree.importer import JsonImporter

import json
importer = JsonImporter()
class Expr:
    pass


class Program(Expr):
    def __init__(self, ListDeclaration):
        self.ListDeclaration = ListDeclaration
# program = Node("Pro")
# list_decraration = Node("Ls Decl", parent=program)
# declaration = Node("Decl", parent=list_decraration)
# decl_variable = Node("Decl Var", parent=declaration)
# decl_function = Node("Decl Fun", parent=declaration)
# tipo = Node("Tipo", parent=decl_variable)
# parametro = Node("Params", parent=decl_function)
# lista_parametros = Node("Ls Params", parent=parametro)
# param = Node("Param", parent=lista_parametros)
# decl_composta = Node("Decl Comp", parent=decl_function)
# decl_locais = Node("Decl Loc", parent=decl_composta)
# lista_comandos = Node("Ls Coma", parent=decl_composta)
# comando = Node("Com", parent=lista_comandos)
# decl_expressao = Node("Decl Expr", parent=comando)
# decl_selecao = Node("Declaracao Selecao", parent=comando)
# decl_iteracao = Node("Decl It", parent = comando)
# decl_retorno = Node("Decl Ret", parent=comando)
# expressao = Node("Expr", parent=decl_expressao)
# variavel = Node("Var", parent=expressao)
# expr_simples = Node("Expr Sim", parent=expressao)
# op_relacional = Node("Op Re", parent=expr_simples)
# soma_expressao = Node("Soma Expr", parent=expr_simples)
# soma  = Node("Soma", parent=soma_expressao)
# termo = Node("Termo", parent=soma_expressao)
# mult = Node("Mult", parent=termo)
# fator = Node("Fator", parent=termo)
# ativacao = Node("Ati", parent=fator)
# argumentos = Node("Arg.", parent=ativacao)
# lista_argumentos = Node("Ls Arg", parent=argumentos)


class ListDeclaration(Expr):
    def __init__(self, decl_left, decl_right):
        self.decl_left = decl_left
        self.decl_right = decl_right


class Declaration(Expr):
    def __init__(self, decl):
        self.decl = decl


class ParserAnalysis(Parser):
    # Get token list from the lexer (required)
    tokens = LexerAnalysis.tokens

    operations = {
        '+': lambda x, y: x + y,
        '−': lambda x, y: x - y,
        '∗': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }

    # Grammar rules and actions
    @_('lista_declaracao')
    def programa(self, p):
        return ('Prog: ', p.lista_declaracao)

    @_(' ')
    def empty(self, p):
        pass

    @_('lista_declaracao declaracao')
    def lista_declaracao(self, p):
        return "List Decl: ", p[0], p[1]
    @_('declaracao')
    def lista_declaracao(self, p):
        return p[0]

    @_('declaracao_variaveis',
       'declaracao_funcoes')
    def declaracao(self, p):
        return 'Decl: ', p[0]

    @_('tipo ID "[" NUMBER "]" ";"')
    def declaracao_variaveis(self, p):
        return 'Decl Var: ', p[0], p[1], p[2], p[3], p[4], p[5]
    @_('tipo ID ";"')
    def declaracao_variaveis(self, p):
        return 'Decl Var: ', p[0], p[1], p[2]


    @_('INT', 'VOID')
    def tipo(self, p):
        return 'Tipo: ', p[0]

    @_('tipo ID "(" parametros ")" declaracao_composta')
    def declaracao_funcoes(self, p):
        return 'Decl Fun: ', p[0], p[1], p[2], p[3], p[4], p[5]

    @_('lista_parametros',
       'VOID')
    def parametros(self, p):
        return 'Parmetros: ', p[0]
    @_('lista_parametros "," param')
    def lista_parametros(self, p):
        return 'Ls Parametros: ', p[0], p[1], p[2]
    @_('param')
    def lista_parametros(self, p):
        return p[0]


    @_('tipo ID "[" "]"')
    def param(self, p):
        return 'Param: ', p[0], p[1], p[2]
    @_('tipo ID')
    def param(self, p):
        return 'Param: ', p[0], p[1]

    @_('"{" declaracoes_locais lista_comandos "}"')
    def declaracao_composta(self, p):
        return 'Decl Composta: ', p[0], p[1], p[2], p[3]

    @_('declaracoes_locais declaracao_variaveis')
    def declaracoes_locais(self, p):
        return 'Decl Locais: ', p[0]
    @_('empty')
    def declaracoes_locais(self, p):
        pass

    @_('lista_comandos comando')
    def lista_comandos(self, p):
        return 'Ls Comandos: ', p[0], p[1]
    @_('empty')
    def lista_comandos(self, p):
        pass

    @_('declaracao_expressao',
       'declaracao_composta',
       'declaracao_selecao',
       'declaracao_iteracao',
       'declaracao_retorno')
    def comando(self, p):
        return 'Comando: ',p[0]

    @_('expressao ";"')
    def declaracao_expressao(self, p):
        return 'Decl Expr: ', p[0], p[1]
    @_('";"')
    def declaracao_expressao(self, p):
        return 'Decl Expr: ', p[0]

    @_('IF "(" expressao ")" comando')
    def declaracao_selecao(self, p):
        return 'Decl Sel: ', p[0], p[1], p[2], p[3], p[4]

    @_('IF "(" expressao ")" comando ELSE comando')
    def declaracao_selecao(self, p):
        return 'Decl Sel: ', p[0], p[1], p[2], p[3], p[4]

    @_('WHILE "(" expressao ")" comando')
    def declaracao_iteracao(self, p):
        return 'Decl It: ', p[0], p[1], p[2], p[3], p[4]


    @_('RETURN expressao ";"')
    def declaracao_retorno(self, p):
        return 'Decl Ret: ', p[0], p[1], p[2]
    @_('RETURN ";"')
    def declaracao_retorno(self, p):
        return 'Decl Ret: ', p[0], p[1]


    @_('variavel ASSIGN expressao')
    def expressao(self, p):
        return 'Expr: ', p[0], p[1], p[2]

    @_('expressao_simples')
    def expressao(self, p):
        return 'Expr: ', p[0]

    @_('ID "[" expressao "]"')
    def variavel(self, p):
        return 'Var: ', p[0], p[1], p[2], p[3]
    @_('ID')
    def variavel(self, p):
        return 'Var: ', p[0]

    @_('soma_expressao op_relacional soma_expressao')
    def expressao_simples(self, p):
        return 'Expr Sim: ', p[0], p[1], p[2]

    @_('soma_expressao')
    def expressao_simples(self, p):
        return 'Expr Sim: ', p[0]

    @_('LE', 'LT', 'GE', 'GT', 'EQ', 'NE')
    def op_relacional(self, p):
        return 'Op Rel: ', p[0]

    @_('soma_expressao soma termo')
    def soma_expressao(self, p):
        return 'Som Expr: ', p[0], p[1], p[2]
    @_('termo')
    def soma_expressao(self, p):
        return p[0]

    @_('PLUS', 'MINUS')
    def soma(self, p):
        return p[0]

    @_('fator aux6')
    def termo(self, p):
        return p[0]
    @_('mult fator aux6')
    def aux6(self, p):
        return p[0], p[1]
    @_('empty')
    def aux6(self, p):
        pass


    @_('DIVIDE', 'TIMES')
    def mult(self, p):
        return 'Mult: ', p[0]

    @_('"(" expressao ")"')
    def fator(self, p):
        return p[0], p[1], p[2]

    @_('variavel', 'ativacao', 'NUMBER')
    def fator(self, p):
        return p[0]

    @_('ID "(" argumentos ")"')
    def ativacao(self, p):
        return 'Ativacao: ', p[0], p[1], p[2], p[3]

    @_('lista_argumentos', 'empty')
    def argumentos(self, p):
        return 'Arg: ', p[0]

    @_('expressao aux5')
    def lista_argumentos(self, p):
        return 'Ls Arg: ', p.expressao, p.aux5
    @_('"," expressao aux5')
    def aux5(self, p):
        return p[0], p[1]
    @_('empty')
    def aux5(self, p):
        pass


def main():
    lexer = LexerAnalysis()
    parser = ParserAnalysis()
    file = open('Inputs/sample.in', 'r')
    while True:
        try:
            data = str()
            for line in file:
                data += str(line)

        except EOFError:
            break
        if data:
            result = parser.parse(lexer.tokenize(data))
            #print(result)
            json_str = json.dumps(result, sort_keys=True, indent=2)
            f = open('Outputs/sample.out', 'w')
            f.write(str(json_str))
            f.close()
            break


if __name__ == '__main__':
    main()
    #for pre, fill, node in RenderTree(program):
    #    print("%s%s" % (pre, node.name))
