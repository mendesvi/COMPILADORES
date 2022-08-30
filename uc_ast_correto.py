import sys

def represent_node(obj, indent):
    def _repr(obj, indent, printed_set):
        """
        Get the representation of an object, with dedicated pprint-like format for lists.
        """
        if isinstance(obj, list):
            indent += 1
            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            return (
                "["
                + (sep.join((_repr(e, indent, printed_set) for e in obj)))
                + final_sep
                + "]"
            )
        elif isinstance(obj, Node):
            if obj in printed_set:
                return ""
            else:
                printed_set.add(obj)
            result = obj.__class__.__name__ + "("
            indent += len(obj.__class__.__name__) + 1
            attrs = []
            for name in obj.__slots__:
                if name == "bind":
                    continue
                value = getattr(obj, name)
                value_str = _repr(value, indent + len(name) + 1, printed_set)
                attrs.append(name + "=" + value_str)
            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            result += sep.join(attrs)
            result += ")"
            return result
        elif isinstance(obj, str):
            return obj
        else:
            return ""

    # avoid infinite recursion with printed_set
    printed_set = set()
    return _repr(obj, indent, printed_set)

class Node:
    """Abstract base class for AST nodes."""

    __slots__ = ("coord",)

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        """A sequence of all children that are Nodes"""
        pass

    attr_names = ()

    def __repr__(self):
        """Generates a python representation of the current node"""
        return represent_node(self, 0)

    def show(
        self,
        buf=sys.stdout,
        offset=0,
        attrnames=False,
        nodenames=False,
        showcoord=False,
        _my_node_name=None,
    ):
        """Pretty print the Node and all its attributes and children (recursively) to a buffer.
        buf:
            Open IO buffer into which the Node is printed.
        offset:
            Initial offset (amount of leading spaces)
        attrnames:
            True if you want to see the attribute names in name=value pairs. False to only see the values.
        nodenames:
            True if you want to see the actual node names within their parents.
        showcoord:
            Do you want the coordinates of each Node to be displayed.
        """
        lead = " " * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__ + " <" + _my_node_name + ">: ")
            inner_offset = len(self.__class__.__name__ + " <" + _my_node_name + ">: ")
        else:
            buf.write(lead + self.__class__.__name__ + ":")
            inner_offset = len(self.__class__.__name__ + ":")

        if self.attr_names:
            if attrnames:
                nvlist = [
                    (n, represent_node(getattr(self, n), offset+inner_offset+1+len(n)+1))
                    for n in self.attr_names
                    if getattr(self, n) is not None
                ]
                attrstr = ", ".join("%s=%s" % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ", ".join(
                    represent_node(v, offset + inner_offset + 1) for v in vlist
                )
            buf.write(" " + attrstr)

        if showcoord:
            if self.coord and self.coord.line != 0:
                buf.write(" %s" % self.coord)
        buf.write("\n")

        for (child_name, child) in self.children():
            child.show(buf, offset + 4, attrnames, nodenames, showcoord, child_name)

class ArrayDecl(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("type", "size",)

    def __init__(self, type, size, coord=None):
        super().__init__(coord)
        self.type = type
        self.size = size

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        if self.size is not None:
            nodelist.append(('size', self.size))
        return tuple(nodelist)



class ArrayRef(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("name", "subscript",)

    def __init__(self, name, subscript, coord=None):
        super().__init__(coord)
        self.name = name
        self.subscript = subscript

    def children(self):
        nodelist = []
        if self.name is not None:
            nodelist.append(('name', self.name))
        if self.subscript is not None:
            nodelist.append(('subscript', self.subscript))
        return tuple(nodelist)

class Assert(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("expr",)

    def __init__(self, expr, coord=None):
        super().__init__(coord)
        self.expr = expr

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

class Assignment(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("lvalue", "rvalue",)

    def __init__(self, lvalue, rvalue, coord=None):
        super().__init__(coord)
        self.lvalue = lvalue
        self.rvalue = rvalue

    def children(self):
        nodelist = []
        if self.lvalue is not None:
            nodelist.append(('lvalue', self.lvalue))
        if self.rvalue is not None:
            nodelist.append(('rvalue', self.rvalue))
        return tuple(nodelist)

class BinaryOp(Node):

    __slots__ = ("op", "left", "right",)

    def __init__(self, op, left, right, coord=None):
        super().__init__(coord)
        self.op = op
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.left is not None:
            nodelist.append(('left', self.left))
        if self.right is not None:
            nodelist.append(('right', self.right))
        return tuple(nodelist)

    attr_names = ("op",)

class Break(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ()

    def __init__(self, coord=None):
        super().__init__(coord)
       

    def children(self):
        nodelist = []
        
        return tuple(nodelist)

    

class Cast(Node):   #eu add esse

    __slots__ = ("type", "expr",)

    def __init__(self, type, expr, coord=None):
        super().__init__(coord)
        self.type = type
        self.expr = expr

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)
class Compound(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("dcls", "stmts")

    def __init__(self, dcls, stmts, coord=None):
        super().__init__(coord)
        self.dcls = dcls
        self.stmts = stmts

    def children(self):
        nodelist = []
        for i, child in enumerate(self.dcls or []):
            nodelist.append(('dcls[%d]' % i, child))
        for i, child in enumerate(self.stmts or []):
            nodelist.append(('stmts[%d]' % i, child))    
        return tuple(nodelist)



class Constant(Node):

    __slots__ = ("type", "value",)

    def __init__(self, type, value, coord=None):
        super().__init__(coord)
        self.type = type
        self.value = value

    def children(self):
        return ()

    attr_names = ("type", "value",)

class Decl(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("name", "type", "init",)

    def __init__(self, name, type, init, coord=None):
        super().__init__(coord)
        self.name = name
        self.type = type
        self.init = init

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        if self.init is not None:
            nodelist.append(('init', self.init))
        return tuple(nodelist)

    attr_names = ("name",)

class DeclList(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("decls", )

    def __init__(self, decls, coord=None):
        super().__init__(coord)
        self.decls = decls
        

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(('decls[%d]' % i, child))   
        return tuple(nodelist)
class EmptyStatement(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ()

    def __init__(self, coord=None):
        super().__init__(coord)
       

    def children(self):
        nodelist = []
        
        return tuple(nodelist)

class ExprList(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("exprs", )

    def __init__(self, exprs, coord=None):
        super().__init__(coord)
        self.exprs = exprs
        

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(('exprs[%d]' % i, child))   
        return tuple(nodelist)

class For(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("init", "cond", "next", "statements",)

    def __init__(self, init, cond, next, statements, coord=None):
        super().__init__(coord)
        self.init = init
        self.cond = cond
        self.next = next
        self.statements = statements

    def children(self):
        nodelist = []
        if self.init is not None:
            nodelist.append(('init', self.init))
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.next is not None:
            nodelist.append(('next', self.next))    
        if self.statements is not None:
            nodelist.append(('statements', self.statements))    
        return tuple(nodelist)

class FuncCall(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("name", "args",)

    def __init__(self, name, args, coord=None):
        super().__init__(coord)
        self.name = name
        self.args = args

    def children(self):
        nodelist = []
        if self.name is not None:
            nodelist.append(('name', self.name))
        if self.args is not None:
            nodelist.append(('args', self.args))
        return tuple(nodelist)

class FuncDecl(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("args", "type",)

    def __init__(self, args, type, coord=None):
        super().__init__(coord)
        self.args = args
        self.type = type

    def children(self):
        nodelist = []
        if self.args is not None:
            nodelist.append(('args', self.args))
        if self.type is not None:
            nodelist.append(('type', self.type))
        return tuple(nodelist)

class FuncDef(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("spec", "decl","param_decls", "statements")

    def __init__(self, spec, decl, param_decls, statements, coord=None):
        super().__init__(coord)
        self.spec = spec
        self.decl = decl
        self.param_decls = param_decls
        self.statements = statements

    def children(self):
        nodelist = []
        if self.spec is not None:
            nodelist.append(('spec', self.spec))
        if self.decl is not None:
            nodelist.append(('decl', self.decl))
        for i, child in enumerate(self.param_decls or []):
            nodelist.append(('param_decls[%d]' % i, child))   
        if self.statements is not None:
            nodelist.append(('statements', self.statements))      
        return tuple(nodelist)

class GlobalDecl(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("decls", )

    def __init__(self, decls, coord=None):
        super().__init__(coord)
        self.decls = decls
        

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(('decls[%d]' % i, child))   
        return tuple(nodelist)

class ID(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("name",)

    def __init__(self, name, coord=None):
        super().__init__(coord)
        self.name = name
        
    def children(self):
        nodelist = []
 
        return tuple(nodelist)

    attr_names = ("name",)


class If(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("cond", "if_statements", "else_statements",)

    def __init__(self, cond, if_statements, else_statements, coord=None):
        super().__init__(coord)
        self.cond = cond
        self.if_statements = if_statements
        self.else_statements = else_statements

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.if_statements is not None:
            nodelist.append(('if_statements', self.if_statements))
        if self.else_statements is not None:
            nodelist.append(('else_statements', self.else_statements))
        return tuple(nodelist)

class InitList(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("exprs", )

    def __init__(self, exprs, coord=None):
        super().__init__(coord)
        self.exprs = exprs
        

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(('exprs[%d]' % i, child))   
        return tuple(nodelist)

class ParamList(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("params", )

    def __init__(self, params, coord=None):
        super().__init__(coord)
        self.params = params
        

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(('params[%d]' % i, child))   
        return tuple(nodelist)


class Print(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("expr",)

    def __init__(self, expr, coord=None):
        super().__init__(coord)
        self.expr = expr

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

class Program(Node):

    __slots__ = ("gdecls",)

    def __init__(self, gdecls, coord=None):
        super().__init__(coord)
        self.gdecls = gdecls

    def children(self):
        nodelist = []
        for i, child in enumerate(self.gdecls or []):
            nodelist.append(('gdecls[%d]' % i, child))
        return tuple(nodelist)

class Read(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("expr",)

    def __init__(self, expr, coord=None):
        super().__init__(coord)
        self.expr = expr

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

class Return(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("expr",)

    def __init__(self, expr, coord=None):
        super().__init__(coord)
        self.expr = expr

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

class Type(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("name",)

    def __init__(self, name, coord=None):
        super().__init__(coord)
        self.name = name
        
    def children(self):
        nodelist = []
 
        return tuple(nodelist)

    attr_names = ("name",)


class VarDecl(Node):

    # <<< YOUR CODE HERE >>>
     # <<< YOUR CODE HERE >>>
    __slots__ = ("declname", "type",)

    def __init__(self, declname=None, type=None, coord=None):
        super().__init__(coord)
        self.declname = declname
        self.type = type

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        
        return tuple(nodelist)

   

class UnaryOp(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("op", "expr",)

    def __init__(self, op, expr, coord=None):
        super().__init__(coord)
        self.op = op
        self.expr = expr

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        
        return tuple(nodelist)

    attr_names = ("op",)

class While(Node):

    # <<< YOUR CODE HERE >>>
    __slots__ = ("cond", "statements",)

    def __init__(self, cond, statements, coord=None):
        super().__init__(coord)
        self.cond = cond
        self.statements = statements

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.statements is not None:
            nodelist.append(('statements', self.statements))
        return tuple(nodelist)
