from cps450.oodle.analysis import DepthFirstAdapter
from cps450.oodle.node import Node
from oodle.G import G
from oodle.Declarations import *
from oodle import Type

class CodeGenx86(DepthFirstAdapter):
    ''''''
    def __init__(self):
        DepthFirstAdapter.__init__(self)
        self.typeMap = dict() #HashMap<Node,Type>
        
        self.hack_has_class = False #HACK for MiniOodle
        self.valid_scope = False
        self.asm_list = []

    def writeAsm(self, asm_str):
        self.asm_list.append(asm_str)
    
    def printAsm(self):
        for l in self.asm_list:
            print l
    
    ###########################################################################
    ## Methods to help with debugging                                         ##
    ###########################################################################
    def printFunc(self, f, node=None):
        n = (': ' + node.toString().strip()) if node else ''
        print 'CodeGenx86: ' + f.__name__ + n

    ###########################################################################
    ## Methods to help with querying/modifying the SymbolTable               ##
    ###########################################################################
    def isClassNameUsed(self, nm):
        '''Check whether class name is already used'''
        sym = G.symTab().lookup(nm)
        return sym != None
    
    def isMethodNameUsed(self, nm):
        '''Check whether method name is already used'''
        sym = G.symTab().lookup(nm)
        return sym != None
    
    def isVarNameUsed(self, nm):
        '''Check whether var name is already used'''
        ret = False
        sym = G.symTab().lookup(nm)
        if sym != None:
            ret = ret or isinstance(sym.decl(), ClassDecl)
            #ret = ret or isinstance(sym.decl(), MethodDecl) #FIXME - probably need this
            ret = ret or (isinstance(sym.decl(), VarDecl) and sym.scope() == G.symTab().getScope())
        return ret
    
    def beginScope(self, b=True):
        self.valid_scope = b
        G.symTab().beginScope()
    
    def endScope(self, b=True):
        if self.valid_scope:
            G.symTab().endScope()
        self.valid_scope = b
    
    def printTypeMap(self):
        for k in self.typeMap:
            print k,':',self.typeMap[k]
    
    def defaultIn(self, node):
        #print " in: " + node.getClass().getName()
        #raise Exception("unimplemented in-node")
        pass
    
    def defaultOut(self, node):
        #print "out: " + node.getClass().getName()
        #raise Exception("unimplemented out-node")
        pass
    
    ###########################################################################
    ## METHOD DECLARATION STUFF                                              ##
    ###########################################################################
    def outAMethod(self, node):
        self.printFunc(self.outAMethod)

    def inAMethodSig(self, node):
        '''Check method signature
           Error Conditions:
            * Method already declared'''
        self.printFunc(self.inAMethodSig, node)

    def outAMethodSig(self, node):
        self.printFunc(self.outAMethodSig, node)
    
    def outAArgList(self, node):
        self.printFunc(self.outAArgList, node)
    
    def outAArgListTail(self, node):
        self.printFunc(self.outAArgListTail, node)
    
    def outAArg(self, node):
        self.printFunc(self.outAArg, node)
    
    def outAMethodVar(self, node):
        '''Manage local method variables
           Error Conditions
            * Any local variables declared'''
        self.printFunc(self.outAMethodVar)
    
    
    ###########################################################################
    ## GENERIC VARIABLE DECLARATION STUFF (also includes method return type) ##
    ###########################################################################    
    def outAVar(self, node):
        self.printFunc(self.outAVar, node)
    
    def outAVarAssign(self, node):
        '''Manage assignment during variable declaration
           Error Conditions:
            * HACK MiniOodle: any assigment during declaration is unsupported'''
        self.printFunc(self.outAVarAssign, node)

    def outAVarType(self, node):
        self.printFunc(self.outAVarType, node)

    def outABoolType(self, node):
        self.printFunc(self.outABoolType, node)
    
    def outAIntType(self, node):
        self.printFunc(self.outAIntType, node)
        
    def outAStringType(self, node):
        '''Unsupported Feature for MiniOodle'''
        self.printFunc(self.outAStringType, node)
    
    def outAUdtType(self, node):
        self.printFunc(self.outAUdtType, node)
    
    def outAArrayType(self, node):
        self.printFunc(self.outAArrayType, node)

    ###########################################################################
    ## CLASS DECLARATION STUFF                                               ##
    ###########################################################################
    def outAKlass(self, node):
        '''Manage class declaration
           Error Conditions:
            * Mismatched class header and footer names'''
        self.printFunc(self.outAKlass)
    
    def inAKlassHeader(self, node):
        '''Push class name into SymbolTable
           Error Conditions:
            * HACK MiniOodle: only one class can be declared 
            * Class name already used'''
        self.printFunc(self.inAKlassHeader, node)
    
    def inAKlassInherits(self, node):
        '''Manage inheritance
           Error Conditions:
            * HACK MiniOodle: inheritance is an unsupported feature'''
        self.printFunc(self.inAKlassInherits, node)

    def inAKlassVar(self, node):
        self.printFunc(self.inAKlassVar)
        src = node.toString().strip()
        self.writeAsm('#' + src)

    def outAKlassVar(self, node):
        '''Manage class variables
           Error Conditions:
            * HACK MiniOodle: no class variable initialization'''
        self.printFunc(self.outAKlassVar)
        nm = '_' + node.getVar().getId().getText()
        self.writeAsm('.comm\t' + nm + ',4,4')

    ###########################################################################
    ## STATEMENT STUFF                                                       ##
    ###########################################################################
    def inAAssignStmt(self, node):
        self.printFunc(self.inAAssignStmt, node)
        src = node.toString().strip()
        self.writeAsm('#' + src)

    def outAAssignStmt(self, node):
        '''Manage 'assignment' statement
           Error Conditions:
            * rhs id must exist and be a VarDecl or (return type) MethodDecl
            * lhs and rhs must have equal types'''
        self.printFunc(self.outAAssignStmt, node)
        nm = '_' + node.getId().getText()
        self.writeAsm('popl _x')
    
    def outAIfStmt(self, node):
        '''Manage 'if' statement
           Error Conditions:
            * expr type != Type.BOOLEAN'''
        self.printFunc(self.outAIfStmt)

    def outAStmtElse(self, node):
        ''''''
        self.printFunc(self.outAStmtElse, node)

    def outALoopStmt(self, node):
        ''''''
        self.printFunc(self.outALoopStmt)

    def outACallStmt(self, node):
        ''''''
        self.printFunc(self.outACallStmt, node)

    ###########################################################################
    ## EXPRESSION STUFF                                                      ##
    ###########################################################################
    def readBinExpr(self, node):
        ''''''
        lhs = node.getE1()
        rhs = node.getE2()
        tp_lhs = self.typeMap[lhs]
        tp_rhs = self.typeMap[rhs]
        return (lhs, rhs, tp_lhs, tp_rhs)
    
    def checkBinExprTypes(self, node, tp_ls):
        ''''''
        (lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
        for t in tp_ls:
            if tp_lhs == t and tp_rhs == t:
                return tp_lhs
        return Type.NONE
    
    def outAIdExpr9(self, node):
        ''''''
        self.printFunc(self.outAIdExpr9, node)
        nm = '_' + node.getId().getText()
        self.writeAsm('pushl ' + nm)

    def outAStrExpr9(self, node):
        ''''''
        self.printFunc(self.outAStrExpr9, node)

    def outAIntExpr9(self, node):
        ''''''
        self.printFunc(self.outAIntExpr9, node)
        imm = '$' + node.getIntLit().getText()
        self.writeAsm('pushl ' + imm)

    def outATrueExpr9(self, node):
        ''''''
        self.printFunc(self.outATrueExpr9, node)

    def outAFalseExpr9(self, node):
        ''''''
        self.printFunc(self.outAFalseExpr9, node)

    def outANullExpr9(self, node):
        ''''''
        self.printFunc(self.outANullExpr9, node)

    def outAParExpr9(self, node):
        ''''''
        self.printFunc(self.outAParExpr9, node)

    def outACallExpr9(self, node):
        ''''''
        self.printFunc(self.outACallExpr9, node)

    def outAPosExpr8(self, node):
        ''''''
        self.printFunc(self.outAPosExpr8, node)

    def outANegExpr8(self, node):
        ''''''
        self.printFunc(self.outANegExpr8, node)

    def outANotExpr8(self, node):
        ''''''
        self.printFunc(self.outANotExpr8, node)

    def outAOtherExpr8(self, node):
        ''''''
        self.printFunc(self.outAOtherExpr8, node)

    def outAMultExpr5(self, node):
        ''''''
        self.printFunc(self.outAMultExpr5, node)

    def outADivExpr5(self, node):
        ''''''
        self.printFunc(self.outAMultExpr5, node)

    def outAOtherExpr5(self, node):
        ''''''
        self.printFunc(self.outAOtherExpr5, node)

    def outAAddExpr4(self, node):
        self.printFunc(self.outAAddExpr4, node)
        self.writeAsm('popl %ebx\n'
                      'popl %eax\n'
                      'addl %ebx %eax\n'
                      'pushl %eax')
    
    def outASubExpr4(self, node):
        ''''''
        self.printFunc(self.outASubExpr4, node)
        self.writeAsm('popl %ebx\n'
                      'popl %eax\n'
                      'subl %ebx %eax\n'
                      'pushl %eax')

    def outAOtherExpr4(self, node):
        ''''''
        self.printFunc(self.outAOtherExpr4, node)

    def outAConcatExpr3(self, node):
        ''''''
        self.printFunc(self.outAConcatExpr3, node)

    def outAOtherExpr3(self, node):
        ''''''
        self.printFunc(self.outAOtherExpr3, node)

    def outALteExpr2(self, node):
        '''Manage 'less than or equal' expr2 expression
           Error Conditions
            * lhs type != rhs type
            * lhs_type != (Type.INT | Type.STRING)
            * rhs_type != (Type.INT | Type.STRING)'''
        self.printFunc(self.outALteExpr2)

    def outAGteExpr2(self, node):
        '''Manage 'greater than or equal' expr2 expression
           Error Conditions
            * lhs type != rhs type
            * lhs_type != (Type.INT | Type.STRING)
            * rhs_type != (Type.INT | Type.STRING)'''
        self.printFunc(self.outAGteExpr2, node)

    def outALtExpr2(self, node):
        '''Manage 'Less than' expr2 expression
           Error Conditions
            * lhs type != rhs type
            * lhs_type != (Type.INT | Type.STRING)
            * rhs_type != (Type.INT | Type.STRING)'''
        self.printFunc(self.outALtExpr2, node)

    def outAGtExpr2(self, node):
        '''Manage 'greater than' expr2 expression
           Error Conditions
            * lhs type != rhs type
            * lhs_type != (Type.INT | Type.STRING)
            * rhs_type != (Type.INT | Type.STRING)'''
        self.printFunc(self.outAGtExpr2, node)

    def outAEqExpr2(self, node):
        '''Manage 'equal to' expr2 expression
           Error Conditions
            * lhs type != rhs type
            * lhs_type != (Type.INT | Type.STRING)
            * rhs_type != (Type.INT | Type.STRING)'''
        self.printFunc(self.outAEqExpr2, node)

    def outAOtherExpr2(self, node):
        '''Manage 'other' expr2 expression
           Error Conditions
            * NONE'''
        self.printFunc(self.outAOtherExpr2, node)
    
    def outAAndExpr1(self, node):
        '''Manage 'and' expr1 expression
           Error Conditions
            * lhs type != Type.BOOLEAN and rhs type != Type.BOOLEAN'''
        self.printFunc(self.outAAndExpr1, node)

    def outAOtherExpr1(self, node):
        '''Manage 'other' expr1 expression
           Error Conditions
            * NONE'''
        self.printFunc(self.outAOtherExpr1, node)
    
    def outAOrExpr(self, node):
        '''Manage 'or' expr expression
           Error Conditions
            * lhs type != Type.BOOLEAN and rhs type != Type.BOOLENA'''
        self.printFunc(self.outAAndExpr1, node)

    def outAOtherExpr(self, node):
        '''Manage 'other' expr expression
           Error Conditions
            * NONE'''
        self.printFunc(self.outAOtherExpr, node)

    def outAExprList(self, node):
        '''Manage 'expr_list'
           Error Conditions
            * NONE
           Special Features
            * puts the entire list into the typeMap'''
        self.printFunc(self.outAExprList, node)

    ###########################################################################
    ## MISCELLANEOUS STUFF                                                   ##
    ###########################################################################
    def outACall(self, node):
        '''Manage a method 'call'
           Error Conditions
            * object does not contain method id
            * method id does not exist in 'me'
            * wrong number of parameters
            * wrong parameter types'''
        self.printFunc(self.outACall, node)
    
    