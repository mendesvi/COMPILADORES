class UCLexer(Lexer):
    """A lexer for the uC language."""

    def __init__(self, error_func):
        """Create a new Lexer.
        An error function. Will be called with an error
        message, line and column as arguments, in case of
        an error during lexing.
        """
        self.error_func = error_func
        
    # Reserved keywords
    keywords = {
        'assert': "ASSERT",
        'break': "BREAK",
        'char': "CHAR",
        'else': "ELSE",
        'for': "FOR",
        'if': "IF",
        'int': "INT",
        'print': "PRINT",
        'read': "READ",
        'return': "RETURN",
        'void': "VOID",
        'while': "WHILE",
    }

     # All the tokens recognized by the lexer
    tokens = tuple(keywords.values()) + (
        # Identifiers
        "ID",
        # constants
        "INT_CONST",
        "CHAR_CONST",
        "STRING_LITERAL",
        # Operators
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "MOD",
        "LE",
        "LT",
        "GE",
        "GT",
        "EQ",
        "NE",
        "OR",
        "AND",
        "NOT",
        # Assignment
        "EQUALS",
        # Delimeters
        "LPAREN",
        "RPAREN",  # ( )
        "LBRACKET",
        "RBRACKET",  # [ ]
        "LBRACE",
        "RBRACE",  # { }
        "COMMA",
        "SEMI",  # , ;
    )

    # String containing ignored characters (between tokens)
    ignore = ' \t'

    # Other ignored patterns
    ignore_newline = r'\n+'
    ignore_comment = r'(\/\*)[\s\S]*?(\*\/)|(\/\/).*\n'

    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INT_CONST = r'[0-9]+'
    CHAR_CONST = r'\'([^\\\n]|(\\.))*?\'' #Usando a ER <.*?> irá corresponder apenas '<a>' https://docs.python.org/pt-br/3/library/re.html
    # <<< YOUR CODE HERE >>>
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'\/(?!\*)' #nao pode ser asterisco em seguida se nao vira omentario
    MOD = r'%'
    EQUALS = r'\=(?!\=)'
    SEMI = r'[\;]'
    COMMA = r'[\,]'
    LPAREN = r'[\(]'
    RPAREN = r'[\)]'
    LBRACE = r'[\{]'
    RBRACE = r'[\}]'
    EQ = r'=='
    NE = r'!='   #!=
    LBRACKET = r'[\[]'
    RBRACKET = r'[\]]'
    STRING_LITERAL = r'\".*?[^\\]\"'
    LE = r'\<\=' #<=
    LT = r'\<'   #<
    GE = r'\>\=' #>=
    GT = r'\>'   #>
    error_string = r'\"[^\"]*?(?=\n)'
    error_comment = r'\/\*[^\/\*]*?\Z'
    error_char = r'\'.{2,}\'|\'[^\']*?(?=\n)'
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'\!'
    # Special cases
    def ID(self, t):
      t.type = self.keywords.get(t.value, "ID")
      return t

    # Define a rule so we can track line numbers
    def ignore_newline(self, t):
      self.lineno += len(t.value)
 
    def ignore_comment(self, t):
      self.lineno += t.value.count("\n")

    def find_tok_column(self, token):
        """Find the column of the token in its line."""
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0: last_cr = 0
        return token.index - last_cr + 1

    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.index += 1

    def _make_tok_location(self, token):
        return token.lineno, self.find_tok_column(token)

    # Error handling rule
    def error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg, t)
    #MINHA FUNCAO
    def error_string(self, t):
        msg = "Unterminated string literal"
        self._error(msg, t)
        
    def error_comment(self, t):
        msg = "Unterminated comment"
        self._error(msg, t)    
    def error_char(self, t):
        msg = "Unterminated character const"
        self._error(msg, t)    

    # Scanner (used only for test)
    def scan(self, text):
        output = ""
        for tok in self.tokenize(text):
            print(tok)
            output += str(tok) + "\n"
        return output
