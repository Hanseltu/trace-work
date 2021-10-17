# -*- coding: utf-8 -*
from __future__ import print_function
from __future__ import division
import sys,random,os,shutil,gc,subprocess,datetime,re,time,signal,shutil,math,copy,os.path
import numpy as np

sys.path.extend(['.', '..'])
sys.path.append(r'/home/tangyixuan/pycparser-master/pycparser')

#replace
pypath = '/home/tangyixuan/testcgov/testshell/anewmethod/Hermes/Hermes-CCS/'
resultpath = '/media/tangyixuan/xuaner/testdeleteprogramserrorInformation/anewmethod/Hermes/CCS1-8-2/'
warningfile = 'hermes-warning-2.txt'
warningflagfile = 'hermes-warningflag-2.txt'
timefile = 'hermers-time-2.txt'

codesnippetpath = '/media/tangyixuan/xuaner/csmith-program/Hermescodesnippet/'

from c_ast import NodeVisitor
from pycparser import parse_file,c_generator,c_ast
warningflag=set()

deleterule = []
nodelist = []
variablelist = {}
global_variable = {}
global_function = {}
allcompilablecout = 0
uncompilablecount = 0
seedtestcount = 0
inlinefunction = []


class IfVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_If(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			#flagdelete = 1
			if flagdelete == 1:
				#print("////////////////////////")
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#print("1111111111111111111111111111")
					opif = random.randint(1,3)
					#opif = 3
					if opif == 1:
						if node.cond:
							print("the entire cond in if is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.If.cond')	
					elif opif == 2:
						if node.iftrue:
							print("the entire iftrue in if is ready to delete...")
							node.iftrue = None
							self.count += 1
							deleterule.append('pycparser.c_ast.If.iftrue')
					else:
						if node.iffalse:
							print("the entire iffalse in if is ready to delete...")
							node.iffalse = None
							self.count += 1
							deleterule.append('pycparser.c_ast.If.iffalse')

class TernaryOpVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_TernaryOp(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opif = random.randint(1,3)
					if opif == 1:
						if node.cond:
							print("the entire cond in TernaryOp is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.TernaryOp.cond')
					elif opif == 2:
						if node.iftrue:
							print("the entire iftrue in TernaryOp is ready to delete...")
							node.iftrue = None
							self.count += 1
							deleterule.append('pycparser.c_ast.TernaryOp.iftrue')
					else:
						if node.iffalse:
							print("the entire iffalse in TernaryOp is ready to delete...")
							node.iffalse = None
							self.count += 1
							deleterule.append('pycparser.c_ast.TernaryOp.iffalse')

class StructVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Struct(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opstruct = random.randint(1,2)
					if opstruct ==1:
						if node.name:
							print("the name in struct is ready to delete...")
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Struct.name')
					else:
						if node.decls:
							#node.decls.children are list
							print("the entire decl of struct is ready to delete...")
							node.decls = []
							self.count += 1
							deleterule.append('pycparser.c_ast.Struct.decls')

class UnionVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Union(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opstruct = random.randint(1,2)
					if opstruct ==1:
						if node.name:
							print("the name in struct is ready to delete...")
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Union.name')
					else:
						if node.decls:
							#node.decls.children are list	
							print("the entire decl of struct is ready to delete...")
							node.decls = []
							self.count += 1
							deleterule.append('pycparser.c_ast.Union.decls')

class DeclVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Decl(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opdecl = random.randint(1,4)
					if opdecl == 1:
						if node.name:
							if '__undefined' not in node.name:
								node.name = ''
								self.count += 1
								deleterule.append('pycparser.c_ast.Decl.name')
					elif opdecl == 2:
						if node.type:
							print("the entire type in decl is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Decl.type')
					elif opdecl == 3:
						if node.init:
							print("the entire init in decl is ready to delete...")
							node.init = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Decl.init')
					else:
						if node.bitsize:
							print("the entire bitsize in decl is ready to delete...")
							node.bitsize = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Decl.bitsize')

class ArrayDeclVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_ArrayDecl(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					oparraydecl = random.randint(1,3)
					if oparraydecl == 1:
						if node.type:
							print("the entire type in arraydecl is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.ArrayDecl.type')
					elif oparraydecl == 2:
						if node.dim:
							print("the entire dim in arraydecl is ready to delete...")
							node.dim = None
							self.count += 1
							deleterule.append('pycparser.c_ast.ArrayDecl.dim')
					else:
						if node.dim_quals:
							node.dim_quals = None
							self.count += 1
							deleterule.append('pycparser.c_ast.ArrayDecl.dim_quals')


class ArrayRefVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_ArrayRef(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					oparayref = random.randint(1,2)
					if oparayref == 1:
						if node.name:
							print("the entire name in ArrayRef is ready to delete...")
							node.name = None
							self.count += 1
							deleterule.append('pycparser.c_ast.ArrayRef.name')
					else:
						if node.subscript:
							print("the entire subscript in ArrayRef is ready to delete...")
							node.subscript = None
							self.count += 1
							deleterule.append('pycparser.c_ast.ArrayRef.subscript')

class BinaryOpVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_BinaryOp(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opBinaryOp = random.randint(1,3)
					if opBinaryOp == 1:
						if node.op:
							node.op = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.BinaryOp.op')
					elif opBinaryOp == 2:
						if node.left:
							print("the entire left in BinaryOp is ready to delete...")
							node.left = None
							self.count += 1
							deleterule.append('pycparser.c_ast.BinaryOp.left')
					else:
						if node.right:
							print("the entire right in BinaryOp is ready to delete...")
							node.right = None
							self.count += 1
							deleterule.append('pycparser.c_ast.BinaryOp.right')

class AssignmentVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Assignment(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opassignment = random.randint(1,3)
					if opassignment == 1:
						if node.op:
							node.op = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Assignment.op')
					elif opassignment == 2:
						if node.lvalue:
							print("the entire lvalue in Assignment is ready to delete...")
							node.lvalue = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Assignment.lvalue')
					else:
						if node.rvalue:
							print("the entire rvalue in Assignment is ready to delete...")
							node.rvalue = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Assignment.rvalue')

class CompoundVisitor(NodeVisitor):
#one operation:[[block_items]]
	def __init__(self):
		self.count = 0
	def visit_Compound(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.block_items:
						print("the entire block_items of Compound is ready to delete...")
						node.block_items = []
						self.count += 1
						deleterule.append('pycparser.c_ast.Compound.block_items')


class CompoundLiteralVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_CompoundLiteral(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: ['type', 'init' ]
					opCompoundLiteral = random.randint(1,2)
					if opCompoundLiteral == 1:
						if node.type:
							print("the entire type in CompoundLiteral is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.CompoundLiteral.type')
					else:
						if node.init:
							print("the entire init of CompoundLiteral is ready to delete...")
							node.init = None
							self.count += 1
							deleterule.append('pycparser.c_ast.CompoundLiteral.init')

class DeclListVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_DeclList(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.decls:
						print("the entire decls of DeclList is ready to delete...")
						node.decls = []
						self.count += 1
						deleterule.append('pycparser.c_ast.DeclList.decls')

class DefaultVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Default(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.stmts:
						print("the entire stmts of Default is ready to delete...")
						node.stmts = []
						self.count += 1
						deleterule.append('pycparser.c_ast.Default.stmts')


class DoWhileVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_DoWhile(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opDoWhile = random.randint(1,2)
					if opDoWhile == 1:
						if node.cond:
							print("the entire cond in DoWhile is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.DoWhile.cond')
					else:
						if node.stmt:
							print("the entire stmt of DoWhile is ready to delete...")
							node.stmt = None
							self.count += 1
							deleterule.append('pycparser.c_ast.DoWhile.stmt')

class SwitchVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Switch(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opDoWhile = random.randint(1,2)
					if opDoWhile == 1:
						if node.cond:
							print("the entire cond in Switch is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Switch.cond')
					else:
						if node.stmt:
							print("the entire stmt of Switch is ready to delete...")
							node.stmt = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Switch.stmt')

class WhileVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_While(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opDoWhile = random.randint(1,2)
					if opDoWhile == 1:
						if node.cond:
							print("the entire cond in While is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.While.cond')
					else:
						if node.stmt:
							print("the entire stmt of While is ready to delete...")
							node.stmt = None
							self.count += 1
							deleterule.append('pycparser.c_ast.While.stmt')


class EnumVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Enum(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					opEnum = random.randint(1,2)
					if opEnum == 1:
						if node.name:
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Enum.name')
					else:
						if node.values:
							print("the entire values in Enum is ready to delete...")
							node.values = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Enum.values')

class EnumeratorVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Enumerator(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: 'name', ['value']
					opEnumerator = random.randint(1,2)
					if opEnumerator == 1:
						if node.name:
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Enumerator.name')
					else:
						if node.value:
							print("the entire value in Enumerator is ready to delete...")
							node.value = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Enumerator.value')

class EnumeratorListVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_EnumeratorList(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.enumerators:
						print("the entire enumerators of EnumeratorList is ready to delete...")
						node.enumerators = []
						self.count += 1
						deleterule.append('pycparser.c_ast.EnumeratorList.enumerators')

class ExprListVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_ExprList(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.exprs:
						print("the entire exprs of ExprList is ready to delete...")
						node.exprs = []
						self.count += 1
						deleterule.append('pycparser.c_ast.ExprList.exprs')

class InitListVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_InitList(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.exprs:
						print("the entire exprs of InitList is ready to delete...")
						node.exprs = []
						self.count += 1
						deleterule.append('pycparser.c_ast.InitList.exprs')

class FileASTVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FileAST(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					if node.ext:	
						print("the entire ext of FileAST is ready to delete...")
						node.ext = []
						self.count += 1
						deleterule.append('pycparser.c_ast.FileAST.ext')

class ForVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_For(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#four operations: ['init', 'cond', 'next', 'stmt' ]
					opFor = random.randint(1,4)
					#opFor = 5
					if opFor == 1:
						if node.init:
							print("the entire init in For is ready to delete...")
							node.init = None
							self.count += 1
							deleterule.append('pycparser.c_ast.For.init')
					elif opFor == 2:
						if node.cond:
							print("the entire cond of For is ready to delete...")
							node.cond = None
							self.count += 1
							deleterule.append('pycparser.c_ast.For.cond')
					elif opFor == 3:
						if node.next:
							print("the entire next of For is ready to delete...")
							node.next = None
							self.count += 1
							deleterule.append('pycparser.c_ast.For.next')
					else:
						if node.stmt:
							print("the entire stmt of For is ready to delete...")
							node.stmt = None
							self.count += 1
							deleterule.append('pycparser.c_ast.For.stmt')


class FuncCallVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncCall(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: ['name', 'args' ]
					opFuncCall = random.randint(1,2)
					if opFuncCall == 1:
						if node.name:
							print("the entire name in FuncCall is ready to delete...")
							node.name = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncCall.name')
					else:
						if node.args:
							print("the entire args of FuncCall is ready to delete...")
							node.args = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncCall.args')

class FuncDeclVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncDecl(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: ['args', 'type' ]
					opFuncDecl = random.randint(1,2)
					if opFuncDecl == 1:
						if node.args:
							print("the entire args in FuncDecl is ready to delete...")
							node.args = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncDecl.args')
					else:
						if node.type:
							print("the entire type of FuncDecl is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncDecl.type')

class FuncDefVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncDef(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#three operations: [decl', 'body' ][['param_decls']]
					opFuncDef = random.randint(1,3)
					if opFuncDef == 1:
						if node.decl:
							print("the entire decl in FuncDef is ready to delete...")
							#print('the entire decl is :' + str(generatorcode.visit(node.decl)))
							node.decl = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncDef.decl')
					elif opFuncDef == 2:
						if node.body:
							print("the entire body of FuncDef is ready to delete...")
							#print('the entire body is :' + str(generatorcode.visit(node.body)))
							node.body = None
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncDef.body')
					else:
						if node.param_decls:
							print("the entire param_decls of FuncDef is ready to delete...")
							#print('the entire param_decls is :' + str(generatorcode.visit(node.param_decls)))
							node.param_decls = []
							self.count += 1
							deleterule.append('pycparser.c_ast.FuncDef.param_decls')
class GotoVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Goto(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operation: name
					if node.name:
						node.name = ''
						self.count += 1
						deleterule.append('pycparser.c_ast.Goto.name')

class IDVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_ID(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operation: name
					if node.name:
						node.name = ''
						self.count += 1
						deleterule.append('pycparser.c_ast.ID.name')
class IdentifierTypeVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_IdentifierType(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operation: names
					if node.names:
						node.names = ''
						self.count += 1
						deleterule.append('pycparser.c_ast.IdentifierType.names')

class LabelVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Label(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: 'name', ['stmt']
					opLabel = random.randint(1,2)
					if opLabel == 1:
						if node.name:
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Label.name')
					else:
						if node.stmt:
							print("the entire stmt in Label is ready to delete...")
							node.stmt = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Label.stmt')
class CaseVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Case(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: ['expr'], [['stmts']] 
					opcase = random.randint(1,2)
					if opcase == 1:
						if node.expr:
							print("the entire expr in case is ready to delete...")
							node.expr = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Case.expr')
					else:
						if node.stmts:
							print("the entire stmts of Case is ready to delete...")
							node.stmts = []
							self.count += 1
							deleterule.append('pycparser.c_ast.Case.stmts')
class NamedInitializerVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_NamedInitializer(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: 'name', [['expr' ]]
					opNamedInitializer = random.randint(1,2)
					if opcase == 1:
						if node.name:
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.NamedInitializer.name')
					else:
						if node.expr:
							print("the entire expr of NamedInitializer is ready to delete...")
							node.expr = []
							self.count += 1
							deleterule.append('pycparser.c_ast.NamedInitializer.expr')
class ParamListVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_ParamList(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operation: [['params']]
					if node.params:
						print("the entire params of ParamList is ready to delete...")
						node.params = []
						self.count += 1
						deleterule.append('pycparser.c_ast.ParamList.params')

class PtrDeclVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_PtrDecl(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: 'quals', ['type']
					if node.type:
						print("the entire type in PtrDecl is ready to delete...")
						node.type = None
						self.count += 1
						deleterule.append('pycparser.c_ast.PtrDecl.type')

class ReturnVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Return(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operations: ['expr']
					if node.expr:
						print("the entire expr in Return is ready to delete...")
						node.expr = None
						self.count += 1
						deleterule.append('pycparser.c_ast.Return.expr')

class StructRefVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_StructRef(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#three operations:'type', [ 'name', 'field']
					opStructRef = random.randint(1,3)
					if opStructRef == 1:
						if node.type:
							node.type = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.StructRef.type')
					elif opStructRef == 2:
						if node.name:
							print("the entire name in StructRef is ready to delete...")
							node.name = None
							self.count += 1
							deleterule.append('pycparser.c_ast.StructRef.name')
					else:
						if node.field:
							print("the entire field in StructRef is ready to delete...")
							node.field = None
							self.count += 1
							deleterule.append('pycparser.c_ast.StructRef.field')
class TypeDeclVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_TypeDecl(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#three operations: 'declname', 'quals', ['type']
					opTypeDecl = random.randint(1,2)
					if opTypeDecl == 1:
						if node.declname:
							node.declname = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.TypeDecl.declname')
					else:
						if node.type:
							print("the entire type in TypeDecl is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.TypeDecl.type')

class TypenameVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Typename(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#three operations: 'name', 'quals', ['type']
					opTypename = random.randint(1,2)
					if opTypename == 1:
						if node.name:
							node.name = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.Typename.name')
					else:
						if node.type:
							print("the entire type in Typename is ready to delete...")
							node.type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Typename.type')
class UnaryOpVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_UnaryOp(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: 'op', ['expr']
					opUnaryOp = random.randint(1,2)
					if opUnaryOp == 1:
						if node.op:
							node.op = ''
							self.count += 1
							deleterule.append('pycparser.c_ast.UnaryOp.op')
					else:
						if node.expr:
							print("the entire expr in UnaryOp is ready to delete...")
							node.expr = None
							self.count += 1
							deleterule.append('pycparser.c_ast.UnaryOp.expr')

class PragmaVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Pragma(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#one operations: 'string'
					if node.string:
						node.string = ''
						self.count += 1
						deleterule.append('pycparser.c_ast.Pragma.string')

class CastVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Cast(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					#two operations: ['to_type', 'expr']
					opCast = random.randint(1,2)
					if opCast == 1:
						if node.to_type:
							print("the entire to_type in Cast is ready to delete...")
							node.to_type = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Cast.to_type')
					else:
						if node.expr:
							print("the entire expr of Cast is ready to delete...")
							node.expr = None
							self.count += 1
							deleterule.append('pycparser.c_ast.Cast.expr')

class ConstantVisitor(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Constant(self, node):
		if self.count < 1:
			flagdelete = random.randint(0,1)
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				flag = coverage(deletelistcodeline)
				if flag:
					self.count += 1
					#two operations: 'type', 'value'
					node = None
					deleterule.append('pycparser.Constant')




class FuncDefVisitor1_1(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncDef(self, node):
		global variablelist
		if self.count < 1:
			flagdelete = random.randint(0,1)
			#1:insert 0:no
			#flagdelete = 1
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				#print(str(deletelistcodeline))
				#for indexdeletelistcodeline in range(0,len(deletelistcodeline)):
				#	if deletelistcodeline[indexdeletelistcodeline] == '':
				#		del deletelistcodeline[indexdeletelistcodeline]
				comparedeletelistcodeline = deletelistcodeline
				functiontitle = re.split('[()&*;, ]',comparedeletelistcodeline[0])
				whetherfunc = False
				#for i in range(0,len(comparedeletelistcodeline)):
				#	print(comparedeletelistcodeline[i])
				for i in range(0,len(functiontitle)):
					if functiontitle[i].startswith('func_'):
						whetherfunc = True
						break
				if whetherfunc:
					#print('00000000000000000000000000000')
					#print(str(comparedeletelistcodeline))
					#print('00000000000000000000000000000')
					#print('00000000000000000000000000000')
					#print(str(deletelistcodeline))
					#print('00000000000000000000000000000')
					countinsert = 0
					flag = False
					selectlocal = random.randint(1,len(deletelistcodeline)-2)
					#print('99999999999999999999999999999')
					#print(str(selectlocal))
					#print('99999999999999999999999999999')

					while True:
						if comparedeletelistcodeline[selectlocal].replace(' ','') != '}' and comparedeletelistcodeline[selectlocal].replace(' ','') != '':
							#print('the line is : '+str(selectlocal)+' : '+comparedeletelistcodeline[selectlocal])
							flag = True
							break
						else:
							#print('not expected line: '+comparedeletelistcodeline[selectlocal])
							selectlocal = random.randint(1,len(deletelistcodeline)-2)
							#print('retry to select: '+str(selectlocal))

					'''
					while True:
						if comparedeletelistcodeline[selectlocal].replace(' ','') != '{' and  comparedeletelistcodeline[selectlocal].replace(' ','') != '}' and comparedeletelistcodeline[selectlocal].replace(' ','') != '':
							#print('the line is : '+str(selectlocal)+' : '+comparedeletelistcodeline[selectlocal])
							flag = True
							break
						else:
							#print('not expected line: '+comparedeletelistcodeline[selectlocal])
							selectlocal = random.randint(2,len(deletelistcodeline)-2)
							#print('retry to select: '+str(selectlocal))
					'''
					if True:
						self.count += 1
						nodevisittypedel = TypeDeclVisitor1()
						nodevisittypedel.visit(node)
						nodevisitlabel = LabelVisitor1()
						nodevisitlabel.visit(node)
						#type
						for key in variablelist.keys():
							if key.startswith('l_'):
								for t in range(0,len(deletelistcodeline)):
									if key in deletelistcodeline[t]:
										substring1 = deletelistcodeline[t][:deletelistcodeline[t].index(key)]
										numberptr = substring1.count('*')
										realptr = ''
										if numberptr != 0:
											for u in range(0,numberptr):
												realptr = realptr + '*'
										variablelist[key] = variablelist[key] + realptr
										substring1 = deletelistcodeline[t][deletelistcodeline[t].index(key)+len(key):]
										if substring1.startswith('['):
											listwords = substring1.split(' ')
											numberweidu = listwords[0].count('[')
											realptr1 = ''
											if numberweidu != 0:
												for u in range(0,numberweidu):
													realptr1 = realptr1 + '[]'
											variablelist[key] = variablelist[key] + realptr1
											break
										else:
											break

						#decide front or later : 0: front
						insertlocal = 0
						#localformer = random.randint(0,1)
						localformer = 1
						blank = []
						copyselectlocal = selectlocal
						print('we begin to calculate the number of blank')
						#print('localformer is : '+str(localformer))
						if localformer == 0:
							#print('1')
							insertlocal = selectlocal-1
							for t in range(0,len(deletelistcodeline[selectlocal])):
								if deletelistcodeline[selectlocal][t] == ' ':
									blank.append(' ')
								else:
									break
						else:
							insertlocal = selectlocal+1
							if deletelistcodeline[selectlocal+1].replace(' ','') == '{':
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
								blank.append('  ')
							else:
								#print('3')
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
						print('---blank number----'+str(len(blank)))
						#clear variablelist
						for localkey in list(variablelist.keys()):
							wetherlocalvariable = False
							for h in range(0,insertlocal):
								if localkey in deletelistcodeline[h]:
									wetherlocalvariable = True
									break
							if wetherlocalvariable is False:
								del variablelist[localkey]
						for localkey in list(variablelist.keys()):
							if localkey.startswith('func_'):
								del variablelist[localkey]
						#print(str(variablelist))
						#select what type of structure is ready to insert
						while(True):
							
							renamecode = replacename('iffalse')
							if len(renamecode) != 0:
								print('insert iffalse')
								#for i in range(0,len(renamecode)):
								#	print(renamecode[i])
								#print('yyyyyyyyyyyyyyyyyyy')
								for b in range(1,len(renamecode)):
									#print('111111111111111')
									#print(str(insertlocal))
									#print('111111111111111')
									deletelistcodeline.insert(insertlocal,''.join(blank)+renamecode[b])
									insertlocal += 1
								break
							else:
								countinsert += 1
								if countinsert > 10:
									#print('countinsert > 10')
									#print('2222222222222222')
									#print(str(insertlocal))
									#print('2222222222222222')
									deletelistcodeline.insert(insertlocal,''.join(blank)+'if(0)')
									break
							
						#print('ooooooooooooooooooooooooooooooo')
						for u in range(0,len(deletelistcodeline)):
							print(deletelistcodeline[u])
							inlinefunction.append(deletelistcodeline[u])
						#print('ooooooooooooooooooooooooooooooo')






class FuncDefVisitor1(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncDef(self, node):
		global variablelist
		if self.count < 1:
			flagdelete = random.randint(0,1)
			#1:insert 0:no
			#flagdelete = 1
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				comparedeletelistcodeline = deletelistcodeline
				functiontitle = wordlist = re.split('[()&*;, ]',comparedeletelistcodeline[0])
				whetherfunc = False
				#for i in range(0,len(comparedeletelistcodeline)):
				#	print(comparedeletelistcodeline[i])
				for i in range(0,len(functiontitle)):
					if functiontitle[i].startswith('func_'):
						whetherfunc = True
						break
				if whetherfunc:
					flag = False
					selectlocal = random.randint(2,len(deletelistcodeline)-2)
					while True:
						if comparedeletelistcodeline[selectlocal].replace(' ','') != '{' and  comparedeletelistcodeline[selectlocal].replace(' ','') != '}' and comparedeletelistcodeline[selectlocal].replace(' ','') != '':
							#print('the line is : '+str(selectlocal)+' : '+comparedeletelistcodeline[selectlocal])
							flag = True
							break
						else:
							#print('not expected line: '+comparedeletelistcodeline[selectlocal])
							selectlocal = random.randint(2,len(deletelistcodeline)-2)
							#print('retry to select: '+str(selectlocal))
				
					if flag:
						self.count += 1
						nodevisittypedel = TypeDeclVisitor1()
						nodevisittypedel.visit(node)
						nodevisitlabel = LabelVisitor1()
						nodevisitlabel.visit(node)
						#type
						for key in variablelist.keys():
							if key.startswith('l_'):
								for t in range(0,len(deletelistcodeline)):
									if key in deletelistcodeline[t]:
										substring1 = deletelistcodeline[t][:deletelistcodeline[t].index(key)]
										numberptr = substring1.count('*')
										realptr = ''
										if numberptr != 0:
											for u in range(0,numberptr):
												realptr = realptr + '*'
										variablelist[key] = variablelist[key] + realptr
										substring1 = deletelistcodeline[t][deletelistcodeline[t].index(key)+len(key):]
										if substring1.startswith('['):
											listwords = substring1.split(' ')
											numberweidu = listwords[0].count('[')
											realptr1 = ''
											if numberweidu != 0:
												for u in range(0,numberweidu):
													realptr1 = realptr1 + '[]'
											variablelist[key] = variablelist[key] + realptr1
											break
										else:
											break

						#decide front or later : 0: front
						insertlocal = 0
						localformer = random.randint(0,1)
						blank = []
						copyselectlocal = selectlocal
						print('we begin to calculate the number of blank')
						#print('localformer is : '+str(localformer))
						if localformer == 0:
							#print('1')
							insertlocal = selectlocal
							for t in range(0,len(deletelistcodeline[selectlocal])):
								if deletelistcodeline[selectlocal][t] == ' ':
									blank.append(' ')
								else:
									break
						else:
							
							if deletelistcodeline[selectlocal+1].replace(' ','') == '{':
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
								blank.append('  ')
							else:
								#print('3')
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
						print('---blank number----'+str(len(blank)))
						#clear variablelist
						for localkey in list(variablelist.keys()):
							wetherlocalvariable = False
							for h in range(0,insertlocal):
								if localkey in deletelistcodeline[h]:
									wetherlocalvariable = True
									break
							if wetherlocalvariable is False:
								del variablelist[localkey]
						for localkey in list(variablelist.keys()):
							if localkey.startswith('func_'):
								del variablelist[localkey]
						#print(str(variablelist))
						#select what type of structure is ready to insert
						while(True):
							renamecode = replacename('iffalse')
							if len(renamecode) != 0:
								print('insert iffalse')
								#for i in range(0,len(renamecode)):
								#	print(renamecode[i])
								#print('yyyyyyyyyyyyyyyyyyy')
								for b in range(1,len(renamecode)):
									deletelistcodeline.insert(insertlocal,''.join(blank)+renamecode[b])
									insertlocal += 1
								break

						#print('ooooooooooooooooooooooooooooooo')
						for u in range(0,len(deletelistcodeline)):
						#	print(deletelistcodeline[u])
							inlinefunction.append(deletelistcodeline[u])
						#print('ooooooooooooooooooooooooooooooo')



class FuncDefVisitor2_1(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_FuncDef(self, node):
		global variablelist
		if self.count < 1:
			flagdelete = random.randint(0,1)
			#1:insert 0:no
			#flagdelete = 1
			if flagdelete == 1:
				generatorcode = c_generator.CGenerator()
				deletelistcodeline = generatorcode.visit(node).splitlines()
				#print(str(deletelistcodeline))
				#for indexdeletelistcodeline in range(0,len(deletelistcodeline)):
				#	if deletelistcodeline[indexdeletelistcodeline] == '':
				#		del deletelistcodeline[indexdeletelistcodeline]
				comparedeletelistcodeline = deletelistcodeline
				functiontitle = re.split('[()&*;, ]',comparedeletelistcodeline[0])
				whetherfunc = False
				#for i in range(0,len(comparedeletelistcodeline)):
				#	print(comparedeletelistcodeline[i])
				for i in range(0,len(functiontitle)):
					if functiontitle[i].startswith('func_'):
						whetherfunc = True
						break
				if whetherfunc:
					#print('00000000000000000000000000000')
					#print(str(comparedeletelistcodeline))
					#print('00000000000000000000000000000')
					#print('00000000000000000000000000000')
					#print(str(deletelistcodeline))
					#print('00000000000000000000000000000')
					countinsert = 0
					flag = False
					selectlocal = random.randint(1,len(deletelistcodeline)-2)
					#print('99999999999999999999999999999')
					#print(str(selectlocal))
					#print('99999999999999999999999999999')

					while True:
						if comparedeletelistcodeline[selectlocal].replace(' ','') != '}' and comparedeletelistcodeline[selectlocal].replace(' ','') != '':
							#print('the line is : '+str(selectlocal)+' : '+comparedeletelistcodeline[selectlocal])
							flag = True
							break
						else:
							#print('not expected line: '+comparedeletelistcodeline[selectlocal])
							selectlocal = random.randint(1,len(deletelistcodeline)-2)
							#print('retry to select: '+str(selectlocal))

					'''
					while True:
						if comparedeletelistcodeline[selectlocal].replace(' ','') != '{' and  comparedeletelistcodeline[selectlocal].replace(' ','') != '}' and comparedeletelistcodeline[selectlocal].replace(' ','') != '':
							#print('the line is : '+str(selectlocal)+' : '+comparedeletelistcodeline[selectlocal])
							flag = True
							break
						else:
							#print('not expected line: '+comparedeletelistcodeline[selectlocal])
							selectlocal = random.randint(2,len(deletelistcodeline)-2)
							#print('retry to select: '+str(selectlocal))
					'''
					if True:
						self.count += 1
						nodevisittypedel = TypeDeclVisitor1()
						nodevisittypedel.visit(node)
						nodevisitlabel = LabelVisitor1()
						nodevisitlabel.visit(node)
						#type
						for key in variablelist.keys():
							if key.startswith('l_'):
								for t in range(0,len(deletelistcodeline)):
									if key in deletelistcodeline[t]:
										substring1 = deletelistcodeline[t][:deletelistcodeline[t].index(key)]
										numberptr = substring1.count('*')
										realptr = ''
										if numberptr != 0:
											for u in range(0,numberptr):
												realptr = realptr + '*'
										variablelist[key] = variablelist[key] + realptr
										substring1 = deletelistcodeline[t][deletelistcodeline[t].index(key)+len(key):]
										if substring1.startswith('['):
											listwords = substring1.split(' ')
											numberweidu = listwords[0].count('[')
											realptr1 = ''
											if numberweidu != 0:
												for u in range(0,numberweidu):
													realptr1 = realptr1 + '[]'
											variablelist[key] = variablelist[key] + realptr1
											break
										else:
											break

						#decide front or later : 0: front
						insertlocal = 0
						#localformer = random.randint(0,1)
						localformer = 1
						blank = []
						copyselectlocal = selectlocal
						print('we begin to calculate the number of blank')
						#print('localformer is : '+str(localformer))
						if localformer == 0:
							#print('1')
							insertlocal = selectlocal-1
							for t in range(0,len(deletelistcodeline[selectlocal])):
								if deletelistcodeline[selectlocal][t] == ' ':
									blank.append(' ')
								else:
									break
						else:
							insertlocal = selectlocal+1
							if deletelistcodeline[selectlocal+1].replace(' ','') == '{':
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
								blank.append('  ')
							else:
								#print('3')
								for t in range(0,len(deletelistcodeline[selectlocal])):
									if deletelistcodeline[selectlocal][t] == ' ':
										blank.append(' ')
									else:
										break
						print('---blank number----'+str(len(blank)))
						#clear variablelist
						for localkey in list(variablelist.keys()):
							wetherlocalvariable = False
							for h in range(0,insertlocal):
								if localkey in deletelistcodeline[h]:
									wetherlocalvariable = True
									break
							if wetherlocalvariable is False:
								del variablelist[localkey]
						for localkey in list(variablelist.keys()):
							if localkey.startswith('func_'):
								del variablelist[localkey]
						#print(str(variablelist))
						#select what type of structure is ready to insert
						while(True):
							
							renamecode = replacename('iftrue')
							if len(renamecode) != 0:
								print('insert iftrue')
								#for i in range(0,len(renamecode)):
								#	print(renamecode[i])
								#print('yyyyyyyyyyyyyyyyyyy')
								for b in range(1,len(renamecode)):
									#print('111111111111111')
									#print(str(insertlocal))
									#print('111111111111111')
									deletelistcodeline.insert(insertlocal,''.join(blank)+renamecode[b])
									insertlocal += 1
								break
							else:
								countinsert += 1
								if countinsert > 10:
									#print('countinsert > 10')
									#print('2222222222222222')
									#print(str(insertlocal))
									#print('2222222222222222')
									deletelistcodeline.insert(insertlocal,''.join(blank)+'if(1)')
									break
							
						#print('ooooooooooooooooooooooooooooooo')
						for u in range(0,len(deletelistcodeline)):
							print(deletelistcodeline[u])
							inlinefunction.append(deletelistcodeline[u])
						#print('ooooooooooooooooooooooooooooooo')

					
class LabelVisitor1(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_Label(self, node):
		pattern1=re.compile("name=\'(.*?)\'")
		decllist=pattern1.findall(str(node))
		if len(decllist) != 0:
			variablelist[decllist[0]] = 'Label'

class TypeDeclVisitor1(NodeVisitor):
	def __init__(self):
		self.count = 0
	def visit_TypeDecl(self, node):
		global variablelist
		#print('-----------------------')

		generatorcode = c_generator.CGenerator()
		deletelistcodeline = str(generatorcode.visit(node))
		#print(deletelistcodeline) #uint16_t
		pattern1=re.compile("declname=\'(.*?)\'")
		decllist=pattern1.findall(str(node))
		if len(decllist) != 0:
			#print(decllist[0])
			variablelist[decllist[0]] = deletelistcodeline


def run_cmd_save_errorInformation(cmd,writepath):
	result_str=''
	#process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	error_f = process.stderr
	errors = error_f.read()
	#print(errors)
	if errors:
		result_str = errors
	if error_f:
		error_f.close()
	f = open(writepath,'wb+')
	f.write(result_str)
	f.close()

def timeout(cmd):
	"""call shell-command and either return its output or kill it
	if it doesn't normally exit within timeout seconds and return None"""
	start = datetime.datetime.now()
	process = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#	while process.poll() is None:
#		time.sleep(0.2)
#		now = datetime.datetime.now()
#		if (now - start).seconds > 5:
#			os.kill(process.pid, signal.SIGKILL)
#			os.waitpid(-1, os.WNOHANG)
#			return None
	return process.stdout.readlines()

def read_error_wrong_Information(rewritepath,regex):
	f = open(rewritepath)
	line = f.readline()
	mydict = {}
	while line: 
		if regex in line:
			strlist = line.split(':')
			if strlist[1].isdigit() and strlist[2].isdigit():
				locationError = strlist[1] + ":" + strlist[2]
				if locationError in mydict:
					count = mydict[locationError]
					count = count + 1
					mydict[locationError] = count
				else:
					mydict[locationError] = 1
			elif strlist[1].isdigit():
				location = strlist[1]
				if location in mydict:
					count1 = mydict[location]
					count1 = count1 + 1
					mydict[location] = count1
				else:
					mydict[location] = 1			
			
		line = f.readline()
	f.close()
	#print("---------------------")
	#mydictItems = mydict.items()
	#print(list(mydictItems))
	return mydict

def whethertimeout(rewritepath):
	flagtimeout = False
	f = open(rewritepath)
	lines = f.readlines()
	if lines == ' ':
		#crash
		flagtimeout = True
	f.close()
	return flagtimeout

def whethercrash(rewritepath):
	flagcrash = False
	f = open(rewritepath)
	lines = f.readlines()
	for j in range(len(lines)):
		if 'submit a full bug report' in lines[j]:
			flagcrash = True
	f.close()
	return flagcrash
	
def readcrashfile(rewritepath):
	line = ' '
	f1 = open(rewritepath)
	lines = f1.readlines()
	if len(lines) > 0:
		line = lines[len(lines)-1]
	return line
def extract_globle_code(originalpath,extractvariable,extractfunction):
	extractcodevariable = []
	extractcodefunction = []
	originalcode = read_coverage(originalpath)
	for i in range(0,len(originalcode)):
		if 'func_' not in originalcode[i]:
			extractcodevariable.append(originalcode[i])
		elif 'func_' in originalcode[i] and '{' not in originalcode[i+1]:		
			extractcodefunction.append(originalcode[i])
		else:
			break
	fwrite = open(extractvariable,'a+')
	for w in range(0, len(extractcodevariable)):
		if '__undefined' not in extractcodevariable[w]:
			fwrite.write(extractcodevariable[w])
	fwrite.close()
	fwrite1 = open(extractfunction,'a+')
	fwrite1.write('#include "/home/tangyixuan/csmith-2.3.0/runtime/csmith.h"'+'\n')
	for w in range(0, len(extractcodefunction)):
		fwrite1.write(extractcodefunction[w])
	fwrite1.close()
	global variablelist
	astvariable = parse_file(extractvariable, use_cpp=True,cpp_path='gcc',cpp_args=['-E', r'-I/home/tangyixuan/pycparser-master/utils/fake_libc_include'])
	nodevisit = TypeDeclVisitor1()
	nodevisit.visit(astvariable.ext)
	astfunction = parse_file(extractfunction, use_cpp=True,cpp_path='gcc',cpp_args=['-E', r'-I/home/tangyixuan/pycparser-master/utils/fake_libc_include'])
	#variablelist
	for key in variablelist.keys():
		if key.startswith('g_'):
			for t in range(0,len(extractcodevariable)):
				if key in extractcodevariable[t]:
					substring1 = extractcodevariable[t][:extractcodevariable[t].index(key)]
					numberptr = substring1.count('*')
					realptr = ''
					if numberptr != 0:
						for u in range(0,numberptr):
							realptr = realptr + '*'
					variablelist[key] = variablelist[key] + realptr
					substring1 = extractcodevariable[t][extractcodevariable[t].index(key)+len(key):]
					if substring1.startswith('['):
						listwords = substring1.split(' ')
						numberweidu = listwords[0].count('[')
						realptr1 = ''
						if numberweidu != 0:
							for u in range(0,numberweidu):
								realptr1 = realptr1 + '[]'
						variablelist[key] = variablelist[key] + realptr1
						break
					else:
						break
		elif key.startswith('func_'):
			for t in range(0,len(extractcodefunction)):
				if key in extractcodefunction[t]:
					if ',' in extractcodefunction[t]:
						para = extractcodefunction[t].split(',')
						variablelist[key] = str(len(para))
					else:
						variablelist[key] = '0'
					break	
	nodevisit1 = TypeDeclVisitor1()
	nodevisit1.visit(astfunction.ext)
	for key in variablelist:
		if key.startswith('g_'):
			global_variable[key] =  variablelist[key]
		elif key.startswith('func_'):
			global_function[key] =  variablelist[key]
	variablelist = {}

#hang hao:lie hao, lei xing, detail
def read_error_wrong_Information2(rewritepath,regex):
	f = open(rewritepath)
	linef = f.readline()
	mydictall = []
	while linef:
		mydictlist = []
		if regex in linef:
			if '/media/tangyixuan/xuaner' in linef:
				strlist = linef.split(':')
				if strlist[1].isdigit() and strlist[2].isdigit():
					hanglie = strlist[1]+ ":" + strlist[2]
					mydictlist.append(hanglie)
					lastdetail = strlist[len(strlist)-1].strip()
					if lastdetail.rfind(']') == len(lastdetail)-1:
						index = lastdetail.rfind('[')
						leixing = lastdetail[index+1:len(lastdetail)-1]
						mydictlist.append(leixing)
						detail = lastdetail[0:index]
						mydictlist.append(detail)
						mydictall.append(mydictlist)
					else:
						leixing = '-'
						mydictlist.append(leixing)
						mydictlist.append(lastdetail)
						mydictall.append(mydictlist)
				elif strlist[1].isdigit():
					mydictlist.append(strlist[1])
					lastdetail = strlist[len(strlist)-1].strip()
					if lastdetail.rfind(']') == len(lastdetail)-1:
						index = lastdetail.rfind('[')
						leixing = lastdetail[index+1:len(lastdetail)-1]
						mydictlist.append(leixing)
						detail = lastdetail[0:index]
						mydictlist.append(detail)
						mydictall.append(mydictlist)
					else:
						leixing = '-'
						mydictlist.append(leixing)
						mydictlist.append(lastdetail)
						mydictall.append(mydictlist)		
		linef = f.readline()
	f.close()
	return mydictall

def read_error_wrong_Information1(rewritepath,regex):
	f = open(rewritepath)
	line = f.readline()
	mydict = {}
	while line:
		if regex in line:
			strlist = line.split(':')
			if strlist[1].isdigit() and strlist[2].isdigit():
				locationError = strlist[1] + ":" + strlist[2]
				if locationError not in mydict:
					mydict[locationError] = strlist[3]
			elif strlist[1].isdigit():
				location = strlist[1]
				if location not in mydict:
					mydict[location] = strlist[2]			
			
		line = f.readline()
	f.close()
	#print("---------------------")
	#mydictItems = mydict.items()
	#print(list(mydictItems))
	return mydict
def read_coverage(coveragepath):
	listcoverage = []
	with open(coveragepath, 'r') as fcoverage:
    		 listcoverage = fcoverage.readlines()
	return listcoverage


def read_specific(linenum,coverage):
	index1=0
	index2=0
	for h in range(0,len(coverage)):
		if h == linenum:
			index1 = coverage[h].index('{')
			#print('11111111111111111index1:'+coverage[h])
		elif h > linenum:
			if coverage[h].find('}') == index1:
				index2 = h
				#print('22222222222222222index2:'+coverage[h])
				break
	return index2
def read_write_delate_testcase(readpath,writepath):			
	listread = []
	countread = 0
	countwrite = 0
	with open(readpath, 'r') as fread:
    		listread = fread.readlines()
	fwrite = open(writepath,'a+')
	for w in range(1, len(listread)):
		fwrite.write(listread[w])
	fwrite.close()
def read_write_testcase(readpath,writepath):
	listread = []
	countread = 0
	countwrite = 0
	with open(readpath, 'r') as fread:
    		listread = fread.readlines()
	#print("length is : " + str(len(listread)))
	for r in range(0, len(listread)):
		if '__undefined;' in listread[r]:
			#print(listread[r])
			break;
		else:
			countread = countread + 1
	#print("----------------countread---" + str(countread))
	fwrite = open(writepath,'a+')
	fwrite.write('#include "/home/tangyixuan/csmith-2.3.0/runtime/csmith.h"' + "\n")
	#print("length is : " + str(len(listread)))
	for w in range(countread, len(listread)):
		fwrite.write(listread[w])
	fwrite.close()

def compare_errorInformation_and_return_string(dict1,dict2):
	errorinformation = ''
	for key1 in dict1.keys():
		value1 = dict1[key1]
		if key1 not in dict2.keys():
			if ':' in key1:
				newkey1_0 = key1[0:key1.find(':')]
				newkey1_1 = str(int(key1[0:key1.find(':')])-1)
				newkey1_2 = str(int(key1[0:key1.find(':')])+1)
			else:
				newkey1_0 = key1
				newkey1_1 = str(int(key1)-1)
				newkey1_2 = str(int(key1)+1)
			flag = False
			for key2 in dict2.keys():
				if newkey1_0 in key2 or newkey1_1 in key2 or newkey1_2 in key2:
					flag = True
					break
			if flag:
				continue
			else:
				errorinformation = errorinformation + key1 + '-' + str(value1)
	for key2 in dict2.keys():
		value2 = dict2[key2]
		if key2 not in dict1.keys():
			if ':' in key2:
				newkey2_0 = key2[0:key2.find(':')]
				newkey2_1 = str(int(key2[0:key2.find(':')])-1)
				newkey2_2 = str(int(key2[0:key2.find(':')])+1)
			else:
				newkey2_0 = key2
				newkey2_1 = str(int(key2)-1)
				newkey2_2 = str(int(key2)+1)
			flag2 = False
			for key1 in dict1.keys():
				if newkey2_0 in key1 or newkey2_1 in key1 or newkey2_2 in key1:
					flag2 = True
					break
			if flag2:
				continue
			else:
				errorinformation = errorinformation + '*****' + key2 + '-' + str(value2)
	return errorinformation

#calculate the simility
def edit_distance(word1, word2): 
	len1 = len(word1) 
	len2 = len(word2) 
	dp = np.zeros((len1 + 1, len2 + 1)) 
	for i in range(len1 + 1): 
		dp[i][0] = i 
	for j in range(len2 + 1): 
		dp[0][j] = j 
	for i in range(1, len1 + 1): 
		for j in range(1, len2 + 1):  
			if word1[i - 1] == word2[j - 1]:
				temp = 0
			else:
				temp = 1
			dp[i][j] = min(dp[i - 1][j - 1] + temp, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)) 
	return dp[len1][len2] 

def simility(word1, word2):  
	res = edit_distance(word1, word2) 
	print('----------res is--'+str(res))
	maxLen = max(len(word1),len(word2)) 
	return 1-res*1.0/maxLen 


#dict1:hang hao:lie hao , lei xing, detail	
def compare_errorInformation_and_return_string1(dict1,dict2):
	print('----------compare_errorInformation_and_return_string1--dict1 :'+str(len(dict1)))
	print('----------compare_errorInformation_and_return_string1--dict2 :'+str(len(dict2)))
	print('-------------------------------------------------------')
	errorinformation = []
	for i in range(0,len(dict1)):
		flag1 = False
		hangdict1 = dict1[i][0]
		leidict1 = dict1[i][1]
		detaildict1 = dict1[i][2]
		if leidict1 not in warningflag:
			fwtime1 = open(resultpath+warningflagfile,'a+')
			fwtime1.write(leidict1 + '\n')
			fwtime1.close()
			warningflag.add(leidict1)
		#hang,lie,leixing
		hanglieleixing1 = 0
		#hang,lie
		hanglie1 = 0
		#hang,lei xing
		hangleixing1 = 0
		#
		no1 = 0
		#hang
		hangsame1 = 0
		for j in range(0,len(dict2)):
			hangdict2 = dict2[j][0]
			leidict2 = dict2[j][1]
			detaildict2 = dict2[j][2]
			#hang,lie
			if hangdict1 == hangdict2:
				flag1 = True
				#sim = simility(detaildict1,detaildict2)
				if leidict1 != leidict2:
					hanglie1 = hanglie1 + 1
				else:
					hanglieleixing1 = hanglieleixing1 + 1
			elif ':' in hangdict1 and ':' in hangdict2:
				hang1 = hangdict1[0:hangdict1.index(':')]
				hang2 = hangdict2[0:hangdict2.index(':')]
				if hang1 == hang2:
					flag1 = True
					if leidict2 == leidict1:
						hangleixing1 = hangleixing1 + 1
					else:
						hangsame1 = hangsame1 + 1	
		if flag1 == False:
			no1 = no1 + 1
		if hanglieleixing1 == 0:
			if hangleixing1 > 0:
				errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1+'(lie diff)')
			elif hanglie1 > 0:
				errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1+'(type diff)')
			elif hangsame1 > 0:
				errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1+'(lie diff and type diff)')
			elif no1 > 0:
				errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1+'(location diff)')
		if hanglieleixing1 > 1:
			errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1+'(chong fu in the other file)')

	for i in range(0,len(dict2)):
		flag2 = False
		hangdict2 = dict2[i][0]
		leidict2 = dict2[i][1]
		detaildict2 = dict2[i][2]
		#hang,lie,leixing
		hanglieleixing2 = 0
		#hang,lie
		hanglie2 = 0
		#hang,lei xing
		hangleixing2 = 0
		#
		no2 = 0
		#
		hangsame2 = 0
		for j in range(0,len(dict1)):
			hangdict1 = dict1[j][0]
			leidict1 = dict1[j][1]
			detaildict1 = dict1[j][2]
			#hang,lie
			if hangdict2 == hangdict1:
				flag2 = True
				#sim = simility(detaildict1,detaildict2)
				if leidict2 != leidict1:
					hanglie2 = hanglie2 + 1
				else:
					hanglieleixing2 = hanglieleixing2 + 1
			elif ':' in hangdict1 and ':' in hangdict2:
				hang1 = hangdict1[0:hangdict1.index(':')]
				hang2 = hangdict2[0:hangdict2.index(':')]
				if hang1 == hang2:
					flag2 = True
					if leidict2 == leidict1:
						hangleixing2 = hangleixing2 + 1
					else:
						hangsame2 = hangsame2 + 1
		if flag2 == False:
			no2 = no2 + 1
		if hanglieleixing2 == 0:
			if hangleixing2 > 0:
				errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2+'(lie diff)')
			elif hanglie2 > 0:
				errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2+'(type diff)')
			elif hangsame2 > 0:
				errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2+'(lie diff and type diff)')
			elif no2 > 0:
				errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2+'(location diff)')
		if hanglieleixing2 > 1:
			errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2+'(chong fu in the other file)')					
	return errorinformation


#dict1:hang hao:lie hao , lei xing, detail	
def compare_errorInformation_no_leixing(dict1,dict2):
	print('----------in compare_errorInformation_no_leixing--dict1 :'+str(len(dict1)))
	print('----------in compare_errorInformation_no_leixing--dict2 :'+str(len(dict2)))
	errorinformation = []
	if len(dict1) == 0 and len(dict2) == 0:
		return errorinformation
	elif len(dict1) != 0 and len(dict2) == 0:
		for j in range(len(dict1)):
			hangdict1 = dict1[j][0]
			leidict1 = dict1[j][1]
			detaildict1 = dict1[j][2]
			errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1)
	elif len(dict1) == 0 and len(dict2) != 0:
		for j in range(len(dict2)):
			hangdict2 = dict2[j][0]
			leidict2 = dict2[j][1]
			detaildict2 = dict2[j][2]
			errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2)
	else:
		for i in range(0,len(dict1)):
			hangdict1 = dict1[i][0]
			leidict1 = dict1[i][1]
			detaildict1 = dict1[i][2]
			j = 0
			for j in range(0,len(dict2)):
				hangdict2 = dict2[j][0]
				if hangdict2 == hangdict1:
					break
			if hangdict1 != dict2[j][0]:
				errorinformation.append('****'+hangdict1+'****'+detaildict1+'****'+leidict1)


		for i in range(0,len(dict2)):
			hangdict2 = dict2[i][0]
			leidict2 = dict2[i][1]
			detaildict2 = dict2[i][2]
			j = 0
			for j in range(0,len(dict1)):
				hangdict1 = dict1[j][0]
				if hangdict2 == hangdict1:
					break
			if hangdict2 != dict1[j][0]:
				errorinformation.append('####'+hangdict2+'####'+detaildict2+'####'+leidict2)
	return errorinformation


def write_errorInformation(writeErrorInformationPath,compilerinformation,errorInformation):
	fw = open(writeErrorInformationPath,'a+')
	fw.write(compilerinformation + '\n')
	for i in range(len(errorInformation)):
		fw.write(''.join(errorInformation[i]) + '\n')
	fw.close()

def write_outdead(writeErrorInformationPath,outdeadline):
	fw1 = open(writeErrorInformationPath,'a+')
	for i in range(len(outdeadline)):
		fw1.write(''.join(outdeadline[i]))
	fw1.close()

def rankposition(raterule,averagedistance,a):
	sumd = 0
	rr1 = {}
	for key in raterule:
		#print(key + ':' + str(raterule[key]))
		rr1[key]=raterule[key]
		sumd = sumd + raterule[key]
	for key in rr1:
		rr1[key]=averagedistance*(1.0-float(rr1[key] / sumd))
	after = sorted(rr1.items(), key=lambda item:item[1])
	positiona = 0
	for i in range(0,len(after)):
		if after[i][0] in a:
			 positiona = i + 1
	return positiona

def calculatescore(raterule,averagedistance,a):
	sumd = 0
	for key in raterule:
		#print(key + ':' + str(raterule[key]))
		sumd = sumd + raterule[key]
	
	ascore=averagedistance*(1.0-float(raterule[a] / sumd))

	return ascore

def codedistance(path1,path2):
	codewithblank1 = read_coverage(path1)
	codewithblank2 = read_coverage(path2)
	countline = 0
	distance = 0.0
	code1 = []
	code2 = []
	codecompile = re.compile("[^a-z^A-Z^0-9]")
	for subcodewithblank1 in range(0,len(codewithblank1)):
		subcode1 = codecompile.sub('',codewithblank1[subcodewithblank1])
		if len(subcode1) != 0:
			code1.append(subcode1)
	for subcodewithblank2 in range(0,len(codewithblank2)):
		subcode2 = codecompile.sub('',codewithblank2[subcodewithblank2])
		if len(subcode2) != 0:
			code2.append(subcode2)
	if len(code1) >= len(code2):
		for linecode2 in range(0,len(code2)):
			for linecode1 in range(0,len(code1)):
				if code2[linecode2] in code1[linecode1]:
					countline += 1
					break
		distance = 1.0 - float(countline / len(code1))
	else:
		for linecode1 in range(0,len(code1)):
			for linecode2 in range(0,len(code2)):
				if code1[linecode1] in code2[linecode2]:
					countline += 1
					break
		distance = 1.0 - float(countline / len(code2))
	return distance

def codedistance1(path1,path2):
	codewithblank1 = read_coverage(path1)
	codewithblank2 = read_coverage(path2)
	distance = 0.0
	chaji = list(set(codewithblank1) ^ set(codewithblank2))
	bingji =  list(set(codewithblank1).union(set(codewithblank2)))
	distance = float(len(chaji) / len(bingji))
	return distance

def sigmode(x):
	return 1.0 / (1 + np.exp(-float(x)))
def coverage(deletecodecoverage):
	path = pypath+'comparecoverage/'
	nondeletecode = []
	for parent,dirnames,filenames in os.walk(path):
		for filename in filenames:
			nondeletecode = read_coverage(path+filename)
	#print(',,,,,,,,,,,,,,,,,,,,nondeletecode:'+str(nondeletecode))
	flagcoverage = False
	codecompile = re.compile("[^a-z^A-Z^0-9]")
	if len(deletecodecoverage) >0:
		#print('...................deletecodecoverage[0]:'+codecompile.sub('',deletecodecoverage[0]))
		if len(nondeletecode) > 0:
			#print('...........length of nondeletecode:'+str(len(nondeletecode)))
			for a in range(0,len(nondeletecode)):
				if codecompile.sub('',deletecodecoverage[0]) in codecompile.sub('',nondeletecode[a]):
					flagcoverage = True
					break
	return flagcoverage
def del_file(path_data):
	file_data = []
	for filecoverage in os.listdir(path_data):
		file_data.append(path_data + filecoverage)
	if len(file_data) > 0:
		for key in file_data:
			if os.path.exists(key):
				os.remove(key)

def constructCFG(cpath):
	print('-----begin construct CFG-----')
	#print(cpath)
	cmdcfg = 'gcc -c -fdump-tree-cfg-lineno ' + cpath
	s=os.popen(cmdcfg)
	s.close()
	print('-----end construct CFG-----')	
	#print('-----end construct CFG-----')
	#print(s.read())
	#print('-----end construct CFG-----')

def compiledbygcc(cpath,compilationpath):
	warning = "-Wall -Wextra -pedantic -Wabi -Waddress -Waggregate-return -Waggressive-loop-optimizations -Warray-bounds -Wattributes -Wbad-function-cast -Wbuiltin-macro-redefined -Wcast-align -Wcast-qual -Wchar-subscripts -Wclobbered -Wcomment -Wcomments -Wconversion -Wcoverage-mismatch -Wcpp -Wdeclaration-after-statement -Wdeprecated -Wdeprecated-declarations -Wdisabled-optimization -Wdiv-by-zero -Wdouble-promotion -Wempty-body -Wendif-labels -Wenum-compare -Werror-implicit-function-declaration -Wfloat-equal -Wformat -Wformat-contains-nul -Wformat-extra-args -Wformat-nonliteral -Wformat-security -Wformat-y2k -Wformat-zero-length -Wfree-nonheap-object -Wignored-qualifiers -Wimplicit -Wimplicit-function-declaration -Wimplicit-int -Winit-self -Winline -Wint-to-pointer-cast -Winvalid-memory-model -Winvalid-pch -Wjump-misses-init -Wlogical-op -Wlong-long -Wmain -Wmaybe-uninitialized -Wmissing-braces -Wmissing-declarations -Wmissing-field-initializers -Wmissing-include-dirs -Wmissing-parameter-type -Wmissing-prototypes -Wmudflap -Wmultichar -Wnarrowing -Wnested-externs -Wnonnull -Wnormalized=id -Wnormalized=nfc -Wnormalized=nfkc -Wold-style-declaration -Wold-style-definition -Woverflow -Woverlength-strings -Woverride-init -Wpacked -Wpacked-bitfield-compat -Wpadded -Wparentheses -Wpedantic -Wpointer-arith -Wpointer-sign -Wpointer-to-int-cast -Wpragmas -Wredundant-decls -Wreturn-local-addr -Wreturn-type -Wsequence-point -Wshadow -Wsign-compare -Wsizeof-pointer-memaccess -Wstack-protector -Wstrict-aliasing -Wstrict-overflow -Wstrict-prototypes -Wsuggest-attribute=const -Wsuggest-attribute=format -Wsuggest-attribute=noreturn -Wsuggest-attribute=pure -Wswitch -Wswitch-default -Wswitch-enum -Wsync-nand -Wsystem-headers -Wtraditional -Wtraditional-conversion -Wtrampolines -Wtrigraphs -Wtype-limits -Wundef -Wuninitialized -Wunknown-pragmas -Wunsafe-loop-optimizations -Wunsuffixed-float-constants -Wunused -Wunused-but-set-parameter -Wunused-but-set-variable -Wunused-function -Wunused-label -Wunused-local-typedefs -Wunused-macros -Wunused-parameter -Wunused-result -Wunused-value -Wunused-variable -Wvarargs -Wvariadic-macros -Wvector-operation-performance -Wvla -Wvolatile-register-var -Wwrite-strings "
	cmd2 = 'timeout 30 /usr/bin/gcc-4.8 -c '+ warning + cpath
	run_cmd_save_errorInformation(cmd2,compilationpath)

def compiledbyclang(cpath,compilationpath):
	cmd1 = 'timeout 30 /home/tangyixuan/LLVM/llvm-8.0-pre/bin/clang-8 -c -Weverything -pedantic -ferror-limit=0 '+ cpath
	run_cmd_save_errorInformation(cmd1,compilationpath)

def kuohao(s):
	location = 0
	a = []
	mark = []
	inlineword = ''
	for i in range(len(s)):
		if s[i] != ")":
			a.append(s[i])
			if s[i] == "(":
				mark.append(s[i])
		else:
			if mark and len(mark)!= 1:
				for j in range(len(a)-1, -1, -1):
					if a[j] != '(':
						a.pop()
					else:
						a.pop()
						mark.pop()
						break
			else:					
				return ''.join(a)

def replacename(codetype):
	global variablelist
	print("-----ready to insert ")
	#insert the function
	filenamelist0 = os.listdir(codesnippetpath+codetype+'/')
	filenamelist = []
	for f in range(0,len(filenamelist0)):
		if filenamelist0[f].endswith('.c'):
			filenamelist.append(filenamelist0[f])
	#print(codesnippetpath+codetype+'/')
	#print('filenamelist' + str(len(filenamelist)))
	sample = random.sample(filenamelist,1)		
	#print(str(sample))
	#print(str(sample[0]))
	samplepath = codesnippetpath+'/'+codetype+'/'+sample[0]
	#samplepath = codesnippetpath+'/Function/11.c'
	print("----------insert "+codetype+" : "+sample[0])
	samplecode = read_coverage(samplepath)
	#for i in range(0,len(samplecode)):
	#	print(samplecode[i])
	#insert::rename the function name
	whetherreplace = samplecode[0][2:].strip()
	renamemaping = {}
	if whetherreplace != '':
		namelist = whetherreplace.split(' ')
		#print(str(namelist))
		#sys.exit(0)
		#print('-----------------'+str(namelist))
		suitablename = []
		#print('=============global_function====='+str(global_function))
		if len(namelist) != 0:
			for h in range(0,len(namelist)):
				if namelist[h] != '':
					nameandtype = namelist[h].split(':')
					#print('///////////////////'+str(nameandtype[0])+'///////////////////'+str(nameandtype[1]))
					if nameandtype[1] == 'int':
						samplecode.insert(1,'int '+nameandtype[0]+';')
					if nameandtype[0].startswith('i') or nameandtype[0].startswith('j'):
						continue
					elif nameandtype[0].startswith('func_'):
						'''
						for i in range(1,len(samplecode)):
							if nameandtype[0] in samplecode[i]:
								substring = samplecode[i][samplecode[i].index(nameandtype[0])+len(nameandtype[0]):]
								extract = kuohao(substring)
   								nameandtype[1] = str(extract.count(','))
								print('/////////////////////'+nameandtype[1])
								break
						'''
						for funckey in global_function:
							#print('=============global_function====='+funckey+'======'+str(global_function[funckey]))
							if nameandtype[1] == str(global_function[funckey]):
								#print('ppppppppppppppppppppp'+funckey)
								suitablename.append(funckey)
						if len(suitablename) != 0:
							if len(suitablename) == 1:
								renamemaping[nameandtype[0]]=suitablename[0]
							else:
								selectname = random.randint(0,len(suitablename)-1)
								renamemaping[nameandtype[0]]=suitablename[selectname]
							suitablename = []
					else:
						#print(str(variablelist))
						#local variable first
						for variable in variablelist:
							if nameandtype[1] == variablelist[variable]:
								#print('ppppppppppppppppppppp'+funckey)
								suitablename.append(variable)
						if len(suitablename) != 0:
							if len(suitablename) == 1:
								renamemaping[nameandtype[0]]=suitablename[0]
							else:
								selectname = random.randint(0,len(suitablename)-1)
								if '[' in nameandtype[0]:
									renamemaping[nameandtype[0]]=suitablename[selectname]+nameandtype[0][nameandtype[0].index('['):]
								else:
									renamemaping[nameandtype[0]]=suitablename[selectname]
							suitablename = []
						#global variable later
						else:
							for variable in global_variable:
								if nameandtype[1] == global_variable[variable]:
									#print('ppppppppppppppppppppp'+funckey)
									suitablename.append(variable)
							if len(suitablename) != 0:
								if len(suitablename) == 1:
									renamemaping[nameandtype[0]]=suitablename[0]
								else:
									selectname = random.randint(0,len(suitablename)-1)
									if '[' in nameandtype[0]:
										renamemaping[nameandtype[0]]=suitablename[selectname]+nameandtype[0][nameandtype[0].index('['):]
									else:
										renamemaping[nameandtype[0]]=suitablename[selectname]
								suitablename = []
							else:
								print('!!!!!!!!!!!!!!!!!!retry again!!!!!!!!!!!!!!!!!!!!!!')
								return []
	if len(renamemaping) != 0:
		#print('ooooooooooooo'+str(renamemaping))
		#replace name
		for r in range(1,len(samplecode)):
			for key in renamemaping:
				if key in samplecode[r]:
					samplecode[r] = samplecode[r].replace(key,renamemaping[key])
	#print('-------------rename------------') 
	#for i in range(0,len(samplecode)):
	#	print(samplecode[i])
	variablelist = {}
	return samplecode
def alwaysfalse(resultpath,testcase,qq,originalcodefile,globallinenum,astnew1):
	global allcompilablecout
	global uncompilablecount
	global inlinefunction
	while(True):
		rewritepath5 = resultpath+'newvariantgcc1/'+testcase+"-"+str(qq)+".c"
		f = open(rewritepath5,'w+')
		print("alwaysfalse, inline of function is ready to insert : ")
		#insert inline the function
		astnew = copy.deepcopy(astnew1)
		nodevisitfunc = FuncDefVisitor1_1()
		nodevisitfunc.visit(astnew.ext)
		if len(inlinefunction) == 0:
			continue
		#print('/////////////////renamecode//////////')
		#for r in range(0,len(inlinefunction)):
		#	print(inlinefunction[r])
		#print('/////////////////end renamecode//////////')
		num1 = 0
		num2 = 0
		for g in range(0,len(originalcodefile)):
			if inlinefunction[0] in originalcodefile[g] and (originalcodefile[g].strip().endswith(';') is False):
				num1 = g
				f.write('\n')
				for v in range(0,len(inlinefunction)):
					f.write(inlinefunction[v]+'\n')
				f.write('\n')
				break
			else:
				f.write(originalcodefile[g])
		#print('num1 is : '+str(num1))
		for l in range(num1+2,len(originalcodefile)):
			#print('---------'+str(l))
			if originalcodefile[l].startswith('static') and 'func_' in originalcodefile[l] and (originalcodefile[l].strip().endswith(';') is False):
				#print(originalcodefile[l])
				#print(str(l))
				num2 = l
				break
			elif originalcodefile[l].startswith('int main'):
				num2 = l
				break
		#print('num2 is: '+str(num2))
		for t in range(num2,len(originalcodefile)):
			f.write(originalcodefile[t])
		f.close()
		inlinefunction = []
		del astnew

		#determine whether compilable
		tempcompilationgcc11 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.gcc.txt"
		tempcompilationclang11 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.clang.txt"
		compiledbygcc(rewritepath5,tempcompilationgcc11)

		if os.path.exists('./'+testcase+"-"+str(qq)+'.o'):
			#print(',,,,,,,,,,')
			os.remove('./'+testcase+"-"+str(qq)+'.o')
		compiledbyclang(rewritepath5,tempcompilationclang11)
		if os.path.exists('./'+testcase+"-"+str(qq)+'.o'):
			#print(',,,,,,,,,,')
			os.remove('./'+testcase+"-"+str(qq)+'.o')
		listdictgcc = read_error_wrong_Information2(tempcompilationgcc11,'error:')
		listdictclang = read_error_wrong_Information2(tempcompilationclang11,'error:')
		#sys.exit(0)
		if len(listdictgcc)!=0 and len(listdictclang)!=0:
			print('........uncompilable...........')
			#sys.exit(0)
			uncompilablecount += 1
			os.remove(tempcompilationgcc11)
			os.remove(tempcompilationclang11)
			os.remove(rewritepath5)
			continue
		else:
			allcompilablecout += 1
			break

def alwaystrue(resultpath,testcase,qq,originalcodefile,globallinenum,astnew1):
	global allcompilablecout
	global uncompilablecount
	global inlinefunction
	while(True):
		rewritepath5 = resultpath+'newvariantgcc1/'+testcase+"-"+str(qq)+".c"
		f = open(rewritepath5,'w+')
		print("awaystrue, inline of function is ready to insert : ")
		#insert inline the function
		astnew = copy.deepcopy(astnew1)
		nodevisitfunc = FuncDefVisitor2_1()
		nodevisitfunc.visit(astnew.ext)
		if len(inlinefunction) == 0:
			continue
		#print('/////////////////renamecode//////////')
		#for r in range(0,len(inlinefunction)):
		#	print(inlinefunction[r])
		#print('/////////////////end renamecode//////////')
		num1 = 0
		num2 = 0
		for g in range(0,len(originalcodefile)):
			if inlinefunction[0] in originalcodefile[g] and (originalcodefile[g].strip().endswith(';') is False):
				num1 = g
				f.write('\n')
				for v in range(0,len(inlinefunction)):
					f.write(inlinefunction[v]+'\n')
				f.write('\n')
				break
			else:
				f.write(originalcodefile[g])
		#print('num1 is : '+str(num1))
		for l in range(num1+2,len(originalcodefile)):
			#print('---------'+str(l))
			if originalcodefile[l].startswith('static') and 'func_' in originalcodefile[l] and (originalcodefile[l].strip().endswith(';') is False):
				#print(originalcodefile[l])
				#print(str(l))
				num2 = l
				break
			elif originalcodefile[l].startswith('int main'):
				num2 = l
				break
		#print('num2 is: '+str(num2))
		for t in range(num2,len(originalcodefile)):
			f.write(originalcodefile[t])
		f.close()
		inlinefunction = []
		del astnew

		#determine whether compilable
		tempcompilationgcc11 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.gcc.txt"
		tempcompilationclang11 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.clang.txt"
		compiledbygcc(rewritepath5,tempcompilationgcc11)

		if os.path.exists('./'+testcase+"-"+str(qq)+'.o'):
			#print(',,,,,,,,,,')
			os.remove('./'+testcase+"-"+str(qq)+'.o')
		compiledbyclang(rewritepath5,tempcompilationclang11)
		if os.path.exists('./'+testcase+"-"+str(qq)+'.o'):
			#print(',,,,,,,,,,')
			os.remove('./'+testcase+"-"+str(qq)+'.o')
		listdictgcc = read_error_wrong_Information2(tempcompilationgcc11,'error:')
		listdictclang = read_error_wrong_Information2(tempcompilationclang11,'error:')
		#sys.exit(0)
		if len(listdictgcc)!=0 and len(listdictclang)!=0:
			print('........uncompilable...........')
			#sys.exit(0)
			uncompilablecount += 1
			os.remove(tempcompilationgcc11)
			os.remove(tempcompilationclang11)
			os.remove(rewritepath5)
			continue
		else:
			allcompilablecout += 1
			break

if __name__ == "__main__":
	start = datetime.datetime.now()
	count0 = 0
	#the number of test case generation
	#seedpath = '/media/tangyixuan/xuaner/csmith-seed/weekseedccs.txt'
	#seedpath = '/home/tang-ubuntu-1604/warning-testing-code/csmith-seed/csmith-original/ccs-seed/seed2.txt'
	#seedpath = '/home/tang-ubuntu-1604/warning-testing-code/csmith-seed/csmith-original/ccs-seed/seed3.txt'
	#seedpath = '/home/tang-ubuntu-1604/warning-testing-code/csmith-seed/csmith-original/ccs-seed/seed4.txt'
	seedpath = '/media/tangyixuan/xuaner/csmith-seed/newconfigure/configure-1.txt'
	fseed = open(seedpath)
	lineseed = fseed.readlines()
	fseed.close()
	for i in range(0,len(lineseed)):
		graphlist = []
		global_variable = {}
		global_function = {}
		del_file(pypath+'comparecoverage/')
		del_file(resultpath+'tempcompilationgccclang/')
		delatefilepathlist = set()
		count0 = count0 + 1
		print("**********the test case number is : %d **********" %count0)
		if count0 < 15054:
			continue
		seed = lineseed[i].strip()
		#seed = 4237969256
		print("**********seed is: "+str(seed))
		#generate test cases by csmith
		cmdcasegenerate = 'csmith -s '+ seed+ ' > ' + pypath + 'testcases/test'+str(count0)+'.c'
		os.system(cmdcasegenerate)
		#insert include, delete original test case
		read_write_testcase(pypath+'testcases/test'+str(count0)+'.c',pypath+'testcases1/test'+str(count0)+'.c')
		#use AST to move zhushi
		ast = parse_file(pypath+'testcases1/test'+str(count0)+'.c', use_cpp=True,cpp_path='gcc',cpp_args=['-E', r'-I/home/tangyixuan/pycparser-master/utils/fake_libc_include'])
		rewritepath0 = pypath+'testcases2/test'+str(count0)+'.c'
		generator1 = c_generator.CGenerator()
		#print(str(generator1.visit(ast)))
		f11 = open(rewritepath0,'w+')
		f11.write(str(generator1.visit(ast)))
		f11.close()
		del ast
		rewritepath1 = pypath+'test'+str(count0)+'.c'
		read_write_testcase(rewritepath0,rewritepath1)
		testcase = 'test'+str(count0)+'.c'
		#compile the deleted testcase
		coverageconfirm = timeout('timeout 5 ./test.sh test'+str(count0))
		if bool(1-os.path.exists(pypath+'test'+str(count0)+'.c.gcov')):
			if os.path.exists(pypath+'test'+str(count0)+'.c'):
				os.remove(pypath+'test'+str(count0)+'.c')                   
			if os.path.exists(pypath+'test'+str(count0)):
				os.remove(pypath+'test'+str(count0))
			if os.path.exists(pypath+'test'+str(count0)+'.gcno'):
				os.remove(pypath+'test'+str(count0)+'.gcno')
			if os.path.exists(pypath+'testcases/test'+str(count0)+'.c'):
				os.remove(pypath+'testcases/test'+str(count0)+'.c')
			if os.path.exists(pypath+'testcases1/test'+str(count0)+'.c'):
				os.remove(pypath+'testcases1/test'+str(count0)+'.c')
			if os.path.exists(pypath+'testcases2/test'+str(count0)+'.c'):
				os.remove(pypath+'testcases2/test'+str(count0)+'.c')
			continue


		#read coverage
		filecoverage = read_coverage(pypath+'test'+str(count0)+'.c.gcov')

		#delete dead code
		afterdelete = []
		lenfi = len(filecoverage)
		a = 0
		hang = 0
		for a in range(0,len(filecoverage)):
			if hang != len(filecoverage)-1:
				if a > hang:
					#print('+++---a is ----------------'+str(a))
					if filecoverage[a] != '':
						line = filecoverage[a].split(':')
						if int(line[1].strip()) > 0:
							if a != len(filecoverage)-1:
								linenext = filecoverage[a+1].split(':')
								# delete dead code
								if line[0].strip() == '#####' and linenext[2].strip() == '{':
									#find the location of '}'
									#print('###'+filecoverage[a]+filecoverage[a+1])
									hang = read_specific(a+1,filecoverage)
									#print('-------hang is ----------------'+str(hang))
								elif line[0].strip() == '#####' and linenext[2].strip() != '{' and 'goto' not in line[2].strip():
									a = a + 1
								elif line[0].strip() == '-' and 'else' in line[2].strip() and linenext[2].strip() == '{':
									hang = read_specific(a+1,filecoverage)
								elif line[2].strip().startswith('lbl_'):
									a = a + 1
								else:
									prex = len(line[0])+len(line[1])+2
									afterdelete.append(filecoverage[a][prex:])
							else:
								prex = len(line[0])+len(line[1])+2
								afterdelete.append(filecoverage[a][prex:])
			else:
				break
			
		rewritepath2 = pypath+'outdead/test'+str(count0)+'.c'
		write_outdead(rewritepath2,afterdelete)

		#rewrite: delete function declaration/ insert ; after 'if'(no { in the next line of if)
		dic1={}
		for k in range(0,len(afterdelete)):
			if afterdelete[k].startswith('static') and 'func_' in afterdelete[k]:
				function = afterdelete[k][0:afterdelete[k].find('(')]
				if dic1 and function in dic1.keys():
					value1 = dic1[function]+1 
					dic1[function] = value1
				else:
					dic1[function] = 1
		afterdelete1 = []
		for gg in range(0,len(afterdelete)):
			afterdelete1.append(afterdelete[gg])
		if dic1:
			#print('---------------len(dic1):'+str(len(dic1)))
			#print('---------------afterdelete:'+str(len(afterdelete)))
			for key	in dic1:
				if dic1[key] == 1:
					#print('-----key:'+key)
					for ll in range(0,len(afterdelete)):
						if key in afterdelete[ll]:
							for hh in range(0,len(afterdelete1)):
								deletes = key+'('
								if deletes in afterdelete1[hh]:
									del afterdelete1[hh]
									break
		#print('---------------afterdelete1:'+str(len(afterdelete1)))
		for p in range(0,len(afterdelete1)):
			if 'if' in afterdelete1[p] and '{' not in afterdelete1[p+1]:
				listifelse = []
				for q in range(p+1,len(afterdelete1)):
					if len(afterdelete1[q].strip()) != 0:
						if 'else' in afterdelete1[q].strip():
							break
						else:
							listifelse.append(afterdelete1[q])
				if len(listifelse) != 1:
					afterdelete1[p] = afterdelete1[p].replace('\n',';\n')
		afterdelete2=[]
		for ss in range(0,len(afterdelete1)):
			afterdelete2.append(afterdelete1[ss])
	
		rewritepath3 = pypath+'outdead1/test'+str(count0)+'.c'
		write_outdead(rewritepath3,afterdelete2)
		#delete coverage file
		if os.path.exists(rewritepath1):
			os.remove(rewritepath1)
		if os.path.exists(pypath+'test'+str(count0)+'.c.gcov'):
			os.remove(pypath+'test'+str(count0)+'.c.gcov')
		#delete original test case
		if os.path.exists(pypath+'testcases/test'+str(count0)+'.c'):
			os.remove(pypath+'testcases/test'+str(count0)+'.c')
		if os.path.exists(pypath+'testcases1/test'+str(count0)+'.c'):
			os.remove(pypath+'testcases1/test'+str(count0)+'.c')
		if os.path.exists(pypath+'testcases2/test'+str(count0)+'.c'):
			os.remove(pypath+'testcases2/test'+str(count0)+'.c')
		if os.path.exists(pypath+'outdead/test'+str(count0)+'.c'):
			os.remove(pypath+'outdead/test'+str(count0)+'.c')
		#compiled file
		rewritepath4 = resultpath+'newvariantgcc1/'+testcase+"-"+str(0)+".c"
		rewritepath44 = pypath+'comparecoverage/'
		delatefilepathlist.add(rewritepath44+'test'+str(count0)+'.c')
		shutil.copy(pypath+'outdead1/test'+str(count0)+'.c',rewritepath44)
		shutil.move(pypath+'outdead1/test'+str(count0)+'.c',rewritepath4)
		
		#compile original file
		tempcompilationgcc = resultpath+'tempcompilationgccclang/test'+str(count0)+'.c'+'gcc.txt'
		tempcompilationclang = resultpath+'tempcompilationgccclang/test'+str(count0)+'.c'+'clang.txt'
		compiledbygcc(rewritepath4,tempcompilationgcc)
		if os.path.exists('./test'+str(count0)+'.c-0.o'):
			#print('.............')
			os.remove('./test'+str(count0)+'.c-0.o')
		compiledbyclang(rewritepath4,tempcompilationclang)
		if os.path.exists('./test'+str(count0)+'.c-0.o'):
			#print('.............')
			os.remove('./test'+str(count0)+'.c-0.o')
		listdictgcc = read_error_wrong_Information2(tempcompilationgcc,'error:')
		listdictclang = read_error_wrong_Information2(tempcompilationclang,'error:')
		if len(listdictgcc)!=0 and len(listdictclang)!=0:
			print("----error, continue the next-------")
			os.remove(tempcompilationgcc)
			os.remove(tempcompilationclang)
			os.remove(rewritepath4)
			continue
		print("--no error--")

		#allcompilablecout += 1	
		delatefilepathlist.add(rewritepath4)
		seedtestcount += 1
		#compare warning message
		listdict1gcc = read_error_wrong_Information2(tempcompilationgcc,'warning:')
		listdict2clang = read_error_wrong_Information2(tempcompilationclang,'warning:')
		os.remove(tempcompilationgcc)
		os.remove(tempcompilationclang)
		ErrorInformationcompare = compare_errorInformation_and_return_string1(listdict1gcc,listdict2clang)
		if len(ErrorInformationcompare)==0:
			print("yes, no consistence")
		else:
			print("----find warning consistence-------")

			writeErrorinforPathcompare = resultpath + warningfile
			mediumtimecompare = datetime.datetime.now()
			timecompare = mediumtimecompare - start
			fwtimecompare = open(writeErrorinforPathcompare,'a+')
			fwtimecompare.write(str(timecompare) + '\n')
			fwtimecompare.close()

			locationErrorBetweenCompilers0 = testcase+"-"+str(0)+".c" + " compiled by gcc4.8 and clang8 : "
			write_errorInformation(writeErrorinforPathcompare,locationErrorBetweenCompilers0,ErrorInformationcompare)

		astnew1 = parse_file(rewritepath4, use_cpp=True,cpp_path='gcc',cpp_args=['-E', r'-I/home/tangyixuan/pycparser-master/utils/fake_libc_include'])

		#extract the globle code
		extractfilepath = resultpath+'newvariantgcc1/'+testcase+"-global-variable.c"
		extractfilepath1 = resultpath+'newvariantgcc1/'+testcase+"-global-function-declaration.c"
		#global variable: global_variable{name,type} global-function:global_function{name, num of para}
		extract_globle_code(rewritepath4,extractfilepath,extractfilepath1)
		delatefilepathlist.add(extractfilepath)
		delatefilepathlist.add(extractfilepath1)
		flawhile0 = False
		variantscore = []
		originalcodefile = read_coverage(rewritepath4)
		#global line
		globallinenum = 0
		for k in range(0,len(originalcodefile)):
			if 'func_' in originalcodefile[k] and '{' in originalcodefile[k+1]:
				globallinenum = k-1
				break

		if os.path.exists('./test'+str(count0)+'.c-0.o'):
			#print('.............')
			os.remove('./test'+str(count0)+'.c-0.o')

		for qq in range(1,9):
			print("number is %d-----this is the : %d-----" %(count0,qq))
			#distance = []
			# 0: delete  1: insert
			#insertordelete = 1
			insertordelete = random.randint(0,1)
			if insertordelete == 0:
				alwaysfalse(resultpath,testcase,qq,originalcodefile,globallinenum,astnew1)
			else:
				alwaystrue(resultpath,testcase,qq,originalcodefile,globallinenum,astnew1)

			rewritepath5 = resultpath+'newvariantgcc1/'+testcase+"-"+str(qq)+".c"
			tempcompilationgcc1 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.gcc.txt"
			tempcompilationclang1 = resultpath+'tempcompilationgccclang/'+testcase+"-"+str(qq)+".c.clang.txt"
			listdict1 = read_error_wrong_Information2(tempcompilationgcc1,'warning:')
			listdict2 = read_error_wrong_Information2(tempcompilationclang1,'warning:')
			delatefilepathlist.add(tempcompilationgcc1)
			delatefilepathlist.add(tempcompilationclang1)
			#print('len of warning in clang8 is :'+str(len(listdict1)))
			#print('len of warning in gcc4.8 is :'+str(len(listdict2)))
			
			ErrorInformation1 = compare_errorInformation_and_return_string1(listdict1,listdict2)
			

			if len(ErrorInformation1)==0:
				print("yes, no consistence")
				#delete the the error information
				delatefilepathlist.add(rewritepath5)
			else:
				print("----find warning consistence-------")
				writeErrorinforPath = resultpath+warningfile
				mediumtime = datetime.datetime.now()
				time = mediumtime - start
				fwtime = open(writeErrorinforPath,'a+')
				fwtime.write(str(time) + '\n')
				fwtime.close()
				locationErrorBetweenCompilers1 = testcase+"-"+str(qq)+".c" + " compiled by gcc4.8 and clang8 : "
				write_errorInformation(writeErrorinforPath,locationErrorBetweenCompilers1,ErrorInformation1)
				delatefilepathlist.add(rewritepath5)
			del ErrorInformation1
			if os.path.exists('./'+testcase+"-"+str(qq)+'.o'):
				print(',,,,,,,,,,')
				os.remove('./'+testcase+"-"+str(qq)+'.o')
			#sys.exit(0)
		#sys.exit(0)
		del astnew1

		gc.collect()
		if len(delatefilepathlist) > 0:
			for key in delatefilepathlist:
				if os.path.exists(key):
					os.remove(key)
		delatefilepathlist.clear()
		del_file(resultpath+'newvariantgcc1/') 
		
		mediumtime = datetime.datetime.now()
		consumtime = mediumtime - start + datetime.timedelta(days=4,hours=18,minutes=21,seconds=41)
		#consumtime = mediumtime - start
		if consumtime.__ge__(datetime.timedelta(days=5,hours=0,minutes=0,seconds=0)):
			fwtimecount = open(resultpath+timefile,'a+')
			fwtimecount.write(str(consumtime) + '\t' + testcase + '\n')
			fwtimecount.write('seed test case : '+ str(seedtestcount)+'\n')
			fwtimecount.write('generate test case : '+ str(allcompilablecout)+'\n')
			fwtimecount.write('uncompilable test case : '+ str(uncompilablecount)+'\n')
			fwtimecount.close()
			exit(0)
		if count0 % 10 == 0:
			fwtime = open(resultpath+timefile,'a+')
			fwtime.write(str(consumtime) + '\t' + ' seed : ' + str(seed) + '\n')
			fwtime.write('number of seed test case : '+ str(seedtestcount)+'\n')
			fwtime.close()							
	end = datetime.datetime.now()	
	print(str(end-start))

				

