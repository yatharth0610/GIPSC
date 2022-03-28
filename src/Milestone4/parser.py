from typing import List
from copy import deepcopy
import ply.yacc as yacc
import ply.lex as lex
import lexer
from lexer import *
import sys
import pprint
from scope import *
from utils import *

tokens=lexer.tokens
tokens.remove('COMMENT')
precedence = (
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

_symbol = '_'
stm.add(_symbol, {'dataType': {'name': '_', 'baseType': '_', 'level': 0}})
    
def p_SourceFile(p):
    """
    SourceFile : PackageClause SEMICOLON ImportDeclMult TopLevelDeclMult
    """
    global ast
    # Check if any label has expecting key set
    for label in stm.labels:
        if stm.labels[label]['expecting'] == True:
            assert(len(stm.labels[label]['prevGotos']) > 0)
            goto = stm.labels[label]['prevGotos'][0]
            raise LogicalError(f"{goto[1]}: Goto declared without declaring any label {label}.")
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
        path = LitNode(dataType = "string", label = p[1])
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
        p[0] = DeclNode()
        if isinstance(p[1], list):
            p[0].addChild(*p[1])
        else:
            p[0].addChild(p[1])

        p[0].addChild(*p[3].children)

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
    length = len(p)-1

    count_0 = 0
    count_1 = 0

    expression_datatypes = []

    for i in range(len(p[length])):
        if isinstance(p[length][i], FuncCallNode):
            func_name = p[length][i].children[0].label
            dt_return = stm.functions[func_name]["return"]
            expression_datatypes.extend(dt_return)
            if len(dt_return) == 0:
                raise TypeError("Function does not return anything!")
            elif len(dt_return) == 1:
                count_0+=1
            else:
                count_1+=1
        else:
            expression_datatypes.append(p[length][i].dataType)
    
    if count_1 > 0:
        raise TypeError(f"{p.lexer.lineno}: Functions with multi-valued return type can't be allowed in single-value context!.")
        if len(p[length]) > 1:
            raise TypeError("Function with more than one return values should be assigned alone!")

    if len(p[1]) != len(expression_datatypes):
        raise NameError("Assignment is not balanced", p.lexer.lineno)
    
    dt = {}

    if len(p) > 4:
        if isinstance(p[2], str):
            p[2] = stm.findType(p[2])

        if isinstance(p[2], str):
            dt = {'baseType' : p[2], 'name': p[2], 'level': 0}
        else:
            dt = p[2].dataType
        
        for i, expression in enumerate(expression_datatypes):
            
            #print("Datatypes being compared:", dt, temp)
            if not isTypeCastable(stm, dt, expression):
                raise TypeError("Mismatch of type for identifier: " + p[1][i].label, p.lexer.lineno)

    if count_1 > 0:
        expr = ExprNode(dataType = dt, label = "ASSIGN", operator = "=")
        for child in p[1]:
            expr.addChild(child)
        expr.addChild(p[length][0])
        p[0].append(expr)
    else:
        for (ident, val) in zip(p[1], p[len(p)-1]):
            expr = ExprNode(dataType=p[2], label="ASSIGN", operator="=")
            expr.addChild(ident, val)
            p[0].append(expr)

    not_base_type = False

    if not isinstance(p[2], str):
        not_base_type = True

    for i, ident in enumerate(p[1]):

        # Check redeclaration for identifier list
        latest_scope = stm.getScope(ident.label)
        if latest_scope == stm.id or ident.label in stm.functions:
            raise NameError('Redeclaration of identifier: ' + ident, p.lexer.lineno)
        
        if len(p) > 4:
            if not not_base_type:
                dt = {'baseType' : p[2], 'name': p[2], 'level': 0}
            else:
                dt = p[2].dataType

            if not_base_type:
                present = checkTypePresence(stm, dt) 
            else:
                present = stm.findType(stm, dt)

            if present == -1:
                raise TypeError('Type not declared/found: ' + dt, p.lexer.lineno)
            else:
                val = None
                # Add to symbol table
                if dt['name'].startswith('int'):
                    val = int(p[length][i].label)
                elif dt['name'].startswith('float'):
                    val = float(p[length][i].label)
                ## Write conditions for rune and other types
                stm.add(ident.label, {'dataType': dt, 'isConst' : True, 'val': val})
                p[1][i].dataType = dt
        else:
            val = None
            dt = p[length][i].dataType
            # Add to symbol table
            if dt['name'].startswith('int'):
                val = int(p[length][i].label)
            elif dt['name'].startswith('float'):
                val = float(p[length][i].label)
            ## Write conditions for rune and other types
            stm.add(ident.label, {'dataType': dt, 'isConst' : True, 'val': val})
            p[1][i].dataType = dt
 
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
    length = len(p)-1
    if len(p) >= 4:
        count_0 = 0
        count_1 = 0

        expression_datatypes = []

        for i in range(len(p[length])):
            if isinstance(p[length][i], FuncCallNode):
                func_name = p[length][i].children[0].label
                dt_return = stm.functions[func_name]["return"]
                expression_datatypes.extend(dt_return)
                if len(dt_return) == 0:
                    raise TypeError("Function does not return anything!")
                elif len(dt_return) == 1:
                    count_0+=1
                else:
                    count_1+=1
            else:
                expression_datatypes.append(p[length][i].dataType)
        if count_1 > 0:
            if len(p[length]) > 1:
                raise TypeError(f"{p.lexer.lineno}: Function with more than one return values should be assigned alone!")
        if len(p[1]) != len(expression_datatypes):
            raise NameError(f"{p.lexer.lineno}: Assignment is not balanced", p.lexer.lineno)
        
        dt = {}

        if len(p) > 4:
            if isinstance(p[2], str):
                p[2] = stm.findType(p[2])

            if isinstance(p[2], str):
                dt = {'baseType' : p[2], 'name': p[2], 'level': 0}
            else:
                dt = p[2].dataType
            for i, expression in enumerate(expression_datatypes):
                if not isTypeCastable(stm, dt, expression):
                    raise TypeError(f"{p.lexer.lineno}: Mismatch of type for identifier: " + p[1][i].label)

        if count_1 > 0:
            expr = ExprNode(dataType = dt, label = "ASSIGN", operator = "=")
            for child in p[1]:
                expr.addChild(child)
            expr.addChild(p[length][0])
            p[0].append(expr)
        else:
            for (ident, val) in zip(p[1], p[len(p)-1]):
                expr = ExprNode(dataType=dt, label="ASSIGN", operator="=")
                expr.addChild(ident, val)
                p[0].append(expr)

        not_base_type = False

        if not isinstance(p[2], str):
            not_base_type = True

        for i, ident in enumerate(p[1]):

            # Check redeclaration for identifier list
            latest_scope = stm.getScope(ident.label)
            if latest_scope == stm.id or ident.label in stm.functions:
                raise NameError('Redeclaration of identifier: ' + ident, p.lexer.lineno)
            
            if len(p) > 4:
                if not not_base_type:
                    dt = {'baseType' : p[2], 'name': p[2], 'level': 0}
                else:
                    dt = p[2].dataType

                if not_base_type:
                    present = checkTypePresence(stm, dt) 
                else:
                    present = stm.findType(stm, dt)

                if present == -1:
                    raise TypeError('Type not declared/found: ' + dt, p.lexer.lineno)
                else:
                    # Add to symbol table
                    stm.add(ident.label, {'dataType': dt, 'isConst' : False})
                    p[1][i].dataType = dt    
            else:
                dt = p[length][i].dataType
                # Add to symbol table
                stm.add(ident.label, {'dataType': dt, 'isConst' : False})
                p[1][i].dataType = dt
    else:
        not_base_type = False

        if not isinstance(p[2], str):
            not_base_type = True

        for i, ident in enumerate(p[1]):

            # Check redeclaration for identifier list
            latest_scope = stm.getScope(ident.label)
            if latest_scope == stm.id or ident.label in stm.functions:
                raise NameError('Redeclaration of identifier: ' + ident, p.lexer.lineno)

            if not not_base_type:
                dt = {'baseType' : p[2], 'name': p[2], 'level': 0}
            else:
                dt = p[2].dataType

            if not_base_type:
                present = checkTypePresence(stm, dt) 
            else:
                present = stm.findType(stm, dt)

            if present == -1:
                raise TypeError('Type not declared/found: ' + dt, p.lexer.lineno)
            else:
                # Add to symbol table
                stm.add(ident.label, {'dataType': dt, 'isConst' : False})
                p[1][i].dataType = dt



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
        dt['name'] = p[3]
        dt['baseType'] = p[3]
        dt['level'] = 0
    else:
        dt = p[3].dataType

    if checkTypePresence(stm, dt) == -1:
        raise TypeError("baseType " + dt + " not declared yet")

    if p[1] in stm.symTable[stm.id].typeDefs:
        raise TypeError("Redeclaration of Alias " + p[1], p.lexer.lineno)
        
    elif isinstance(p[3], str) and p[3] in stm.symTable[stm.id].avlTypes:
        stm.symTable[stm.id].typeDefs[p[1]] = p[3]
    
    elif isinstance(p[3], str):
        stm.symTable[stm.id].typeDefs[p[1]] = stm.symTable[stm.id].typeDefs[p[3]]

    else:
        stm.symTable[stm.id].typeDefs[p[1]] = dt

def p_TypeDef(p):
    """
    Typedef : IDENT Type
              | IDENT IDENT

    """
    if isinstance(p[2], str):
        p[2] = stm.findType(p[2])
    dt = p[2].dataType

    if checkTypePresence(stm, dt) == -1:
        raise TypeError("baseType " + dt + " not declared yet")

    if p[1] in stm.symTable[stm.id].typeDefs:
        raise TypeError("Redeclaration of type " + p[1], p.lexer.lineno)
        
    elif isinstance(p[2], str) and p[2] in stm.symTable[stm.id].avlTypes:
        stm.symTable[stm.id].typeDefs[p[1]] = p[2]
    
    elif isinstance(p[2], str):
        stm.symTable[stm.id].typeDefs[p[1]] = stm.symTable[stm.id].typeDefs[p[2]]

    else:
        stm.symTable[stm.id].typeDefs[p[1]] = p[2]
        # params = []
        # for key in dt['keyTypes']:
        #     params.append(dt['keyTypes'][key])
        # stm.addFunction(p[1], {"params": params , "return": [p[2]], "dataType": {'name': 'func', 'baseType': 'func', 'level': 0}})

###################################################################################
### Identifier List
###################################################################################

def p_IdentifierList(p):
    """
    IdentifierList : IDENT
                   | IDENT COMMA IdentifierList
    """
    
    p[0] = [IdentNode(label = p[1], scope = stm.id)]

    if len(p) > 2:
        p[0].extend(p[3])


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

        if not checkBinOp(stm, dt1, dt2, p[2], p[3].label[0]):
            raise TypeError("Incompatible operand types", p.lexer.lineno)

        dt = getFinalType(stm, dt1, dt2, p[2])

        isConst = False
        val = None
        if isinstance(p[1], ExprNode) and isinstance(p[3], ExprNode) and p[1].isConst and p[3].isConst:
            isConst = True
            val = Operate(p[2], p[1].val, p[3].val, p.lexer.lineno, p[3].dataType['name'])

        p[0] = ExprNode(operator = p[2], dataType = dt, label = p[1].label+p[2]+p[3].label, isConst = isConst, val=val)
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
        flag = False
        if not isinstance(p[2], str) and hasattr(p[2], 'isAddressable'):
            flag = p[2].isAddressable 
        if not checkUnOp(stm, p[2].dataType, p[1], flag):
            raise TypeError("Incompatible operand for Unary Expression", p.lexer.lineno)
        val = None
        isConst = p[2].isConst
        if isConst:
            if p[1] == '*' or p[1] == '&':
                # Referencing or dereferencing a constant in compile time is not possible
                isConst = False
                val = None
            else:
                val = Operate(p[1], None, p[2].val, p.lexer.lineno, p[2].dataType['name'])
        p[0] = ExprNode(dataType = getUnaryType(stm, p[2].dataType, p[1]), operator=p[1], isConst=isConst, val=val)
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
    if len(p) == 2 and (isinstance(p[1], LitNode) or isinstance(p[1], CompositeLitNode)):
        if isinstance(p[1], LitNode):
            p[0] = ExprNode(p[1].dataType, p[1].label, None, p[1].isConst, False, p[1].val)
            if p[1].children:
                for child in p[1].children:
                    p[0].children.append(child)
        else:
            # Ig Composite Literal is only used for assignment
            p[0] = p[1]

    ## PrimaryExpr -> Ident
    elif (len(p) == 2):
        if p[1] in stm.symTable[0].typeDefs:
            # Type Declaration Found
            # Assuming Constructor Initialisation
            dt = stm.symTable[0].typeDefs[p[1]]
            p[0] = ExprNode(dataType=dt, label=p[1], isAddressable=False, isConst=False, val=None)
            return

        # Check declaration
        latest_scope = ((stm.getScope(p[1]) != -1) or (p[1] in stm.functions)) 

        if latest_scope == 0:
            ## To be checked for global declarations (TODO)
            print("Expecting global declaration for ",p[1], p.lexer.lineno)
        stm_entry = stm.get(p[1])
        dt = stm_entry['dataType']
        p[0] = ExprNode(dataType=dt, label = p[1], isAddressable=True, isConst=stm_entry.get('isConst', False), val=stm_entry.get('val', None))
    
    ## PrimaryExpr -> LPAREN Expr RPAREN
    elif len(p) == 4:
        p[0] = p[2]

    else:
        dt = None
        ## PrimaryExpr -> PrimaryExpr Selector
        if isinstance(p[2], DotNode):
            if 'name' not in p[1].dataType or p[1].dataType['name'] != 'struct':
                raise TypeError("Expecting struct type but found different one", p.lexer.lineno)
            
            field = p[2].chidren[0]
            found = False
            idx = -1
            for i in p[1].dataType:
                if i == 'name':
                    continue
                if p[1].dataType[i]['field']==field:
                    found = True
                    idx = i
                    
            if not found:
                raise NameError("No such field found in " + p[1].label, p.lexer.lineno)                

            p[2].addChild(p[1])
            dt = p[2].dataType[idx]

        ## PrimaryExpr -> PrimaryExpr Index
        elif isinstance(p[2], IndexNode):
            if 'name' not in p[1].dataType or (p[1].dataType['name'] != 'array' and p[1].dataType['name']!= 'map') :
                raise TypeError("Expecting array or map type but found different one", p.lexer.lineno)

            if p[1].dataType['name'] == 'array':
                if isinstance(p[2].dataType, str):
                    if not isBasicInteger(stm, p[2].dataType):
                        raise TypeError("Index cannot be of type " + p[2].dataType, p.lexer.lineno)
                else:
                    if isinstance(p[2].dataType['baseType'], str) and p[2].dataType['level'] == 0:
                        if not isBasicInteger(stm, p[2].dataType['baseType']):
                            raise TypeError("Index cannot be of type " + p[2].dataType, p.lexer.lineno)
                    else:
                        raise TypeError("Index type incorrect", p.lexer.lineno)

                dt = p[1].dataType.copy()
                dt['level']-=1

                if dt['level']==0:
                    dt = {'name': dt['baseType'], 'baseType': dt['baseType'], 'level': 0}

            if p[1].dataType['name'] == 'map':
                if not isTypeCastable(p[2].dataType, p[1].dataType['KeyType']):
                    raise TypeError("Incorrect type for map " + p.lexer.lineno)
                dt = p[1].dataType['ValueType']

            p[2].children[0] = p[1]
            

        ## PrimaryExpr -> PrimaryExpr Slice
        elif isinstance(p[2], SliceNode):
            if 'name' not in p[1].dataType or p[1].dataType['name'] != 'slice' :
                raise TypeError("Expecting a slice type but found different one", p.lexer.lineno)

            if  p[2].lIndexNode != None: 
                if not isBasicInteger(stm, p[2].lIndexNode.dataType['baseType']):
                    raise TypeError("Index cannot be of type " + p[2].dataType, p.lexer.lineno)
            
            if  p[2].rIndexNode != None: 
                if not isBasicInteger(stm, p[2].rIndexNode.dataType['baseType']):
                    raise TypeError("Index cannot be of type " + p[2].dataType, p.lexer.lineno)

            else:
                if isinstance(p[2].lIndexNode.dataType, str):
                    if not isBasicInteger(stm, p[2].lIndexNode.dataType):
                        raise TypeError("Index cannot be of type " + p[2].lIndexNode.dataType, p.lexer.lineno)
                else:
                    if isinstance(p[2].lIndexNode.dataType['baseType'], str) and p[2].lIndexNode.dataType['level'] == 0:
                        if not isBasicInteger(stm, p[2].lIndexNode.dataType):
                            raise TypeError("Index cannot be of type " + p[2].lIndexNode.dataType, p.lexer.lineno)
                    else:
                        raise TypeError("Index type incorrect", p.lexer.lineno)
                
                if isinstance(p[2].rIndexNode.dataType, str):
                    if not isBasicInteger(stm, p[2].rIndexNode.dataType):
                        raise TypeError("Index cannot be of type " + p[2].rIndexNode.dataType, p.lexer.lineno)
                else:
                    if isinstance(p[2].rIndexNode.dataType['baseType'], str) and p[2].rIndexNode.dataType['level'] == 0:
                        if not isBasicInteger(stm, p[2].rIndexNode.dataType):
                            raise TypeError("Index cannot be of type " + p[2].rIndexNode.dataType, p.lexer.lineno)
                    else:
                        raise TypeError("Index type incorrect", p.lexer.lineno)

            dt = p[1].dataType.copy()
            p[2].children[0] = p[1]

        ## PrimaryExpr -> PrimaryExpr Arguments
        elif isinstance(p[2], List):
            dt = stm.findType(p[1].label)
            if dt != -1:
                if not isinstance(dt, StructType):
                    raise TypeError(f'Not of type struct')
                p[2] = CompositeLitNode(dt, p[2])
                p[0] = p[2]
                p[0].dataType = dt.dataType
                p[0].isAddressable = False
                return
            else:
                if p[1].label not in stm.functions:
                    raise NameError("No such function declared ", p.lexer.lineno)

                info = stm.functions[p[1].label]
                paramList = info['params']
                dt = None
                if info['return'] != None:
                    dt = info['return']

                if len(paramList) != len(p[2]):
                    raise NameError("Different number of arguments in function call: " + p[1].label + "\n Expected " + str(len(paramList)) + " number of arguments but got " + str(len(p[2])), p.lexer.lineno)

                for i, argument in enumerate(p[2]):
                    dt1 = argument.dataType
                    dt2 = paramList[i]

                    if not isTypeCastable(stm, dt1, dt2):
                        raise TypeError("Type mismatch on argument number: " + i, p.lexer.lineno)

                p[2] = FuncCallNode(p[1], p[2])
        
        p[0] = p[2]       
        p[0].isAddressable = True
        p[0].dataType = dt
        if isinstance(p[2], list):
            p[0].isAddressable = False            

###################################################################################
## Selector

def p_Selector(p):
    """
    Selector : PERIOD IDENT
    """
    p[0] = DotNode()
    p[0].addChild(p[2])

#########################FuncCallNo##########################################################
## Index

def p_Index(p):
    """
    Index : LBRACK Expr RBRACK
    """
    p[0] = IndexNode(None, p[2], dataType = p[2].dataType)

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
        dt = None
        if isinstance(p[2], str):
            p[0] = stm.findType(p[2])
        else:
            p[0] = p[2]


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
    p[0] = BrackType(p[4], p[2])

    p[0].dataType['baseType'] = p[4].dataType['baseType']
    p[0].dataType['level'] = p[4].dataType['level'] + 1
    
    p[0].dataType['name'] = 'array'

def p_ArrayLength(p):
    """
    ArrayLength : Expr
    """
    if p[1].dataType['name'] != 'int':
        raise TypeError(f"{p.lexer.lineno}: ArrayLength must be of Integer Type")
    # Golang requires that array size be constant representable
    # const int x = 2
    # var a [x+x]int = [x+x]int{2, 3} works
    # var int x = 2
    # var a [x+x]int = [x+x]int{2, 3} doesn't work
    if p[1].isConst != True:
        raise TypeError(f"{p.lexer.lineno}: ArrayLength is not a constant.")

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
        p[0] = []
    else:
        p[1].extend(p[2])
        p[0] = p[1]


def p_FieldDecl(p):
    """
    FieldDecl : IdentifierList Type 
              | IdentifierList IDENT
              | EmbeddedField
    """
    if len(p) == 2:
        p[0] = [StructFieldType(p[1], p[1])]

    elif len(p) == 3:
        p[0] = []
        if isinstance(p[2], str):
            p[2] = stm.findType(p[2])
        for key in p[1]:
            p[0].append(StructFieldType(key, p[2]))
    

def p_EmbeddedField(p):
    """
    EmbeddedField : MUL IDENT
                  | IDENT
    """
    if len(p) == 2:
        t = stm.findType(p[1])
        t.label = p[1]
        p[0] = t
    else:
        t = stm.findType(p[2])
        t.label = p[2]
        p[2] = t
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

    if p[2].dataType['name'] == 'map' or p[2].dataType['name'] == 'func' or p[2].dataType['name'] == 'slice' or p[2].dataType['name'] == 'array':
        raise TypeError(f"{p.lexer.lineno} Invalid map key type")

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
    if check_int(p[1]):
        p[0] = LitNode(dataType = {'name': 'int', 'baseType': 'int', 'level': 0}, label = p[1], isConst=True, val=int(p[1]))
    else:
        raise ("Integer Overflow detected", p.lexer.lineno)

def p_FloatLit(p):
    """
    FloatLit : FLOAT
    """
    p[0] = LitNode(dataType = {'name': 'float64', 'baseType': 'float64', 'level': 0}, label = p[1], isConst=True, val=float(p[1]))
    
def p_ImagLit(p):
    """
    ImagLit : IMAG
    """
    p[0] = LitNode(dataType = {'name': 'complex128', 'baseType': 'complex128', 'level': 0}, label = p[1], isConst=True, val=float(p[1].strip('i')))

def p_RuneLit(p):
    """
    RuneLit : RUNE
    """
    p[0] = LitNode(dataType = {'name': 'rune', 'baseType': 'rune', 'level': 0}, label = p[1], isConst=True, val=p[1])

def p_StringLit(p):
    """
    StringLit : STRING
    """
    p[0] = LitNode(dataType = {'name': 'string', 'baseType': 'string', 'level': 0}, label = p[1], isConst=True, val=p[1])

def p_BoolLit(p):
    """
    BoolLit : BOOL
    """
    p[0] = LitNode(dataType = {'name': 'bool', 'baseType': 'bool', 'level': 0}, label = p[1], isConst=True, val = p[1])

###################################################################################
### Composite Literal
###################################################################################

## Need to implement checks
# TODO: Remove arguments
def p_CompositeLit(p):
    """
    CompositeLit : StructType LiteralValue
                 | ArrayType LiteralValue
                 | SliceType LiteralValue
                 | MapType LiteralValue
                 | IDENT LiteralValue
    """
    if isinstance(p[1], str):
        p[1] = stm.findType(p[1])
    p[0] = CompositeLitNode(p[1], p[2])

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
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

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
    FuncDecl : FuncSig FunctionBody
             | FuncSig
    """
    ## Make node
    p[0] = FuncNode(p[1][0], p[1][1][0], p[1][1][1], p[2])
    stm.currentReturnType = None
    stm.exitScope()

def p_FuncSig(p):
    """
    FuncSig : FUNC FunctionName Signature
    """
    if p[3][1] == None:
        if p[3][0] == None:
            stm.addFunction(p[2].label, {"params": [] , "return": [], "dataType": {'name': 'func', 'baseType': 'func', 'level': 0}})
            stm.currentReturnType = p[3][1]
            stm.newScope()
        else:
            stm.addFunction(p[2].label, {"params": p[3][0].dataType, "return": [], "dataType": {'name': 'func', 'baseType': 'func', 'level': 0}})
            stm.currentReturnType = p[3][1]
            stm.newScope()
            for i, param in enumerate(p[3][0].children):
                stm.add(param.label, {"dataType": param.dataType, "val": param.val, "isConst": param.isConst, "isArg": True})
                p[3][0].children[i].scope = stm.id

    else:
        if p[3][0] == None:
            stm.addFunction(p[2].label, {"params": [] , "return": p[3][1].dataType, "dataType": {'name': 'func', 'baseType': 'func', 'level': 0}})
            stm.currentReturnType = p[3][1]
            stm.newScope()
        else:
            stm.addFunction(p[2].label, {"params": p[3][0].dataType, "return": p[3][1].dataType, "dataType": {'name': 'func', 'baseType': 'func', 'level': 0}})
            stm.currentReturnType = p[3][1]
            stm.newScope()
            for i, param in enumerate(p[3][0].children):
                stm.add(param.label, {"dataType": param.dataType, "val": param.val, "isConst": param.isConst, "isArg": True})
                p[3][0].children[i].scope = stm.id
    
    p[0] = [p[2], p[3]]

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
    ##  Check redeclaration
    if p[1] in stm.functions or stm.getScope(p[1]) >= 0 :
        raise ("Redeclaration of function " + p[1], p.lexer.lineno)

    p[0] = IdentNode(scope = stm.id, label = p[1], dataType = "func")

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
        p[0] = [p[1], FuncReturnNode([])]

###################################################################################
## Function Parameters

def p_Parameters(p):
    """
    Parameters : LPAREN RPAREN
               | LPAREN ParameterList RPAREN
               | LPAREN ParameterList COMMA RPAREN
    """
    if len(p) == 3:
        p[0] = FuncParamNode([])
    else:
        p[0] = p[2]
    

def p_ParameterList(p):
    """
    ParameterList : ParameterDecl
                  | ParameterList COMMA ParameterDecl
    """
    if len(p)==2 :
        p[0] = FuncParamNode(p[1])

    elif len(p) == 4:
        p[1].addChild(*p[3])
        p[0] = p[1]

def p_ParameterDecl(p):
    """
    ParameterDecl : IdentifierList Type
                  | IdentifierList IDENT
    """
    p[0] = p[1]
    if isinstance(p[2], str):
        p[2] = stm.findType(p[2])
    for i in range(len(p[0])):
        p[0][i].dataType = p[2].dataType

###################################################################################
## Return Type

def p_Result(p):
    """
    Result : LPAREN ParametersType RPAREN
           | LPAREN RPAREN
           | IDENT
           | Type
    """
    if len(p) > 3:
        if isinstance(p[2], str):
            p[2] = stm.findType(p[2])
        if isinstance(p[2], Type):
            p[2] = [p[2]]
        p[0] = FuncReturnNode(p[2])
    else:
        p[0] = FuncReturnNode([])

def p_ParametersType(p):
    """
    ParametersType : IDENT
                   | Type
                   | ParametersType COMMA IDENT
                   | ParametersType COMMA Type
    """
    if len(p) == 2:
        if isinstance(p[1], str):
            p[0] = FuncParamType()
            p[0].addChild(stm.findType(p[1]))
        else:
            p[0] = FuncParamType()
            p[0].addChild(p[1])
    else:
        if isinstance(p[3], str):
            p[1].addChild(ElementaryType(dataType={'name':p[3], 'baseType': p[3], 'level': 0}))
        else:
            p[1].addChild(p[3])
        p[0] = p[1]

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
            p[1].extend(p[3])
        elif p[1] is not None:
            p[1] = [p[1]]
            p[1].extend(p[3])
        p[0] = p[1]
    else:
        p[0] = []

def p_Statement(p):
    """
    Statement : Decl
              | SimpleStmt
              | BreakStmt
              | ContinueStmt
              | FallthroughStmt
              | Block
              | GotoStmt
              | LabeledStmt
              | IfStmt
              | SwitchStmt
              | ForStmt
              | ReturnStmt
    """
    p[0] = p[1]

###################################################################################
### Labeled Statements
###################################################################################

def p_LabeledStmt(p):
    """
    LabeledStmt : Label COLON Statement
    """

    labelScopeTab = deepcopy(stm.symTable[stm.getCurrentScope()])
    if p[1] not in stm.labels:
        # Create a new label and need not set expecting to true; set it to false
        stm.labels[p[1]] = {
            'scopeTab': labelScopeTab,
            'mappedName' : stm.getNewLabel(),
            'expecting' : False ,
            'lineno' : p.lexer.lineno,
            'prevGotos': []
        }
    elif p[1] in stm.labels:
        # Analyse previous gotos (if any), and set expecting to False
        if stm.labels[p[1]]['expecting'] == True:
            for goto in stm.labels[p[1]]['prevGotos']:
                gotoScopeTab, gotoLineno = goto
                if not isValidGoto(stm, labelScopeTab, gotoScopeTab, checkNoSkipVar=True):
                    raise LogicalError(f"{p.lexer.lineno}: Invalid placement of Goto at {gotoLineno} - Goto statement outside of a block can't jump inside a block and variable declarations can't be skipped.")
            stm.labels[p[1]]['expecting'] = False
            stm.labels[p[1]]['scopeTab'] = labelScopeTab
            stm.labels[p[1]]['lineno'] = p.lexer.lineno
        else:
            # Redeclaration of label - Error
            raise LogicalError(f"{p.lexer.lineno}: Label declared earlier at {stm.labels[p[1]]['lineno']}.")
    p[0] = LabelNode(p[1], LabelStatementNode(p[3], p.lexer.lineno))

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
    p[0] = EmptyNode()

###################################################################################
### Expression Statements

def p_ExpressionStmt(p):
    """
    ExpressionStmt : Expr
    """
    # Check if builtin function definitions are added in STM
    builtInFuncsToAvoid = [
        'append',
        'cap',
        'complex',
        'imag',
        'len',
        'make',
        'new',
        'real'
    ]
    if hasattr(stm, 'builtInFuncs') and isinstance(p[1], FuncCallNode):
        funcName =  p[1].children[0].children[0]
        if funcName in builtInFuncsToAvoid and funcName not in stm.functions:
            funcReturnType = stm.builtInFuncs[funcName]['return']
            raise ValueNotUsedError(f"{p.lexer.lineno}: Value of type {funcReturnType} is not used.")
    p[0] = p[1]

###################################################################################
### Increment/Decrement Statements

def p_IncDecStmt(p):
    """
    IncDecStmt :  Expr INC
                 | Expr DEC
    """
    if p[1].isAddressable == False:
        raise LogicalError(f"{p.lexer.lineno}: Expression is not addressable.")
    if not isBasicNumeric(stm, p[1].dataType):
        raise LogicalError(f"{p.lexer.lineno}: Non-numeric type can't be incremented or decremented.")
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
    if len(p[1]) != len(p[3]):
        if len(p[3]) == 1 and isinstance(p[3][0], FuncCallNode):
            pass 
        else:
            raise LogicalError(f"{p.lexer.lineno}: Imbalanced assignment with {len(p[1])} identifiers and {len(p[3])} expressions.")
    p[0] = []
    for key, val in zip(p[1], p[3]):
        if key.label != _symbol:
            if key.isConst == True:
                raise TypeError(f"{p.lexer.lineno}: LHS contains constant! Cannot assign")
            if key.dataType != val.dataType:
                raise TypeError(f"{p.lexer.lineno}: Type of {key.label} and {val.label} doesn't match.")
            if key.isAddressable == False:
                raise TypeError(f"{p.lexer.lineno}: LHS expression is not assignable")
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

    length = len(p) - 1

    count_0 = 0
    count_1 = 0

    expression_datatypes = []

    for i in range(len(p[length])):
        if isinstance(p[length][i], FuncCallNode):
            func_name = p[length][i].children[0].label
            dt_return = stm.functions[func_name]["return"]
            expression_datatypes.extend(dt_return)
            if len(dt_return) == 0:
                raise TypeError("Function does not return anything!")
            elif len(dt_return) == 1:
                count_0+=1
            else:
                count_1+=1
        else:
            expression_datatypes.append(p[length][i].dataType)
    
    if count_1 > 0:
        if len(p[length]) > 1:
            raise TypeError("Function with more than one return values should be assigned alone!")

    if len(p[1]) != len(expression_datatypes):
        raise NameError("Assignment is not balanced", p.lexer.lineno)
    
    dt = {}

    if len(p[1]) != len(p[3]):
        raise LogicalError(f"{p.lexer.lineno}: Imbalanced declaration with {len(p[1])} identifiers and {len(p[3])} expressions.")
    p[0] = []
    for key, val in zip(p[1], p[3]):
        exprNode = ExprNode(None, label="DEFINE", operator="=")
        exprNode.addChild(key, val)
        p[0].append(exprNode)

    for i, ident in enumerate(p[1]):

        # Check redeclaration for identifier list
        latest_scope = stm.getScope(ident.label)
        if latest_scope == stm.id or ident.label in stm.functions:
            raise NameError('Redeclaration of identifier: ' + ident, p.lexer.lineno)
        
        # Add to symbol table
        dt = p[length][i].dataType
        stm.add(ident.label, {'dataType': dt, 'isConst' : False})
        p[1][i].dataType = dt

###################################################################################
### Goto Statements
###################################################################################

def p_GotoStmt(p):
    """
    GotoStmt :  GOTO Label
    """
    gotoScopeTab = deepcopy(stm.symTable[stm.getCurrentScope()])
    if p[2] in stm.labels:
        # Label has been seen before
        if stm.labels[p[2]]['expecting']:
            # Currently not seen the labeled statement
            # Label has been created earlier by previous goto
            stm.labels[p[2]]['prevGotos'].append(
                (gotoScopeTab, p.lexer.lineno)
            )
        else:
            # Label already declared before (backward jump)
            # Check parent condition
            if not isValidGoto(stm, stm.labels[p[2]]['scopeTab'], gotoScopeTab):
                raise LogicalError(f"{p.lexer.lineno}: Invalid placement of goto wrt label at {stm.labels[p[2]]['lineno']} - Goto statement outside of a block can't jump inside a block.")
            # No need to append gotos as semantic analysis is complete
    else:
        # Label not declared before; expecting label; (forward jump)
        # Semantic analysis to be done when corresponding Label is parsed

        # Will shallow copy work or do we need deepcopy?
        # Label is created for the first time from goto
        stm.labels[p[2]] = {
            'scopeTab': None,
            'mappedName' : stm.getNewLabel(),
            'expecting' : True ,
            'lineno' : None,
            'prevGotos': [
                (gotoScopeTab, p.lexer.lineno)
            ]
        }
            
    p[0] = GotoNode(p[2])

###################################################################################
### Return Statements
###################################################################################

def p_ReturnStmt(p):
    """
    ReturnStmt : RETURN ExpressionList
                | RETURN
    """
    # This case should never arise
    if stm.currentReturnType is None:
        raise LogicalError(f"{p.lexer.lineno}: Return statement outside of a function.")
    # if len(stm.currentReturnType)
    if len(p) == 2:
        if stm.currentReturnType:
            raise LogicalError(f"{p.lexer.lineno}: Current function doesn't return nothing.")
        p[0] = ReturnNode([])
    else:
        for returnDataType, ExprNode in zip(stm.currentReturnType.dataType, p[2]):
            if returnDataType != ExprNode.dataType:
                return LogicalError(f"{p.lexer.lineno}: Return type of current function and the return statement doesn't match.")
        p[0] = ReturnNode(p[2])

###################################################################################
### Break Statements
###################################################################################

def p_BreakStmt(p):
    """
    BreakStmt : BREAK 
              | BREAK Label
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
    ContinueStmt :  CONTINUE
                 |  CONTINUE Label
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
    """
                #  | TypeSwitchStmt
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
    smtNode = None
    varNode = None
    casesNode = []
    if len(p) == 7:
        casesNode = p[4]
    elif len(p) == 8:
        varNode = p[2]
        casesNode = p[5]
    elif len(p) == 9:
        smtNode = p[2]
        casesNode = p[6]
    else:
        smtNode = p[2]
        varNode = p[4]
        casesNode = p[7]
    
    p[0] = SwitchNode(smtNode, varNode, casesNode)

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
    if len(p) == 2:
        return []
    else:
        p[2].append(p[1])
        p[0] = p[2]

def p_ExprCaseClause(p):
    """
    ExprCaseClause : ExprSwitchCase COLON StatementList
    """
    p[0] = CasesNode(p[1], p[3])

def p_ExprSwitchCase(p):
    """
    ExprSwitchCase : CASE ExpressionList
                     | DEFAULT
    """
    if len(p) == 3:
        p[0] = []
        for expr in p[2]:
            p[0].append(CaseNode(expr))
    else:
        p[0] = [DefaultNode()]

###################################################################################
### Type Switch Statements

# def p_TypeSwitchStmt(p):
#     """
#     TypeSwitchStmt : SWITCH SimpleStmt SEMICOLON TypeSwitchGuard LBRACE TypeCaseClauseMult RBRACE
#                      | SWITCH TypeSwitchGuard LBRACE TypeCaseClauseMult RBRACE
#     """

# def p_TypeSwitchGuard(p):
#     """
#     TypeSwitchGuard : IDENT DEFINE PrimaryExpr PERIOD LPAREN TYPE RPAREN
#                       | PrimaryExpr PERIOD LPAREN TYPE RPAREN
#     """

# def p_TypeCaseClauseMult(p):
#     """
#     TypeCaseClauseMult : TypeCaseClause TypeCaseClauseMult 
#                         |
#     """

# def p_TypeCaseClause(p):
#     """
#     TypeCaseClause : CASE TypeList COLON StatementList
#                      | DEFAULT COLON StatementList
#     """

# def p_TypeList(p):
#     """
#     TypeList : Type
#                 | IDENT 
#                 | Type COMMA TypeList
#                 | IDENT COMMA TypeList
#     """

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
    if len(p) == 5:
        p[0] = ForNode(None, p[3])
    else:
        p[0] = ForNode(p[3], p[4])

def p_BeginFor(p):
    """
    BeginFor : 
    """
    stm.newScope()
    stm.forDepth += 1

def p_EndFor(p):
    """
    EndFor : 
    """
    stm.forDepth -= 1
    stm.exitScope()
    
def p_Condition(p):
    """
    Condition : Expr
    """
    p[0] = ForClauseNode(None, p[1], None)

###################################################################################
### For Clause

def p_ForClause(p):
    """
    ForClause : InitStmt SEMICOLON Condition SEMICOLON PostStmt
                | InitStmt SEMICOLON SEMICOLON PostStmt
    """
    if len(p) == 6:
        p[0] = ForClauseNode(p[1], p[3].children[1], p[5])
    else:
        dt = {
            'name' : 'bool',
            'baseType': 'bool',
            'level' : 0
        }
        trueNode = ExprNode(dt, label='true', operator=None, isConst=True, isAddressable=False, val='true')
        # Absence of condition is equivalent to a FOR true statement
        p[0] = ForClauseNode(p[1], trueNode, p[4])

def p_InitStmt(p):
    """
    InitStmt :   SimpleStmt
    """
    p[0] = p[1]

def p_PostStmt(p):
    """
    PostStmt :   SimpleStmt
    """
    if isinstance(p[1], ExprNode) and p[1].label == 'DEFINE':
        raise LogicalError("Short Variable Declaration not allowed in post statement of for loop.")
    p[0] = p[1]

###################################################################################
### Range Clause

def p_RangeClause(p):
    """
    RangeClause : RangeList RANGE Expr
    """
    if not (p[3].dataType['name'] in ['array', 'slice', 'map'] or (p[3].dataType['name'] == 'pointer' and p[3].dataType['baseType'] == 'array')): 
        raise TypeError(f"{p.lexer.lineno}: Core Type of range clause must be array, pointer to an array, slice or map")
    p[0] = ForRangeNode(p[1], p[3])

def p_RangeList(p):
    """
    RangeList : ExpressionList ASSIGN 
                | IdentifierList DEFINE
                | 
    """
    if len(p) == 1:
        return []
    else:
        if p[2] == '=':
            for expr in p[1]:
                if expr.isAddressable is False:
                    raise TypeError(f"{p.lexer.lineno}: Operands in expression list must be addressable or map index expressions.")
        if len(p[1]) > 2:
            raise LogicalError(f"{p.lexer.lineno}: Atmost two iteration values may be provided to the range expression.")
        return p[1]


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

def genAutomaton(parser):
    path_to_root = os.environ.get('PATH_TO_ROOT')
    milestone = os.environ.get('MILESTONE')
    if path_to_root is not None:
        with open(path_to_root + "/src/Milestone" + str(milestone) + "/action.txt", "w") as f:
            for key, val in parser.action.items():
                f.writelines(f'{key} : {val}\n')

        with open(path_to_root + "/src/Milestone" + str(milestone) + "/goto.txt", "w") as f:
            for key, val in parser.goto.items():
                f.writelines(f'{key} : {val}\n')

def parse(parser, lexer, source_code):
    # Trying to handle input
    return parser.parse(source_code, lexer = lexer)

def writeOutput(parser_out, output_file):
    if parser_out is None:
        raise ValueError("Invalid output from parser.")
    with open(output_file, 'w') as fout:
        pprint.pprint(parser_out, width=10, stream=fout)


def df(root, level):
    print('    '*level + str(root) +  " - " +  str(type(root)))
    if hasattr(root, 'children') and root.children:
        for child in root.children:
            df(child, level+1)

def buildAndCompile():
    source_code = None
    path_to_source_code = sys.argv[1]
    output_file = path_to_source_code[:-2] + "output"
    with open(path_to_source_code, 'r') as f:
        source_code = f.read()
    lexer = lex.lex()
    parser, _ = yacc.yacc(debug=True)
    genAutomaton(parser)
    parser_out = parse(parser, lexer, source_code)
    # df(parser_out, 0)
    writeOutput(parser_out, output_file)
    return parser_out


if __name__ == '__main__':
    buildAndCompile()


