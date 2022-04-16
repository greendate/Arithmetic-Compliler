import unittest
from tokens import Token, TokenType
from parser_ import Parser
from nodes import *

class TestParser(unittest.TestCase):

	def test_empty(self):
		tokens = []
		node = Parser(tokens).parse()
		self.assertEqual(node, None)

	def test_numbers(self):
		tokens = [Token(TokenType.NUMBER, 51.2)]
		node = Parser(tokens).parse()
		self.assertEqual(node, NumberNode(51.2))

	def test_single_operations(self):
		tokens = [
			Token(TokenType.NUMBER, 27),
			Token(TokenType.PLUS),
			Token(TokenType.NUMBER, 14),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, AddNode(NumberNode(27), NumberNode(14)))

		tokens = [
			Token(TokenType.NUMBER, 27),
			Token(TokenType.MINUS),
			Token(TokenType.NUMBER, 14),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, SubtractNode(NumberNode(27), NumberNode(14)))

		tokens = [
			Token(TokenType.NUMBER, 27),
			Token(TokenType.MULTIPLY),
			Token(TokenType.NUMBER, 14),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, MultiplyNode(NumberNode(27), NumberNode(14)))

		tokens = [
			Token(TokenType.NUMBER, 27),
			Token(TokenType.DIVIDE),
			Token(TokenType.NUMBER, 14),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, DivideNode(NumberNode(27), NumberNode(14)))

	def test_full_expression(self):
		tokens = [
			Token(TokenType.NUMBER, 27),
			Token(TokenType.PLUS),
			Token(TokenType.LPAREN),
			Token(TokenType.NUMBER, 43),
			Token(TokenType.DIVIDE),
			Token(TokenType.NUMBER, 36),
			Token(TokenType.MINUS),
			Token(TokenType.NUMBER, 48),
			Token(TokenType.RPAREN),
			Token(TokenType.MULTIPLY),
			Token(TokenType.NUMBER, 51),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, AddNode(
			NumberNode(27),
			MultiplyNode(
				SubtractNode(
					DivideNode(
						NumberNode(43),
						NumberNode(36)
					),
					NumberNode(48)
				),
				NumberNode(51)
			)
		))


	def test_simple_comparison(self):
		tokens = [
 			Token(TokenType.NUMBER, 12),
 			Token(TokenType.LESS),
 			Token(TokenType.NUMBER, 15),
 		]

		node = Parser(tokens).parse()
		self.assertEqual(node, LessNode(NumberNode(12), NumberNode(15)))

		tokens = [
		   Token(TokenType.NUMBER, 17),
		   Token(TokenType.LESSEQ),
		   Token(TokenType.NUMBER, 21),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, LessEqNode(NumberNode(17), NumberNode(21)))

		tokens = [
		  Token(TokenType.NUMBER, 6),
		  Token(TokenType.EQUAL),
		  Token(TokenType.NUMBER, 6),
		 ]

		node = Parser(tokens).parse()
		self.assertEqual(node, EqualNode(NumberNode(6), NumberNode(6)))

		tokens = [
			 Token(TokenType.NUMBER, 77),
			 Token(TokenType.GREATER),
			 Token(TokenType.NUMBER, 26),
	 	]

		node = Parser(tokens).parse()
		self.assertEqual(node, GreaterNode(NumberNode(77), NumberNode(26)))

		tokens = [
			Token(TokenType.NUMBER, 154),
			Token(TokenType.GREATEREQ),
			Token(TokenType.NUMBER, 102),
		]

		node = Parser(tokens).parse()
		self.assertEqual(node, GreaterEqNode(NumberNode(154), NumberNode(102)))

	def test_term_comparison(self):
		tokens = [
			Token(TokenType.NUMBER, 5),
			Token(TokenType.MULTIPLY),
			Token(TokenType.NUMBER, 8),
			Token(TokenType.LESS),
			Token(TokenType.NUMBER, 12),
			Token(TokenType.DIVIDE),
			Token(TokenType.NUMBER, 5),
		]
		node = Parser(tokens).parse()
		self.assertEqual(node, LessNode(MultiplyNode(NumberNode(5), NumberNode(8)), DivideNode(NumberNode(12), NumberNode(5))))

	def test_expression_comparison(self):
		tokens = [
			Token(TokenType.NUMBER, 4),
			Token(TokenType.PLUS),
			Token(TokenType.LPAREN),
			Token(TokenType.NUMBER, 14),
			Token(TokenType.MULTIPLY),
			Token(TokenType.NUMBER, 7),
			Token(TokenType.RPAREN),
			Token(TokenType.GREATEREQ),
			Token(TokenType.LPAREN),
			Token(TokenType.NUMBER, 21),
			Token(TokenType.DIVIDE),
			Token(TokenType.NUMBER, 3),
			Token(TokenType.RPAREN),
			Token(TokenType.MINUS),
			Token(TokenType.NUMBER, 11),
		]
		node = Parser(tokens).parse()
		self.assertEqual(node, GreaterEqNode(AddNode(NumberNode(4), MultiplyNode(NumberNode(14), NumberNode(7))), SubtractNode(DivideNode(NumberNode(21), NumberNode(3)), NumberNode(11))))
