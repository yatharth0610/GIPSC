from array import ArrayType
from tkinter import E
from typing import List
from numpy import iscomplexobj
import ply.yacc as yacc
import ply.lex as lex
import lexer
from lexer import *
import sys
# from scope import *
from scope import *
from utils import *

tokens=lexer.tokens
tokens.remove('COMMENT')
# tokens.append('MULTP')

precedence = (
    # ('left', 'CONV'),
# COMPACT = False
# def get_value_p(p):
#     value = [str(sys._getframe(1).f_code.co_name)[2:]]
#     # value = []
#     for i in range(1, len(p)):
#         if isinstance(p[i], str):
#             if p[i] in ignored_tokens:
#                 continue
#             if p[i] not in non_terminals:
#                 value.append([p[i]])
#         elif len(p[i]) > 0:
#             if COMPACT:
#                 if p[i][0] == value[0]:
#                     value.extend(p[i][1:])
#                 else:
#                     value.append(p[i])
#             else:
#                 value.append(p[i])
#     if not isinstance(value, str) and COMPACT:
#         if len(value) == 2:
#             return value[1]
#         if len(value) == 1:
#             return []
#         if len(value) > 2:
#             if value[0] == 'Expr':
#                 value = value[2] + [value[1]] + value[3:]
#             elif value[0] == 'UnaryExpr':
#                 value = value[1] + [value[2]]
#                 # print(value, value[2] + [value[1]] + value[3:])
#     return value
    
# def p_SourceFile(p):
#     """
#     SourceFile : SetupContext PackageClause SEMICOLON ImportDeclMult TopLevelDeclMult
#     """(p)
#     endContext()

# def p_SetupContext(p):
#     """
#     SetupContext :
#     """    
#     p[0] = []
#     setupContext()

# def p_BeginScope(p):
#     """
#     : 
#     """
#     p[0] = []
#     beginScope()

# def p_EndScope(p):
#     """
#     : 
#     """
#     p[0] = []
#    ()
    ('left', 'LBRACE'),
    ('right', 'ASSIGN', 'DEFINE'),
    ('left','IDENT'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','INT', 'FLOAT', 'IMAG', 'RUNE', 'STRING'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left', 'COMMA'),
    ('right', 'NOT', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN', 'AND_NOT_ASSIGN'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'EQL', 'NEQ','LSS','LEQ','GTR','GEQ'),
    ('left', 'ADD', 'SUB','OR','XOR'),
    ('left', 'MUL', 'QUO','REM','AND','AND_NOT','SHL','SHR'),
    ('left', 'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'RBRACE', 'INC', 'DEC', 'PERIOD'),
    ('left', 'UMUL'),
)

non_terminals = {}
ignored_tokens = [';', '{', '}', '(', ')', '[', ']', ',']

##################################################################################
####################                                        ######################
#####                         STARTING GRAMMAR                            ########
####################                                        ######################
##################################################################################

stm = SymTableMaker()
ast = None
    
def p_SourceFile(p):
    """
    SourceFile : PackageClause SEMICOLON ImportDeclMult TopLevelDeclMult
    """
    global ast
    p[0] = FileNode(p[1], p[3], p[4])
    ast = p[0]

###################################################################################
### Package related grammar
###################################################################################

def p_PackageClause(p):
    """
    PackageClause : PACKAGE IDENT
    """
    p[0] = LitNode(dataType = 'string', label = f'"{p[2]}"')

###################################################################################
### Import related grammar
###################################################################################

def p_ImportDeclMult(p):
    """
    ImportDeclMult : ImportDecl SEMICOLON ImportDeclMult
                   |  
    """
    if len(p) > 1:
        p[3].addChild(*p[1])
        p[0] = p[3]
    else:
        p[0] = ImportNode()

def p_ImportDecl(p):
    """
    ImportDecl : IMPORT ImportSpec
               | IMPORT LPAREN ImportSpecMult RPAREN
    """
    if len(p) == 3:
        p[0] = [p[2]]
    elif len(p) == 5:
        p[0] = p[3]

def p_ImportMult(p):
    """
    ImportSpecMult : ImportSpec SEMICOLON ImportSpecMult  
               |
    """
    if len(p) == 1:
        p[0] = []
    elif len(p) == 4:
        p[3].append(p[1])
        p[0] = p[3]

def p_ImportSpec(p):
    """
    ImportSpec : PERIOD ImportPath
              | IDENT ImportPath
              | ImportPath 
    """
    if len(p) == 2:
        alias = IdentNode(0, p[1][1:-1])
        path = LitNode("string", p[1])
        p[0] = ImportPathNode(alias, path)
    
def p_ImportPath(p):
    """
    ImportPath : STRING
    """
    p[0] = p[1]

###################################################################################
### Top-Level related grammar
###################################################################################

def p_TopLevelDeclMult(p):
    """
    TopLevelDeclMult : TopLevelDecl SEMICOLON TopLevelDeclMult 
                     |
    """
    if len(p)>1:
        if isinstance(p[1], list):
            p[3].addChild(*p[1])
        else:
            p[3].addChild(p[1])
        p[0] = p[3]

    if len(p)==1:
        p[0] = DeclNode()

def p_TopLevelDecl(p):
    """
    TopLevelDecl : Decl 
                 | FuncDecl
    """
    if p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []

def p_Decl(p):
    """
    Decl : ConstDecl 
         | VarDecl
         | TypeDecl
    """
    if p[1] is not None:
        p[0] = p[1]

###################################################################################
### Constant Declarations
###################################################################################

def p_ConstDecl(p):
    """
    ConstDecl : CONST ConstSpec
              | CONST LPAREN ConstSpecMult RPAREN
    """
    if len(p)==3:
        p[0] = p[2]
    
    else:
        p[0] = p[3]

def p_ConstSpecMult(p):
    """
    ConstSpecMult : ConstSpec SEMICOLON ConstSpecMult 
                  | ConstSpec
    """
    if len(p) == 4:
        p[3].extend(p[1])
        p[0] = p[3]

    else:
        p[0] = []

def p_ConstSpec(p):
    """
    ConstSpec : IdentifierList Type ASSIGN ExpressionList 
              | IdentifierList IDENT ASSIGN ExpressionList
              | IdentifierList ASSIGN ExpressionList
    """
    p[0] = []

    if len(p[1]) != len(p[len(p)-1]):
        raise NameError("Assignment is not balanced", p.lineno(1))
    
    if len(p) > 4:
        dt = {}
        if isinstance(p[2], str):
            dt['BaseType'] = p[2]
            dt['level'] = 0
        else:
            dt = p[2].dataType
        
        for i, expression in enumerate(p[len(p)-1]):
            if not isTypeCastable(stm, dt, expression.dataType):
                raise TypeError("Mismatch of type for identifier: " + p[1][i].label, p.lineno(1))

    for (ident, val) in zip(p[1], p[len(p)-1]):
        expr = ExprNode(dataType=p[2], label="ASSIGN", operator="=")
        expr.addChild(ident, val)
        p[0].append(expr)

    not_base_type = False

    if not isinstance(p[2], str):
        not_base_type = True

    for i, (ident, val) in enumerate(zip(p[1], p[len(p)-1])):

        # Check redeclaration for identifier list
        latest_scope = stm.getScope(ident.label)
        if latest_scope == stm.id or ident.label in stm.functions:
            raise NameError('Redeclaration of identifier: ' + ident, p.lineno(1))
        
        dt = p[2].dataType

        if not_base_type:
            present = checkTypePresence(stm, dt) 
        else:
            present = stm.findType(stm, dt)

        if present == -1:
            raise TypeError('Type not declared/found: ' + dt, p.lineno(1))
        else:
            # Add to symbol table
            stm.add(ident, {'type': p[2].dataType, 'isConst' : True})
            p[1].children[i].dataType = dt
 
###################################################################################
### Variable Declarations
###################################################################################

def p_VarDecl(p):
    """
    VarDecl : VAR VarSpec
            | VAR LPAREN VarMult RPAREN
    """
    if len(p)==3:
        p[0] = p[2]
    
    else:
        p[0] = p[3]

def p_VarMult(p):
    """
    VarMult : VarSpec SEMICOLON VarMult 
            | VarSpec
    """
    if len(p) > 1:
        p[3].extend(p[1])
        p[0] = p[3]
    else:
        p[0] = [Node()] 

def p_VarSpec(p):
    """
    VarSpec : IdentifierList Type ASSIGN ExpressionList
            | IdentifierList IDENT ASSIGN ExpressionList
            | IdentifierList ASSIGN ExpressionList
            | IdentifierList Type
            | IdentifierList IDENT
    """
    p[0] = []

    if len(p) >= 4:
        if len(p[1]) != len(p[len(p)-1]):
            raise NameError("Assignment is not balanced", p.lineno(1))
        
        if len(p) > 4:
            dt = {}
            if isinstance(p[2], str):
                dt['BaseType'] = p[2]
                dt['level'] = 0
            else:
                dt = p[2].dataType
            
            for i, expression in enumerate(p[len(p)-1]):
                if not isTypeCastable(stm, dt, expression.dataType):
                    raise TypeError("Mismatch of type for identifier: " + p[1][i].label, p.lineno(1))

        for (ident, val) in zip(p[1], p[len(p)-1]):
            expr = ExprNode(dataType=p[2], label="ASSIGN", operator="=")
            expr.addChild(ident, val)
            p[0].append(expr)

        not_base_type = False

        if not isinstance(p[2], str):
            not_base_type = True

        for i, (ident, val) in enumerate(zip(p[1], p[len(p)-1])):

            # Check redeclaration for identifier list
            latest_scope = stm.getScope(ident.label)
            if latest_scope == stm.id or ident.label in stm.functions:
                raise NameError('Redeclaration of identifier: ' + ident, p.lineno(1))
            
            dt = p[2].dataType

            if not_base_type:
                present = checkTypePresence(stm, dt) 
            else:
                present = stm.findType(stm, dt)

            if present == -1:
                raise TypeError('Type not declared/found: ' + dt, p.lineno(1))
            else:
                # Add to symbol table
                stm.add(ident, {'type': p[2].dataType, 'isConst' : False})
                p[1].children[i].dataType = dt
    else:
        not_base_type = False

        if not isinstance(p[2], str):
            not_base_type = True

        for i, ident in enumerate(p[1]):

            # Check redeclaration for identifier list
            latest_scope = stm.getScope(ident.label)
            if latest_scope == stm.id or ident.label in stm.functions:
                raise NameError('Redeclaration of identifier: ' + ident, p.lineno(1))

            dt = p[2].dataType

            if not_base_type:
                present = checkTypePresence(stm, dt) 
            else:
                present = stm.findType(stm, dt)

            if present == -1:
                raise TypeError('Type not declared/found: ' + dt, p.lineno(1))
            else:
                # Add to symbol table
                stm.add(ident, {'type': p[2].dataType, 'isConst' : False})
                p[1].children[i].dataType = dt



###################################################################################
### Type Declarations
###################################################################################

def p_TypeDecl(p):
    """
    TypeDecl : TYPE TypeSpec
             | TYPE LPAREN TypeSpecMult RPAREN
    """

def p_TypeSpecMult(p):
    """
    TypeSpecMult : TypeSpec SEMICOLON TypeSpecMult 
                 | 
    """

    
def p_TypeSpec(p):
    """
    TypeSpec : AliasDecl
             | Typedef
    """

def p_AliasDecl(p):
    """
    AliasDecl : IDENT ASSIGN Type
                | IDENT ASSIGN IDENT
    """ 
    dt = {}
    if isinstance(p[3], str):
        dt['baseType'] = p[3]
        dt['level'] = 0
    else:
        dt = p[3].dataType

    if checkTypePresence(stm, dt) == -1:
        raise TypeError("BaseType " + dt + " not declared yet")

    if p[1] in stm[stm.id].typeDefs:
        raise TypeError("Redeclaration of Alias " + p[1], p.lineno(1))
        
    else:
       stm[stm.id].typeDefs[p[1]] = dt['baseType']

def p_TypeDef(p):
    """
    Typedef : IDENT Type
              | IDENT IDENT

    """
    if p[1] in stm[stm.id].typeDefs:
        raise ("Redeclaration of Alias " + p[1].label, p.lineno(1))
    present = stm.findType(p[len(p)-1])
    if present != -1:
       stm[stm.id].typeDefs[p[1].label] = p[len(p)-1].label
    else:
        raise TypeError('Base type not found ' + p[len(p)-1], p.lineno(1))


###################################################################################
### Identifier List
###################################################################################

def p_IdentifierList(p):
    """
    IdentifierList : IDENT
                   | IDENT COMMA IdentifierList
    """

    if len(p) == 2:
        p[0] = [IdentNode(label = p[1], scope = stm.id)]

    else:
        p[3].append(IdentNode(label = p[1], scope = stm.id))
        p[0] = p[3]


###################################################################################
#####################                                        ######################
######                           EXPRESSIONS                               ########
#####################                                        ######################
###################################################################################

def p_ExpressionList(p):
    """
    ExpressionList : Expr
                   | ExpressionList COMMA Expr
    """
    if len(p) == 2:
        p[0] = [p[1]]
        
    else:
        p[1].append(p[3])
        p[0] = p[1]
    
def p_Expr(p):
    """
    Expr : UnaryExpr 
         | Expr LOR  Expr
         | Expr LAND Expr
         | Expr EQL  Expr
         | Expr NEQ Expr
         | Expr LSS Expr
         | Expr LEQ Expr
         | Expr GTR Expr
         | Expr GEQ Expr
         | Expr ADD  Expr
         | Expr SUB Expr
         | Expr OR Expr
         | Expr XOR Expr
         | Expr MUL Expr
         | Expr QUO Expr
         | Expr REM Expr
         | Expr SHL Expr
         | Expr SHR Expr
         | Expr AND Expr
         | Expr AND_NOT Expr
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        dt1 = p[1].dataType
        dt2 = p[3].dataType

        # if not checkBinOp(stm, dt1, dt2, p[2], p[3].label[0]):
        #     raise TypeError("Incompatible operand types", p.lineno(1))

        dt = getFinalType(stm, dt1, dt2, p[2])

        isConst = False
        if (p[1].isConst and p[3].isConst):
            isConst = True

        p[0] = ExprNode(operator = p[2], dataType = dt, label = p[1].label+p[2]+p[3].label, isConst = isConst)
        p[0].addChild(p[1], p[3])

def p_UnaryExpr(p):
    """
    UnaryExpr : PrimaryExpr 
            | ADD UnaryExpr
            | SUB UnaryExpr
            | NOT UnaryExpr
            | XOR UnaryExpr
            | MUL UnaryExpr
            | AND UnaryExpr
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # if not checkUnOp(stm, p[1], p[2].dataType):
        #     raise TypeError("Incompatible operand for Unary Expression", p.lineno(1))
        
        p[0] = ExprNode(dataType = getUnaryType(p[2].dataType, p[1]), operator=p[1])
        p[0].addChild(p[2])

###################################################################################
### Primary Expression
###################################################################################

def p_PrimaryExpr(p):
    """
    PrimaryExpr :  Lit
                | IDENT
                | LPAREN Expr RPAREN
                | PrimaryExpr Selector
                | PrimaryExpr Index
                | PrimaryExpr Slice
                | PrimaryExpr Arguments
    """

    ## PrimaryExpr -> Lit
    if len(p) == 2 and isinstance(p[1], LitNode):
        p[0] = p[1]

    # ## Primary Expr -> Ident
    elif (len(p) == 2):

        # # Check declaration
        # latest_scope = ((stm.getScope(p[1]) != -1) or (p[1] in stm.functions)) 

        # if latest_scope == 0:
        #     ## To be checked for global declarations (TODO)
        #     print("Expecting global declaration for ",p[1], p.lineno(1))
            
        # dt = stm.get(p[1])['type']
        p[0] = ExprNode(dataType=None, label = p[1])
    
    ## Primary Expr -> LPAREN Expr RPAREN
    elif len(p) == 4:
        p[0] = p[2]

    else:
        ## PrimaryExpr -> PrimaryExpr Selector
        if isinstance(p[2], DotNode):
            p[2].addChild(p[1])

        ## PrimaryExpr -> PrimaryExpr Index
        elif isinstance(p[2], IndexNode):
            p[2].children[0] = p[1]

        ## PrimaryExpr -> PrimaryExpr Slice
        elif isinstance(p[2], SliceNode):
            p[2].children[0] = p[1]

        ## PrimaryExpr -> PrimaryExpr Arguments
        elif isinstance(p[2], List):
            p[2] = FuncCallNode(p[1], p[2])
        
        p[0] = p[2]
    

###################################################################################
## Selector

def p_Selector(p):
    """
    Selector : PERIOD IDENT
    """
    p[0] = DotNode()
    p[0].addChild(p[2])

###################################################################################
## Index

def p_Index(p):
    """
    Index : LBRACK Expr RBRACK
    """
    p[0] = IndexNode(None, p[2])

###################################################################################
## Slice

def p_Slice(p):
    """
    Slice : LBRACK Expr COLON Expr RBRACK
          | LBRACK COLON Expr RBRACK
          | LBRACK Expr COLON RBRACK
          | LBRACK COLON RBRACK
          | LBRACK COLON Expr COLON Expr RBRACK
          | LBRACK Expr COLON Expr COLON Expr RBRACK
    """
    lIndexNode = None
    rIndexNode = None
    maxIndexNode = None
    if len(p) == 5:
        if(p[2] == ":"):
            rIndexNode = p[3]
        else:
            lIndexNode = p[2]
    elif len(p) == 6:
        lIndexNode = p[2]
        rIndexNode = p[4]
    elif len(p) == 7:
        rIndexNode = p[3]
        maxIndexNode = p[5]
    elif len(p) == 8:
        lIndexNode = p[2]
        rIndexNode = p[4]
        maxIndexNode = p[6]
    
    p[0] = SliceNode(None, lIndexNode, rIndexNode, maxIndexNode)

###################################################################################
## Arguments

def p_Arguments(p):
    """
    Arguments : LPAREN RPAREN
              | LPAREN ExpressionList RPAREN
              | LPAREN ExpressionList COMMA RPAREN
              | LPAREN TypeT RPAREN
              | LPAREN TypeT COMMA RPAREN
              | LPAREN TypeT COMMA ExpressionList RPAREN 
              | LPAREN TypeT COMMA ExpressionList COMMA RPAREN 
              | LPAREN IDENT RPAREN
              | LPAREN IDENT COMMA RPAREN
              | LPAREN IDENT COMMA ExpressionList RPAREN 
              | LPAREN IDENT COMMA ExpressionList COMMA RPAREN 
    """
    p[0] = []
    if len(p) == 4:
        if isinstance(p[2], list):
            p[0] = p[2]
        else:
            p[0] = [p[2]]
    elif len(p) == 5:
        if isinstance(p[2], list):
            p[0] = p[2]
        else:
            p[0] = [p[2]]
    elif len(p) == 6 or len(p) == 7:
        p[0] = [p[2]] + p[4]

    # p[0] = Node()

    # if len(p) == 3:
    #     return

    # ## Arguments : LPAREN ExpressionList RPAREN or LPAREN ExpressionList
    # if not isinstance(p[2], str) and p[2].children != None and len(p[2].children) > 0 and isinstance(p[2].children[0], ExprNode):
    #     p[0] = p[2]
    
    # elif len(p) > 3 and isinstance(p[2], str) and p[3] != '.':
    #     if stm.findType(p[2]) == -1:
    #         raise TypeError("Type " + p[2] + " not defined before", p.lineno(1))
    #     else:
    #         if len(p) == 4 or len(p) == 5:
    #             p[0].addChild(*[Type(datatype = p[2], scope = stm.id)])
    #         else:
    #             p[4].children.append(Type(datatype = p[2], scope = stm.id))
    #             p[0] = p[4]

###################################################################################
#####################                                        ######################
######                             TYPES                                   ########
#####################                                        ######################
###################################################################################

def p_Type(p):
    """
    Type : TypeT
         | PointerType
         | LPAREN PointerType RPAREN
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParenType(p[2], dataType = p[2].dataType)

def p_TypeT(p):
    """
    TypeT : ArrayType
          | StructType
          | SliceType
          | MapType
          | LPAREN TypeT RPAREN
          | LPAREN IDENT RPAREN
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ParenType(p[2], dataType = p[2].dataType)


###################################################################################
### Pointer Type
###################################################################################

def p_PointerType(p):
    """
    PointerType : MUL Type %prec UMUL
               | MUL IDENT %prec UMUL
    """
    p[0] = PointerType(p[2])

    if isinstance(p[2], str):
         p[0].dataType['baseType'] = p[2]
         p[0].dataType['level'] = 1
    else:
        p[0].dataType['baseType'] = p[2].dataType['baseType']
        p[0].dataType['level'] = p[2].dataType['level'] + 1
    
    p[0].dataType['name'] = 'pointer'

    


###################################################################################
### Slice Type
###################################################################################

def p_SliceType(p):
    """
    SliceType : LBRACK RBRACK ElementType
    """
    p[0] = BrackType(p[3])
        
    p[0].dataType['baseType'] = p[3].dataType['baseType']
    p[0].dataType['level'] = p[3].dataType['level'] + 1
   

    p[0].dataType['name'] = 'slice'

###################################################################################
### Array Type
###################################################################################

def p_ArrayType(p):
    """
    ArrayType : LBRACK ArrayLength RBRACK ElementType
    """
    p[0] = BrackType(p[2], p[4])

    p[0].dataType['baseType'] = p[4].dataType['baseType']
    p[0].dataType['level'] = p[4].dataType['level'] + 1
    
    p[0].dataType['name'] = 'array'

def p_ArrayLength(p):
    """
    ArrayLength : Expr
    """
    p[0] = p[1]


def p_ElementType(p):
    """
    ElementType : Type
                | IDENT
    """
    p[0] = ElementaryType()
    
    if not isinstance(p[1], str):
        p[0].dataType = p[1].dataType 
    else:
        p[0].dataType['baseType'] = p[1]
        p[0].dataType['level'] = 0

    p[0].dataType['name'] = 'elementary'

###################################################################################
### Struct Type
###################################################################################

def p_StructType(p):
    """
    StructType : STRUCT BeginStruct LBRACE FieldDeclMult RBRACE EndStruct 
    """
    p[0] = StructType(p[4])
    p[0].dataType = {}

    for i, item in enumerate(p[4]):
        p[0].dataType[i] = item.dataType

    p[0].dataType['name'] = 'struct'

def p_BeginStruct(p):
    """
    BeginStruct : 
    """

def p_EndStruct(p):
    """
    EndStruct : 
    """

#extra
def p_FieldDeclMult(p):
    """
    FieldDeclMult : FieldDeclMult FieldDecl SEMICOLON
                  | 
    """
    if len(p) == 1:
        return []
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_FieldDecl(p):
    """
    FieldDecl : IdentifierList Type 
              | IdentifierList IDENT
              | EmbeddedField
              | IdentifierList Type Tag
              | IdentifierList IDENT Tag
              | EmbeddedField Tag
    """
    if len(p) == 2:
        p[0] = [StructFieldType(None, p[1], None)]
        if isinstance(p[1], str):
            p[0].dataType['baseType'] = p[1]
            p[0].dataType['level'] = 0
        else:
            p[0].dataType = p[1].dataType 

    elif len(p) == 3:
        if isinstance(p[1], List):
            p[0] = []
            for key in p[1]:
                p[0].append(StructFieldType(key, p[2], None))
                if isinstance(p[2], str):
                    p[0].dataType.append({'baseType': p[2], 'level' : 0})   
                else:
                    p[0].dataType.append(p[2].dataType)         
        else:
            p[0] = [StructFieldType(None, p[1], p[2])]

    elif len(p) == 4:
        p[0] = []
        for key in p[1]:
            p[0].append(StructFieldType(key, p[2], p[3]))
            if isinstance(p[2], str):
                p[0].dataType.append({'baseType': p[2], 'level' : 0})   
            else:
                p[0].dataType.append(p[2].dataType)
                    
    p[0].dataType['name'] = 'field'
    
def p_Tag(p):
    """
    Tag : STRING
    """
    p[0] = p[1]

def p_EmbeddedField(p):
    """
    EmbeddedField : MUL IDENT
                  | IDENT
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = PointerType(p[2])
        p[0].dataType['baseType'] = p[2]
        p[0].dataType['level'] = 1
    p[0].dataType['name'] = 'embedded'

###################################################################################
### Map Type
###################################################################################

def p_MapType(p):
    """
    MapType : MAP LBRACK KeyType RBRACK ElementType
    """
    p[0] = MapType(p[3], p[5])

    p[0].dataType = {'name' : 'map'}
    p[0].dataType['KeyType'] = p[2].dataType
    p[0].dataType['ValueType'] = p[4].dataType

def p_KeyType(p):
    """
    KeyType : Type
            | IDENT
    """
    p[0] = p[1]

    if isinstance(p[1], str):
        p[0].dataType['baseType'] = p[1]
        p[0].dataType['level'] = 0

    p[0].dataType['name'] = 'key'


###################################################################################
#####################                                        ######################
######                             LITERALS                                ########
#####################                                        ######################
###################################################################################

def p_Lit(p):
    """
    Lit : BasicLit
        | CompositeLit
        | FunctionLit
    """
    p[0] = p[1]

###################################################################################
### Basic Literal
###################################################################################
    
def p_BasicLit(p):
    """
    BasicLit : IntLit
             | FloatLit
             | ImagLit
             | RuneLit
             | StringLit
             | BoolLit
    """
    p[0] = p[1]

def p_IntLit(p):
    """
    IntLit : INT
    """
    p[0] = LitNode(dataType = 'int', label = p[1])
    # if check_int(p[1]):
    #     p[0] = LitNode(dataType = 'int', label = p[1])
    # else:
    #     raise ("Integer Overflow detected", p.lineno(1))

def p_FloatLit(p):
    """
    FloatLit : FLOAT
    """
    p[0] = LitNode(dataType = 'float64', label = p[1])
    
def p_ImagLit(p):
    """
    ImagLit : IMAG
    """
    p[0] = LitNode(dataType = 'complex128', label = p[1])

def p_RuneLit(p):
    """
    RuneLit : RUNE
    """
    p[0] = LitNode(dataType = 'rune', label = p[1])

def p_StringLit(p):
    """
    StringLit : STRING
    """
    p[0] = LitNode(dataType = 'string', label = p[1])

def p_BoolLit(p):
    """
    BoolLit : BOOL
    """
    p[0] = LitNode(dataType = 'bool', label = p[1])

###################################################################################
### Composite Literal
###################################################################################

## Need to implement checks
def p_CompositeLit(p):
    """
    CompositeLit : StructType Arguments
                 | ArrayType LiteralValue
                 | SliceType LiteralValue
                 | MapType LiteralValue
                 | IDENT LiteralValue
    """
    p[0] = p[2]
    if not isinstance(p[1], str):
        p[0].dataType = p[1].dataType
    else:
        p[0].dataType['baseType'] = p[1]
        p[0].dataType['level'] = 0

    # if isinstance(p[1], BrackType):
    #     return p[2]
    # elif isinstance(p[1], MapType):
    #     return p[2]
    # elif len(p) == 3:
    #     return p[2]


def p_LiteralValue(p):
    """
    LiteralValue : LBRACE ElementList COMMA RBRACE 
                 | LBRACE ElementList RBRACE 
                 | LBRACE RBRACE 
    """
    if len(p) > 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_ElementList(p):
    """
    ElementList : KeyedElement 
                | ElementList COMMA KeyedElement 
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[3].append(p[1])
        p[0] = p[3]

def p_KeyedElement(p):
    """
    KeyedElement : Element
                 | Key COLON Element
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = KeyValNode(p[1], p[3])

def p_Key(p):
    """
    Key : Expr
        | LiteralValue
    """
    p[0] = p[1]

def p_Element(p):
    """
    Element : Expr
            | LiteralValue
    """
    p[0] = p[1]

###################################################################################
### Function Literal
###################################################################################

def p_FunctionLit(p):
    """
    FunctionLit : FUNC Signature FunctionBody
    """
    p[0] = FuncNode(None, p[2][0], p[2][1], p[3])

###################################################################################
## Function Declarations

def p_FuncDecl(p):
    """
    FuncDecl : FUNC FunctionName Signature FunctionBody
             | FUNC FunctionName Signature
    """
    
    ## Add entry in stm
    # info = {'params' : [], 'result': []}
    # for i in range(len(p[3].children)):
    #     if isinstance(p[3].children[i], ResultNode):
    #         info['result'].append(p[3].children[i].dataType)
    #     else:
    #         info['params'].append([p[3].children[i].label, p[3].children[i].dataType]) 

    # stm.addFunction(p[2].label, info)

    ## Make node
    p[0] = FuncNode(p[2], p[3][0], p[3][1], p[4])
    

# def p_BeginFunc(p):
#     """
#     BeginFunc : 
#     """
#     stm.newScope()

# def p_EndFunc(p):
#     """
#     EndFunc : 
#     """
#     stm.exitScope()

###################################################################################
## Function Name
def p_FunctionName(p):
    """
    FunctionName : IDENT
    """
    p[0] = p[1]
    # ##  Check redeclaration
    # if p[2].label in stm.functions:
    #     raise ("Redeclaration of function " + p[2].label, p.lineno(1))
    
    # ## Add func type to symbol table
    # stm[stm.id].addType("func")

    # info = {}
    # stm.addFunction(p[1], info)

    # p[0] = IdentNode(scope = stm.id, label = p[1], dataType = "func")

###################################################################################
## Function Body

def p_FunctionBody(p):
    """
    FunctionBody : Block
    """
    p[0] = p[1]

###################################################################################
## Function Signature

def p_Signature(p):
    """
    Signature : Parameters Result
              | Parameters
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], None]

    # p[0] = Node()
    # p[0].children.append(p[1])
    # if len(p) > 2:
    #     p[0].children.append(p[2])

###################################################################################
## Function Parameters

def p_Parameters(p):
    """
    Parameters : LPAREN RPAREN
               | LPAREN ParameterList RPAREN
               | LPAREN ParameterList COMMA RPAREN
    """
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]

def p_ParameterList(p):
    """
    ParameterList : ParameterDecl
                  | ParameterList COMMA IDENT
                  | ParameterList COMMA Type
                  | ParameterList COMMA ParameterDecl 
    """
    if len(p)==2 :
        p[0] = FuncParamNode(p[1])

    elif len(p) == 4 and isinstance(p[3], List):
        p[1].addChild(*p[3])
        p[0] = p[1]

    else:
        p[0] = FuncParamNode(p[1])
        p[0].addChild(p[3])

def p_ParameterDecl(p):
    """
    ParameterDecl : IdentifierList Type
                  | IdentifierList IDENT
    """
    p[0] = p[1]
    # p[0] = Node()
    
    # if len(p) == 3 and isinstance(p[2], str):
    #     stm[stm.id].addType(p[2])

    #     for i, child in enumerate(p[1].children):
    #         p[0].chidren.append(ParamNode(label = child.label, dataType = p[2]))

###################################################################################
## Return Type

def p_Result(p):
    """
    Result : Parameters 
           | Type
           | IDENT
    """
    p[0] = FuncReturnNode(p[1])
    # p[0] = ResultNode()
    # if len(p) == 1 and isinstance(p[1], str):
    #     p[0].children.append(IdentNode(dataType = p[1]))
    
    # elif len(p) == 1:
    #     p[0] = p[1]

###################################################################################
#####################                                        ######################
######                           STATEMENTS                                ########
#####################                                        ######################
###################################################################################

def p_StatementList(p):
    """
    StatementList : Statement SEMICOLON StatementList  
                  | 
    """
    if len(p) == 4:
        if isinstance(p[1], List):
            p[3].extend(p[1])
        elif p[1] is not None:
            p[3].append(p[1])
        p[0] = p[3]
    else:
        p[0] = []

def p_Statement(p):
    """
    Statement : Decl
              | LabeledStmt
              | SimpleStmt
              | GotoStmt
              | ReturnStmt
              | BreakStmt
              | ContinueStmt
              | FallthroughStmt
              | Block
              | IfStmt
              | SwitchStmt
              | ForStmt
    """
    p[0] = p[1]

###################################################################################
### Labeled Statements
###################################################################################

def p_LabeledStmt(p):
    """
    LabeledStmt : Label COLON Statement
    """
    p[0] = LabelNode(p[1], p[3])

def p_Label(p):
    """
    Label : IDENT
    """
    p[0] = p[1]

###################################################################################
### Simple Statements
###################################################################################

def p_SimpleStmt(p):
    """
    SimpleStmt :  EmptyStmt
                | ExpressionStmt
                | IncDecStmt
                | Assignment
                | ShortVarDecl
    """
    p[0] = p[1]

###################################################################################
### Empty Statements

def p_EmptyStmt(p):
    """
    EmptyStmt : 
    """

###################################################################################
### Expression Statements

def p_ExpressionStmt(p):
    """
    ExpressionStmt : Expr
    """
    p[0] = p[1]

###################################################################################
### Increment/Decrement Statements

def p_IncDecStmt(p):
    """
    IncDecStmt :  Expr INC
                 | Expr DEC
    """
    if p[2] == '++':
        p[0] = IncNode(p[1])
    else:
        p[0] = DecNode(p[1])

###################################################################################
### Assignment Statements

def p_Assignment(p):
    """
    Assignment : ExpressionList assign_op ExpressionList
    """
    p[0] = []
    for key, val in zip(p[1], p[3]):
        exprNode = ExprNode(None, operator=p[2])
        exprNode.addChild(key, val)
        p[0].append(exprNode)

def p_assign_op(p):
    """
    assign_op : add_op_assign 
              | mul_op_assign
              | ASSIGN
    """
    p[0] = p[1]

def p_add_op_assign(p):
    """
    add_op_assign : ADD_ASSIGN
                    | SUB_ASSIGN
                    | OR_ASSIGN
                    | XOR_ASSIGN
    """
    p[0] = p[1]

def p_mul_op_assign(p):
    """
    mul_op_assign : MUL_ASSIGN
                    | QUO_ASSIGN
                    | REM_ASSIGN
                    | AND_ASSIGN
                    | SHL_ASSIGN
                    | SHR_ASSIGN
                    | AND_NOT_ASSIGN
    """
    p[0] = p[1]

###################################################################################
### Short Variable Declaration

def p_ShortVarDecl(p):
    """
    ShortVarDecl : IdentifierList DEFINE ExpressionList
    """
    p[0] = []
    for key, val in zip(p[1], p[3]):
        exprNode = ExprNode(None, label="DEFINE", operator="=")
        exprNode.addChild(key, val)
        p[0].append(exprNode)

###################################################################################
### Goto Statements
###################################################################################

def p_GotoStmt(p):
    """
    GotoStmt :  GOTO Label
    """
    p[0] = GotoNode(p[2])

###################################################################################
### Return Statements
###################################################################################

def p_ReturnStmt(p):
    """
    ReturnStmt : RETURN ExpressionList
                | RETURN
    """
    if len(p) == 2:
        p[0] = ReturnNode([])
    else:
        p[0] = ReturnNode(p[2])

###################################################################################
### Break Statements
###################################################################################

def p_BreakStmt(p):
    """
    BreakStmt : BREAK Label
                | BREAK
    """
    if len(p) == 2:
        p[0] = BreakNode()
    else:
        p[0] = BreakNode(p[2])

###################################################################################
### Continue Statements
###################################################################################

def p_ContinueStmt(p):
    """
    ContinueStmt :  CONTINUE Label
                    | CONTINUE
    """
    if len(p) == 2:
        p[0] = ContinueNode()
    else:
        p[0] = ContinueNode(p[2])

###################################################################################
### Fallthrough Statements
###################################################################################

def p_FallthroughStmt(p):
    """
    FallthroughStmt : FALLTHROUGH
    """
    p[0] = FallthroughNode()

###################################################################################
### Block Statements
###################################################################################

def p_Block(p):
    """
    Block : LBRACE StatementList RBRACE
    """
    p[0] = BlockNode(p[2])

###################################################################################
### If Else Statements
###################################################################################

def p_IfStmt(p):
    """
    IfStmt : IF Expr Block else_stmt
           | IF SimpleStmt SEMICOLON Expr Block else_stmt
    """
    if len(p) == 5:
        p[0] = IfNode(None, p[2], ThenNode(p[3]), p[4])
    else:
        p[0] = IfNode(p[2], p[4], ThenNode(p[5]), p[6])

def p_else_stmt(p):
    """
    else_stmt : ELSE IfStmt
                | ELSE Block
                |
    """
    if len(p) > 1:
        p[0] = ElseNode(p[2])

###################################################################################
### Switch Statements
###################################################################################

def p_SwitchStmt(p):
    """
    SwitchStmt :  ExprSwitchStmt
                 | TypeSwitchStmt
    """
    p[0] = p[1]

###################################################################################
### Expression Switch Statements

def p_ExprSwitchStmt(p):
    """
    ExprSwitchStmt : SWITCH SimpleStmt SEMICOLON Expr LBRACE BeginSwitch ExprCaseClauseMult EndSwitch RBRACE
                     | SWITCH Expr LBRACE BeginSwitch ExprCaseClauseMult EndSwitch RBRACE
                     | SWITCH SimpleStmt SEMICOLON LBRACE BeginSwitch ExprCaseClauseMult EndSwitch RBRACE
                     | SWITCH LBRACE BeginSwitch ExprCaseClauseMult EndSwitch RBRACE
    """


def p_BeginSwitch(p):
    """
    BeginSwitch : 
    """

def p_EndSwitch(p):
    """
    EndSwitch : 
    """

def p_ExprCaseClauseMult(p):
    """
    ExprCaseClauseMult : ExprCaseClause ExprCaseClauseMult 
                         |
    """

def p_ExprCaseClause(p):
    """
    ExprCaseClause : ExprSwitchCase COLON StatementList
    """

def p_ExprSwitchCase(p):
    """
    ExprSwitchCase : CASE ExpressionList
                     | DEFAULT
    """

###################################################################################
### Type Switch Statements

def p_TypeSwitchStmt(p):
    """
    TypeSwitchStmt : SWITCH SimpleStmt SEMICOLON TypeSwitchGuard LBRACE TypeCaseClauseMult RBRACE
                     | SWITCH TypeSwitchGuard LBRACE TypeCaseClauseMult RBRACE
    """

def p_TypeSwitchGuard(p):
    """
    TypeSwitchGuard : IDENT DEFINE PrimaryExpr PERIOD LPAREN TYPE RPAREN
                      | PrimaryExpr PERIOD LPAREN TYPE RPAREN
    """

def p_TypeCaseClauseMult(p):
    """
    TypeCaseClauseMult : TypeCaseClause TypeCaseClauseMult 
                        |
    """

def p_TypeCaseClause(p):
    """
    TypeCaseClause : CASE TypeList COLON StatementList
                     | DEFAULT COLON StatementList
    """

def p_TypeList(p):
    """
    TypeList : Type
                | IDENT 
                | Type COMMA TypeList
                | IDENT COMMA TypeList
    """

###################################################################################
### For Statements
###################################################################################

def p_ForStmt(p):
    """
    ForStmt : FOR BeginFor Condition Block EndFor
            | FOR BeginFor ForClause Block EndFor
            | FOR BeginFor RangeClause Block EndFor
            | FOR BeginFor Block EndFor
    """

def p_BeginFor(p):
    """
    BeginFor : 
    """
    # print("For Begins")
    # beginScope()
    # context['forDepth'] += 1
    # Add two labels to be used
    # for code generation

def p_EndFor(p):
    """
    EndFor : 
    """
    # print("For Ends")
#     context['forDepth'] -= 1
#    ()

def p_Condition(p):
    """
    Condition : Expr
    """

###################################################################################
### For Clause

def p_ForClause(p):
    """
    ForClause : InitStmt SEMICOLON Condition SEMICOLON PostStmt
                | InitStmt SEMICOLON SEMICOLON PostStmt
    """

def p_InitStmt(p):
    """
    InitStmt :   SimpleStmt
    """

def p_PostStmt(p):
    """
    PostStmt :   SimpleStmt
    """

###################################################################################
### Range Clause

def p_RangeClause(p):
    """
    RangeClause : RangeList RANGE Expr
    """

def p_RangeList(p):
    """
    RangeList : ExpressionList ASSIGN 
                | IdentifierList DEFINE
                | 
    """


###################################################################################
#####################                                        ######################
######                             ERROR                                   ########
#####################                                        ######################
###################################################################################

def p_error(p):
    print("Syntax Error: ", p)


###################################################################################
#####################                                        ######################
######                           BUILD LEXER                               ########
#####################                                        ######################
###################################################################################

def parse():
    lexer = lex.lex()

    parser, grammar = yacc.yacc(debug = True)

    path_to_root = os.environ.get('PATH_TO_ROOT')
    milestone = os.environ.get('MILESTONE')
    if path_to_root is not None:
        with open(path_to_root + "/src/Milestone" + str(milestone) + "/action.txt", "w") as f:
            for key, val in parser.action.items():
                f.writelines(f'{key} : {val}\n')

        with open(path_to_root + "/src/Milestone" + str(milestone) + "/goto.txt", "w") as f:
            for key, val in parser.goto.items():
                f.writelines(f'{key} : {val}\n')

    non_terminals = grammar.Nonterminals

    # Trying to handle input
    with open(sys.argv[1], 'r') as f:
        import pprint
        out = parser.parse(f.read(), lexer = lexer)
        if out is None:
            f.close()
            sys.exit(1)
        output_file = sys.argv[1][:-2] + "output"
        with open(output_file, 'w') as fout:
            pprint.pprint(out, width=10, stream=fout)
    
    return ast
