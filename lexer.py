from tokens import Token, TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'
OPERATORS = '<=>'

class Lexer:
	def __init__(self, text):
		self.text = iter(text)
		self.advance()

	def advance(self):
		try:
			self.current_char = next(self.text)
		except StopIteration:
			self.current_char = None

	def generate_tokens(self):
		while self.current_char != None:
			if self.current_char in WHITESPACE:
				self.advance()
			elif self.current_char == '.' or self.current_char in DIGITS:
				yield self.generate_number()
			elif self.current_char == '+':
				self.advance()
				yield Token(TokenType.PLUS)
			elif self.current_char == '-':
				self.advance()
				yield Token(TokenType.MINUS)
			elif self.current_char == '*':
				self.advance()
				yield Token(TokenType.MULTIPLY)
			elif self.current_char == '/':
				self.advance()
				yield Token(TokenType.DIVIDE)
			elif self.current_char == '(':
				self.advance()
				yield Token(TokenType.LPAREN)
			elif self.current_char == ')':
				self.advance()
				yield Token(TokenType.RPAREN)
			elif self.current_char in OPERATORS:
				yield self.generate_operator()
			else:
				raise Exception(f"Illegal character '{self.current_char}'")


	def generate_number(self):
		decimal_point_count = 0
		number_str = self.current_char
		self.advance()

		while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
			if self.current_char == '.':
				decimal_point_count += 1
				if decimal_point_count > 1:
					break

			number_str += self.current_char
			self.advance()

		if number_str.startswith('.'):
			number_str = '0' + number_str
		if number_str.endswith('.'):
			number_str += '0'

		return Token(TokenType.NUMBER, float(number_str))


	def generate_operator(self):

		operator_str = self.current_char
		self.advance()

		while self.current_char != None and self.current_char in OPERATORS:
			operator_str += self.current_char
			self.advance()

		if operator_str == "<":
			return Token(TokenType.LESS)

		elif operator_str == "<=":
			return Token(TokenType.LESSEQ)

		elif operator_str == "==":
			return Token(TokenType.EQUAL)

		elif operator_str == ">":
			return Token(TokenType.GREATER)

		elif operator_str == ">=":
			return Token(TokenType.GREATEREQ)

		else:
			raise Exception(f"Illegal character '{operator_str}'")
