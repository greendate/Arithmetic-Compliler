import unittest
from tokens import Token, TokenType
from lexer import Lexer

class TestLexer(unittest.TestCase):

	def test_empty(self):
		tokens = list(Lexer("").generate_tokens())
		self.assertEqual(tokens, [])

	def test_whitespace(self):
		tokens = list(Lexer(" \t\n  \t\t\n\n").generate_tokens())
		self.assertEqual(tokens, [])

	def test_numbers(self):
		tokens = list(Lexer("123 123.456 123. .456 .").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.NUMBER, 123.000),
			Token(TokenType.NUMBER, 123.456),
			Token(TokenType.NUMBER, 123.000),
			Token(TokenType.NUMBER, 000.456),
			Token(TokenType.NUMBER, 000.000),
		])

	def test_operators(self):
		tokens = list(Lexer("+-*/").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.PLUS),
			Token(TokenType.MINUS),
			Token(TokenType.MULTIPLY),
			Token(TokenType.DIVIDE),
		])

	def test_parens(self):
		tokens = list(Lexer("()").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.LPAREN),
			Token(TokenType.RPAREN),
		])

	def test_all(self):
		tokens = list(Lexer("27 + (43 / 36 - 48) * 51").generate_tokens())
		self.assertEqual(tokens, [
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
		])

	def test_comparison_operators(self):
		tokens = list(Lexer("< <= == > >=").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.LESS),
			Token(TokenType.LESSEQ),
			Token(TokenType.EQUAL),
			Token(TokenType.GREATER),
			Token(TokenType.GREATEREQ),
		])

	def test_simple_comparison(self):
		tokens = list(Lexer("5==2").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.NUMBER, 5),
			Token(TokenType.EQUAL),
			Token(TokenType.NUMBER, 2),
		])

	def test_term_comparison(self):
		tokens = list(Lexer("5*8<12/5").generate_tokens())
		self.assertEqual(tokens, [
			Token(TokenType.NUMBER, 5),
			Token(TokenType.MULTIPLY),
			Token(TokenType.NUMBER, 8),
			Token(TokenType.LESS),
			Token(TokenType.NUMBER, 12),
			Token(TokenType.DIVIDE),
			Token(TokenType.NUMBER, 5),
		])

	def test_expression_comparison(self):
		tokens = list(Lexer("4 + (14 * 7) >= (21 / 3) - 11").generate_tokens())
		self.assertEqual(tokens, [
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
		])
