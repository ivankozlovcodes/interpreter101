#!/usr/local/bin/python

import os
import sys
from util import *

# constants
DEBUG = 0
test = "( 2 + --3 )"
operators = ['+', '-', '*', '/', '%', '^']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

input = get_input() if DEBUG is 0 else test

def get_precedence(op):
	if op == '-' or op == '+':
		return 13
	elif op == '*' or op == '/' or op == '%':
		return 14
	elif op == '^':
		return 15
	return -1

def opcmp(op1, op2):
	return get_precedence(op1) - get_precedence(op2)

def tokenize(input):
	result = []
	tokens = input.split(' ')
	for token in tokens:
		i = 0
		while i < len(token):
			c = token[i]
			if c in numbers:
				tail = token[i:]
				for j in range(0, len(tail)):
					if tail[j] not in numbers:
						break
				if j is len(tail) - 1 and tail[j] in numbers:
					j += 1
				result.append(token[i:i+j])
				i += j
			else:
				result.append(c)
				i += 1
	return result

def infix_to_postfix(infix):
	sign = 1
	rpn = []
	stack = []
	lastop = True

	print(infix)
	for idx, token in enumerate(infix):
		if token is '-' or token is '+' and lastop is True:
			sign = -1 if token is '-' else 1
			if idx < len(infix) and infix[idx + 1] in operators:
				raise Exception("Incorrect token '{}' at pos {}".format(infix[idx + 1], idx + 1))
		if token in operators:
			while len(stack) > 0 and opcmp(stack[-1], token) >= 0:
				rpn.append(stack.pop())
			stack.append(token)
			lastop = True
		elif token == '(':
			stack.append(token)
		elif token == ')':
			while stack[-1] != '(':
				rpn.append(stack.pop())
			stack.pop()
			lastop = False
		else:
			rpn.append(str(sign * int(token)))
			sign = 1
			lastop = False

	while len(stack) != 0:
		rpn.append(stack.pop())

	return rpn

rpn = infix_to_postfix(tokenize(input))
for el in rpn:
	puts(el + ' ')
print()