import unittest
from nodes import *
from interpreter import Interpreter
from values import Number

class TestInterpreter(unittest.TestCase):

	def test_numbers(self):
		value = Interpreter().visit(NumberNode(51.2))
		self.assertEqual(value, Number(51.2))

		value = Interpreter().visit(NumberNode(-12.5))
		self.assertEqual(value, Number(-12.5))


	def test_single_operations(self):
		result = Interpreter().visit(AddNode(NumberNode(27), NumberNode(14)))
		self.assertEqual(result.value, 41)

		result = Interpreter().visit(SubtractNode(NumberNode(27), NumberNode(14)))
		self.assertEqual(result.value, 13)

		result = Interpreter().visit(MultiplyNode(NumberNode(27), NumberNode(14)))
		self.assertEqual(result.value, 378)

		result = Interpreter().visit(DivideNode(NumberNode(27), NumberNode(14)))
		self.assertAlmostEqual(result.value, 1.92857, 5)

		with self.assertRaises(Exception):
			Interpreter().visit(DivideNode(NumberNode(27), NumberNode(0)))


	def test_single_comparisons(self):
		# Less or Equal
		result = Interpreter().visit(LessEqNode(NumberNode(10), NumberNode(10)))
		self.assertEqual(result, True)

		result = Interpreter().visit(LessEqNode(NumberNode(5), NumberNode(10)))
		self.assertEqual(result, True)

		result = Interpreter().visit(LessEqNode(NumberNode(15), NumberNode(10)))
		self.assertEqual(result, False)

		# Less Node
		result = Interpreter().visit(LessNode(NumberNode(15), NumberNode(15)))
		self.assertEqual(result, False)

		result = Interpreter().visit(LessNode(NumberNode(9.66), NumberNode(10)))
		self.assertEqual(result, True)

		result = Interpreter().visit(LessNode(NumberNode(11), NumberNode(10.99)))
		self.assertEqual(result, False)

		# Equality
		result = Interpreter().visit(EqualNode(NumberNode(15), NumberNode(15)))
		self.assertEqual(result, True)

		result = Interpreter().visit(EqualNode(NumberNode(6), NumberNode(-6)))
		self.assertEqual(result, False)

		result = Interpreter().visit(EqualNode(NumberNode(14.6), NumberNode(15.1)))
		self.assertEqual(result, False)

		result = Interpreter().visit(EqualNode(NumberNode(16), NumberNode(15)))
		self.assertEqual(result, False)

		# Greater Node
		result = Interpreter().visit(GreaterNode(NumberNode(12), NumberNode(12)))
		self.assertEqual(result, False)

		result = Interpreter().visit(GreaterNode(NumberNode(12), NumberNode(13)))
		self.assertEqual(result, False)

		result = Interpreter().visit(GreaterNode(NumberNode(12), NumberNode(11)))
		self.assertEqual(result, True)

		result = Interpreter().visit(GreaterNode(NumberNode(7), NumberNode(-7)))
		self.assertEqual(result, True)

		# Greater or Equal
		result = Interpreter().visit(GreaterEqNode(NumberNode(12.56), NumberNode(12.56)))
		self.assertEqual(result, True)

		result = Interpreter().visit(GreaterEqNode(NumberNode(12), NumberNode(-13)))
		self.assertEqual(result, True)

		result = Interpreter().visit(GreaterEqNode(NumberNode(27.2), NumberNode(27)))
		self.assertEqual(result, True)

		result = Interpreter().visit(GreaterEqNode(NumberNode(7), NumberNode(7.01)))
		self.assertEqual(result, False)

		# More than one operator
		with self.assertRaises(Exception):
			result = Interpreter().visit(EqualNode(GreaterEqNode(NumberNode(7), NumberNode(5)), NumberNode(5)))

		with self.assertRaises(Exception):
			result = Interpreter().visit(EqualNode(EqualNode(NumberNode(10), NumberNode(10)), NumberNode(10)))


	def test_full_expression(self):
		tree = AddNode(
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
		)

		result = Interpreter().visit(tree)
		self.assertAlmostEqual(result.value, -2360.08, 2)


	def test_term_comparisons(self):
		tree = GreaterNode(
			DivideNode(
				NumberNode(1558),
				NumberNode(18)
			),
			MultiplyNode(
				NumberNode(12.3),
				NumberNode(3.5)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, True)

		tree = EqualNode(
			DivideNode(
				NumberNode(1500),
				NumberNode(8)
			),
			MultiplyNode(
				NumberNode(62.5),
				NumberNode(3)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, True)

		tree = LessNode(
			MultiplyNode(
				NumberNode(15),
				NumberNode(18)
			),
			MultiplyNode(
				NumberNode(100),
				NumberNode(2)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, False)


	def test_expression_comparisons(self):
		tree = EqualNode(
			AddNode(
				NumberNode(27),
				MultiplyNode(
					SubtractNode(
						DivideNode(
							NumberNode(48),
							NumberNode(12)
						),
						NumberNode(2)
					),
					NumberNode(12)
				)
			),
			AddNode(
				MultiplyNode(
					NumberNode(4),
					NumberNode(12.5)
				),
				NumberNode(1)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, True)

		tree = GreaterNode(
			SubtractNode (
				MultiplyNode(
					NumberNode(5),
					NumberNode(12)
				),
				DivideNode(
					NumberNode(1000),
					NumberNode(24)
				)
			),
			AddNode(
				NumberNode(1000),
				MultiplyNode(
					NumberNode(48),
					NumberNode(12)
				)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, False)

		tree = LessEqNode(
			AddNode(
				NumberNode(27),
				MultiplyNode(
					SubtractNode(
						DivideNode(
							NumberNode(48),
							NumberNode(12)
						),
						NumberNode(2)
					),
					NumberNode(12)
				)
			),
			AddNode(
				MultiplyNode(
					NumberNode(4),
					NumberNode(12.5)
				),
				NumberNode(1)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, True)

		tree = GreaterNode(
			AddNode(
				NumberNode(1000),
				MultiplyNode(
					NumberNode(48),
					NumberNode(12)
				)
			),
			SubtractNode (
				MultiplyNode(
					NumberNode(5),
					NumberNode(12)
				),
				DivideNode(
					NumberNode(1000),
					NumberNode(24)
				)
			)
		)

		result = Interpreter().visit(tree)
		self.assertEqual(result, True)
