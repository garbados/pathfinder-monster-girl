import os
import random
import re
import sys

LOG = True if 'LOG' in os.environ else False
SIMPLE = True if 'SIMPLE' in os.environ else False

def dN(n):
	return random.randint(1, n)

def roll(n=1, m=20, x=0, b=None, w=None):
	"""
	Roll N dM dice, adding X to the sum.
	If `b` is an integer, take the highest `b` rolls.
	Or if `w` is an integer, take the lowest `w` rolls.
	"""
	rolls = [dN(m) for i in range(n)]
	rolls.sort()
	if LOG:
		print("Rolls:", rolls)
	if isinstance(b, int):
		rolls = rolls[-b:]
	elif isinstance(w, int):
		rolls = rolls[:w]
	return sum(rolls) + x

# Convenience methods for accessing roll
def d4(n=1, *args, **kwargs):
	return roll(n, 4, *args, **kwargs)
def d6(n=1, *args, **kwargs):
	return roll(n, 6, *args, **kwargs)
def d8(n=1, *args, **kwargs):
	return roll(n, 8, *args, **kwargs)
def d10(n=1, *args, **kwargs):
	return roll(n, 10, *args, **kwargs)
def d12(n=1, *args, **kwargs):
	return roll(n, 12, *args, **kwargs)
def d20(n=1, *args, **kwargs):
	return roll(n, 20, *args, **kwargs)
def d100(n=1, *args, **kwargs):
	return roll(n, 100, *args, **kwargs)

def express(n, m, b, w, x):
	expression = '{}d{}'.format(n, m)
	if b is not None:
		expression += 'b{}'.format(b)
	elif w is not None:
		expression += 'w{}'.format(w)
	if x > 0:
		expression += '+{}'.format(x)
	elif x < 0:
		expression += '-{}'.format(-x)
	return expression

# Handle expressions like "5d6b2+3"
expression_regex = '(\d+?)?d(\d+)(b(\d+?))?(w(\d+?))?(\-(\d+?))?'
def parse(expression):
	try:
		result = int(expression)
		return result
	except ValueError:
		# parse normally
		pass
	matches = re.findall(expression_regex, expression)
	results = []
	for match in matches:
		n = int(match[0]) if match[0] else 1
		m = int(match[1]) if match[1] else 20
		b = int(match[3]) if match[3] else None
		w = int(match[5]) if match[5] else None
		x = -int(match[7]) if match[7] else 0
		if LOG:
			this_expression = express(n, m, b, w, x)
			print('Eval: {}'.format(this_expression))
		# roll the dice!
		result = roll(n, m, x, b, w)
		results.append(result)
		# log the mapping of expressions to results
		if LOG:
			print('Result: {} => {}'.format(this_expression, result))
	return sum(results)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Needs at least one dice expression to evaluate.')
		print('Use the `-v, --verbose` flag to print rolls and results.')
		print('Ex: python roll.py 2d20b1')
		print('Ex: python roll.py 2d20w1')
		print('Ex: python roll.py 5d6+3')
		print('Ex: python roll.py 1d8 1d6 1d4 1d3+2')
	else:
		# handle options
		options = [argv for argv in sys.argv if argv[0] == '-']
		if '-v' in options or '--verbose' in options:
			LOG = True
		# sum dice expressions
		args = [argv for argv in sys.argv[1:] if argv[0] != '-']
		for exp_group in args:
			exps = exp_group.split('+')
			results = [parse(exp) for exp in exps]
			result = sum(results)
			if LOG:
				print('Sum: {}'.format(result))
			else:
				print(' => '.join([exp_group, str(result)]))
