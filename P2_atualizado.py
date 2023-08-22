class UCParser(Parser):
    """A parser for the uC language."""

    # Get the token list from the lexer (required)
    tokens = UCLexer.tokens

    precedence = (
        ('left', 'ID'),       
        ('left', 'INT', 'VOID', 'CHAR', 'ASSERT', 'INT_CONST', 'CHAR_CONST','STRING_LITERAL'), 
        ('left', 'ELSE'), 
        ('left', 'FOR'),
        ('left', 'WHILE'),  
        ('left', 'BREAK'),
        ('left', 'READ', 'PRINT'),
        ('left', 'RPAREN', 'LPAREN', 'LBRACKET', 'RBRACKET'),
        ('left', 'LBRACE'),
        ('left', 'RBRACE'),
        ('right', 'NOT'),
        ('left', 'AND', 'OR'),
        ('left', 'EQ', 'NE'),
        ('nonassoc', 'LE', 'LT', 'GE', 'GT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'DIVIDE','TIMES', 'MOD'),
        ('right', 'EQUALS'),
        ('left', 'RETURN'),
        ('left', 'COMMA', 'SEMI')  
    )

    def __init__(self, error_func=lambda msg, x, y: print("Lexical error: %s at %d:%d" % (msg, x, y), file=sys.stdout)):
        """Create a new Parser.
        An error function for the lexer.
        """
        self.lexer = UCLexer(error_func)

    def parse(self, text, lineno=1, index=0):
        return super().parse(self.lexer.tokenize(text, lineno, index))

    # Internal auxiliary methods
    def _token_coord(self, p):
        return self.lexer._make_location(p)

    # Error handling rule
    def error(self, p):
        if p:
            if hasattr(p, 'lineno'):
                print("Error at line %d near the symbol %s " % (p.lineno, p.value))
            else:
                print("Error near the symbol %s" % p.value)
        else:
            print("Error at the end of input")

    # <program> ::= {<global_declaration>}+
    @_('global_declaration_list')
    def program(self, p):
        return ('program', p.global_declaration_list)

    @_('global_declaration { global_declaration }')
    def global_declaration_list(self, p):
        return [p.global_declaration0] + p.global_declaration1

    # <global_declaration> ::= <function_definition>
    #                        | <declaration>
    @_('function_definition')
    def global_declaration(self, p):
        return p.function_definition

    @_('declaration')
    def global_declaration(self, p):
        return ('global_decl', p.declaration)

    # <function_definition> ::= <type_specifier> <declarator> <compound_statement>
    # <<< YOUR CODE HERE >>>
    @_('type_specifier declarator compound_statement' )
    def function_definition(self, p):
        return ('func_def', (p.type_specifier, ('decl', p.declarator, None)), p.compound_statement )  #conferir


    # <type_specifier> ::= "void"
    #                    | "char"
    #                    | "int"
    # <<< YOUR CODE HERE >>>
    @_('VOID', 'CHAR', 'INT')
    def type_specifier(self, p):
        return ('type: %s @ %d:%d' % ((p[0],) + self._token_coord(p)))


    # <declarator> ::= <identifier>
    #                | <declarator> "[" {<constant_expression>}? "]"
    #                | <declarator> "(" {<parameter_list>}? ")"
    # <<< YOUR CODE HERE >>>

   # declarator = tuple('var_decl', tuple('id: ' + str(ID) + ' @ lineno:column'))
    #       | tuple('array_decl @ lineno:column', declarator, constant_expression)
     #      | tuple('func_decl @ lineno:column', declarator, parameter_list)

    @_('ID')
    def declarator(self, p):
        return ('var_decl', ('id: %s @ %d:%d' % ((p.ID,)+self._token_coord(p))))

    @_('declarator LBRACKET [ constant_expression ] RBRACKET')
    def declarator(self, p):
        return ('array_decl @ %d:%d' % self._token_coord(p), p.declarator, p.constant_expression)

    @_('declarator LPAREN [ parameter_list ] RPAREN')
    def declarator(self, p):
        return ('func_decl @ %d:%d' % self._token_coord(p), p.declarator, p.parameter_list)
    # <constant_expression> ::= <binary_expression>
    # <<< YOUR CODE HERE >>>
    @_('binary_expression')
    def constant_expression(self, p):
        return p.binary_expression
    # <binary_expression> ::= <unary_expression>
    #                       | <binary_expression>  "*"   <binary_expression>
    #                       | <binary_expression>  "/"   <binary_expression>
    #                       | <binary_expression>  "%"   <binary_expression>
    #                       | <binary_expression>  "+"   <binary_expression>
    #                       | <binary_expression>  "-"   <binary_expression>
    #                       | <binary_expression>  "<"   <binary_expression>
    #                       | <binary_expression>  "<="  <binary_expression>
    #                       | <binary_expression>  ">"   <binary_expression>
    #                       | <binary_expression>  ">="  <binary_expression>
    #                       | <binary_expression>  "=="  <binary_expression>
    #                       | <binary_expression>  "!="  <binary_expression>
    #                       | <binary_expression>  "&&"  <binary_expression>
    #                       | <binary_expression>  "||"  <binary_expression>
    # <<< YOUR CODE HERE >>>

    @_('unary_expression')
    def binary_expression(self, p):
        return p.unary_expression

    @_('binary_expression TIMES binary_expression',
       'binary_expression DIVIDE binary_expression',
       'binary_expression MOD binary_expression',
       'binary_expression PLUS binary_expression',
       'binary_expression MINUS binary_expression',
       'binary_expression LT binary_expression',
       'binary_expression LE binary_expression',
       'binary_expression GT binary_expression',
       'binary_expression GE binary_expression',
       'binary_expression EQ binary_expression',
       'binary_expression NE binary_expression',
       'binary_expression AND binary_expression',
       'binary_expression OR binary_expression')
    def binary_expression(self, p):
        return ('binary_op: %s @ %d:%d' % ((p[1],)+self._token_coord(p)), p.binary_expression0, p.binary_expression1)

    # <unary_expression> ::= <postfix_expression>
    #                      | <unary_operator> <unary_expression>
    # <<< YOUR CODE HERE >>>
               # unary_expression = postfix_expression
                # | tuple('unary_op: ' + str(unary_operator), unary_expression)

    @_('postfix_expression')
    def unary_expression(self, p):
        return p.postfix_expression

    @_('unary_operator unary_expression')
    def unary_expression(self, p):
        return ('unary_op: %s'% p.unary_operator, p.unary_expression)

    # <postfix_expression> ::= <primary_expression>
    #                        | <postfix_expression> "[" <expression> "]"
    #                        | <postfix_expression> "(" {<argument_expression>}? ")"
    # <<< YOUR CODE HERE >>>
               # postfix_expression = primary_expression
              #   | tuple('array_ref', postfix_expression, expression)
              #  | tuple('func_call', postfix_expression, argument_expression)
    @_('primary_expression')
    def postfix_expression(self, p):
        return p.primary_expression

    @_('postfix_expression LBRACKET expression RBRACKET')
    def postfix_expression(self, p):
        return ('array_ref', p.postfix_expression,p.expression)

    @_('postfix_expression LPAREN [ argument_expression ] RPAREN ')
    def postfix_expression(self, p):
        return ('func_call', p.postfix_expression, p.argument_expression)

    # <primary_expression> ::= <identifier>
    #                        | <constant>
    #                        | <string>
    #                        | "(" <expression> ")"
    # <<< YOUR CODE HERE >>>
              #  primary_expression = tuple('id: ' + str(ID) + ' @ lineno:column')
               #    | constant
                #   | tuple('constant: string, ' + str(STRING_LITERAL) + ' @ lineno:column')
                 #  | expression
    @_('ID')
    def primary_expression(self, p):
        return ('id: %s @ %d:%d' % ((p.ID,) + self._token_coord(p)))

    @_('constant')
    def primary_expression(self, p):
        return p.constant

    @_('STRING_LITERAL')
    def primary_expression(self, p):
        return ('constant: string, %s @ %d:%d' % ((p.STRING_LITERAL,) + self._token_coord(p)))

    @_('LPAREN expression RPAREN')
    def primary_expression(self, p):
        return p.expression
    # <constant> ::= <integer_constant>
    #              | <character_constant>
    # <<< YOUR CODE HERE >>>
      
    @_('INT_CONST')
    def constant(self, p):
        return ('constant: int, %s @ %d:%d' % ((p.INT_CONST,) + self._token_coord(p)))

    @_('CHAR_CONST')
    def constant(self, p):
        return ('constant: char, %s @ %d:%d' % ((p.CHAR_CONST,) + self._token_coord(p)))
    # <expression> ::= <assignment_expression>
    #                | <expression> "," <assignment_expression>
    # <<< YOUR CODE HERE >>>
    @_('expression2')
    def expression(self, p):
        return (p.expression2)
    @_('assignment_expression COMMA assignment_expression { COMMA assignment_expression }')
    def expression2(self, p):
        return ('expr_list', [p.assignment_expression0, p.assignment_expression1] + p.assignment_expression2)

    @_('assignment_expression')
    def expression2(self, p):
        return p.assignment_expression


                                      #################################################################### conferir at aqui ###################################################
    # <argument_expression> ::= <assignment_expression>
    #                         | <argument_expression> "," <assignment_expression>
    # <<< YOUR CODE HERE >>>
                ##########################################################################3conferir##########################################################################
    @_('argument_expression2')
    def argument_expression(self, p):
        return ( p.argument_expression2)
    @_('assignment_expression COMMA assignment_expression { COMMA assignment_expression }')
    def argument_expression2(self, p):
        return ('expr_list', [p.assignment_expression0, p.assignment_expression1] + p.assignment_expression2)
    @_('assignment_expression')
    def argument_expression2(self, p):
        return p.assignment_expression    
              #  argument_expression = assignment_expression
                 #   | tuple('expr_list', list(assignment_expression))

                #########################################################################CONFERIR ESSE TBM ############################################
    # <assignment_expression> ::= <binary_expression>
    #                           | <unary_expression> "=" <assignment_expression>
    # <<< YOUR CODE HERE >>>
    @_('binary_expression')
    def assignment_expression(self, p):
        return (p.binary_expression)

    @_('unary_expression EQUALS assignment_expression')
    def assignment_expression(self, p):
        return ('assign: = @ %d:%d' % self._token_coord(p), p.unary_expression, p.assignment_expression)


    # <unary_operator> ::= "+"
    #                    | "-"
    #                    | "!"
    # <<< YOUR CODE HERE >>>
    @_('PLUS')
    def unary_operator(self, p):
        return ('+ @ %d:%d' % self._token_coord(p))

    @_('MINUS')
    def unary_operator(self, p):
        return ('- @ %d:%d' % self._token_coord(p))

    @_('NOT')
    def unary_operator(self, p):
        return ('! @ %d:%d' % self._token_coord(p))


    # <parameter_list> ::= <parameter_declaration>
    #                    | <parameter_list> "," <parameter_declaration>
    # <<< YOUR CODE HERE >>> #########################################################CONFERIR#############################
    @_('parameter_list2')
    def parameter_list(self, p):
        return p.parameter_list2

    @_('parameter_declaration { COMMA parameter_declaration }')
    def parameter_list2(self, p):
        return ('param_list', [ p.parameter_declaration0 ] + p.parameter_declaration1)
       #######################################################################################CONFERIR ATE AQUI####################
    # <parameter_declaration> ::= <type_specifier> <declarator>
    # <<< YOUR CODE HERE >>>
    @_('type_specifier declarator')
    def parameter_declaration(self, p):
        return (p.type_specifier, ('decl', p.declarator, None))


    # <declaration> ::=  <type_specifier> {<init_declarator_list>}? ";"
    # <<< YOUR CODE HERE >>>
    @_('type_specifier [ init_declarator_list ] SEMI')
    def declaration(self, p):
        return (p.type_specifier, p.init_declarator_list)
    # <init_declarator_list> ::= <init_declarator>
    #                          | <init_declarator_list> "," <init_declarator>
    # <<< YOUR CODE HERE >>>
                ################################################################CONFERIR##############################
    @_('init_declarator_list2')
    def init_declarator_list(self, p):
        return (p.init_declarator_list2)

    @_('init_declarator { COMMA init_declarator }')
    def init_declarator_list2(self, p):
        return ([ p.init_declarator0 ]+ p.init_declarator1)
                #################################################################CONFERIR ATE AQUI##########################
    # <init_declarator> ::= <declarator>
    #                     | <declarator> "=" <initializer>
    # <<< YOUR CODE HERE >>>
    @_('declarator [ EQUALS initializer ]')
    def init_declarator(self, p):
        return ('decl', p.declarator, p.initializer)
    # <initializer> ::= <assignment_expression>
    #                 | "{" {<initializer_list>}? "}"
    #                 | "{" <initializer_list> , "}"
    # <<< YOUR CODE HERE >>>
    @_('assignment_expression')
    def initializer(self, p):
        return (p.assignment_expression)
    @_('LBRACE [ initializer_list ] RBRACE')
    def initializer(self, p):
        return (p.initializer_list)
    @_('LBRACE initializer_list "," RBRACE')
    def initializer(self, p):
        return (p.initializer_list)
    # <initializer_list> ::= <initializer>
    #                      | <initializer_list> "," <initializer>
    # <<< YOUR CODE HERE >>>
                ####################################CONFERIR###############
    @_('initializer_list2')
    def initializer_list(self, p):
        return (p.initializer_list2)

    @_('initializer {  COMMA initializer }')
    def initializer_list2(self, p):
        return ('init_list', [ p.initializer0 ] + p.initializer1)
        ##############################################CONFERIR ATE AQUI#########################
    # <compound_statement> ::= "{" {<declaration>}* {<statement>}* "}"
    # <<< YOUR CODE HERE >>>
    @_('LBRACE { declaration } { statement } RBRACE')
    def compound_statement(self, p):
        return ('compound @ %d:%d' % self._token_coord(p), p.declaration, p.statement)

    # <statement> ::= <expression_statement>
    #               | <compound_statement>
    #               | <selection_statement>
    #               | <iteration_statement>
    #               | <jump_statement>
    #               | <assert_statement>
    #               | <print_statement>
    #               | <read_statement>
    # <<< YOUR CODE HERE >>>
    @_('expression_statement', 'compound_statement', 'selection_statement', 'iteration_statement', 'jump_statement', 'assert_statement', 'print_statement', 'read_statement')
    def statement(self, p):
        return (p[0])
    # <expression_statement> ::= {<expression>}? ";"
    # <<< YOUR CODE HERE >>>
    @_('[ expression ] SEMI')
    def expression_statement(self, p):
        if p.expression is not None:
          return p.expression
        else:
          return ('empty_statement @ %d:%d' % self._token_coord(p))

    # <selection_statement> ::= "if" "(" <expression> ")" <statement>
    #                         | "if" "(" <expression> ")" <statement> "else" <statement>
    # <<< YOUR CODE HERE >>>
    @_('IF LPAREN expression RPAREN statement [ ELSE statement ]')
    def selection_statement(self, p):
        return ('if @ %d:%d' % self._token_coord(p), p.expression, p.statement0, p.statement1)
    # <iteration_statement> ::= "while" "(" <expression> ")" <statement>
    #                         | "for" "(" {<expression>}? ";" {<expression>}? ";" {<expression>}? ")" <statement>
    #                         | "for" "(" <declaration> {<expression>}? ";" {<expression>}? ")" <statement>
    # <<< YOUR CODE HERE >>>
    @_('WHILE LPAREN expression RPAREN statement')
    def iteration_statement(self, p):
        return ('while @ %d:%d' % self._token_coord(p), p.expression, p.statement)

    @_('FOR LPAREN [ expression ] SEMI [ expression ] SEMI [ expression ] RPAREN statement')
    def iteration_statement(self, p):
        return ('for @ %d:%d' % self._token_coord(p), p.expression0, p.expression1, p.expression2, p.statement)

    @_('FOR LPAREN declaration [ expression ] SEMI [ expression ] RPAREN statement')
    def iteration_statement(self, p):
        return ('for @ %d:%d' % self._token_coord(p), ('decl_list', p.declaration), p.expression0, p.expression1, p.statement)

    # <jump_statement> ::= "break" ";"
    #                    | "return" {<expression>}? ";"
    # <<< YOUR CODE HERE >>>
    @_('BREAK SEMI')
    def jump_statement(self, p):
        return ('break @ %d:%d' % self._token_coord(p))

    @_('RETURN [ expression ] SEMI')
    def jump_statement(self, p):
        return ('return @ %d:%d' % self._token_coord(p), p.expression)
    # <assert_statement> ::= "assert" <expression> ";"
    # <<< YOUR CODE HERE >>>
    @_('ASSERT expression SEMI')
    def assert_statement(self, p):
        return ('assert @ %d:%d' % self._token_coord(p), p.expression)

    # <print_statement> ::= "print" "(" {<expression>}? ")" ";"
    # <<< YOUR CODE HERE >>>
    @_('PRINT LPAREN [ expression ] RPAREN SEMI')
    def print_statement(self, p):
        return ('print @ %d:%d' % self._token_coord(p), p.expression)

    # <read_statement> ::= "read" "(" <argument_expression> ")" ";"
    # <<< YOUR CODE HERE >>>
    @_('READ LPAREN argument_expression RPAREN SEMI')
    def read_statement(self, p):
        return ('read @ %d:%d' % self._token_coord(p), p.argument_expression)
