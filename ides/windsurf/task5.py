#!/usr/bin/env python3
"""
Task 5: Creative Problem Solving and Complex Requirements
Math Expression Calculator with Caching

Features:
- Parses and evaluates mathematical expressions with operator precedence
- Supports addition, subtraction, multiplication, division, and parentheses
- Implements a caching mechanism for repeated expressions
- Provides user-friendly error messages
"""
import re
import argparse
from typing import Dict, Tuple, Union, List, Optional
from functools import lru_cache


# Expression Tokens
NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'


class Token:
    """Token class to represent lexical tokens in the expression."""
    def __init__(self, type_: str, value: Union[str, float]):
        self.type = type_
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'

    def __repr__(self) -> str:
        return self.__str__()


class Lexer:
    """
    Lexer to tokenize the input expression string.
    Converts raw text into a stream of tokens.
    """
    def __init__(self, text: str):
        # Remove all whitespace from the input text
        self.text = text.replace(' ', '')
        self.pos = 0
        self.current_char = self.text[0] if self.text else None

    def error(self) -> None:
        """Raise an exception for invalid character."""
        raise ValueError(f"Invalid character: '{self.current_char}'")

    def advance(self) -> None:
        """Move to the next character in the input."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def number(self) -> float:
        """
        Parse a multi-digit number (integer or float).
        Returns the number as a float.
        """
        result = ''
        
        # Handle the integer part
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Handle decimal point if present
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            
            # Handle the decimal part
            if not (self.current_char is not None and self.current_char.isdigit()):
                raise ValueError("Invalid float format: expected digits after decimal point")
                
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        return float(result)

    def get_next_token(self) -> Token:
        """
        Tokenize the input text.
        Returns the next token in the sequence.
        """
        while self.current_char is not None:
            
            # Handle digits
            if self.current_char.isdigit():
                return Token(NUMBER, self.number())

            # Handle operators and parentheses
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
                
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
                
            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')
                
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
                
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
                
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            # If none of the above, we have an invalid character
            self.error()
            
        # End of input
        return Token(EOF, None)


class Parser:
    """
    Parser that implements a recursive descent parser.
    Grammar:
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MULTIPLY | DIVIDE) factor)*
        factor : NUMBER | LPAREN expr RPAREN | (PLUS | MINUS) factor
    """
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected: Optional[str] = None) -> None:
        """Raise an exception for syntax errors."""
        if expected:
            msg = f"Syntax Error: Expected {expected}, got {self.current_token.type}"
        else:
            msg = f"Syntax Error at token: {self.current_token}"
        raise SyntaxError(msg)

    def eat(self, token_type: str) -> None:
        """
        Consume the current token if it matches the expected type.
        Otherwise, raise a syntax error.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self) -> float:
        """Parse a factor in the expression grammar."""
        token = self.current_token
        
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
            
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
            
        # Handle unary operators
        elif token.type in (PLUS, MINUS):
            if token.type == PLUS:
                self.eat(PLUS)
                return self.factor()
            else:
                self.eat(MINUS)
                return -self.factor()
                
        self.error()

    def term(self) -> float:
        """Parse a term in the expression grammar."""
        result = self.factor()
        
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
                
        return result

    def expr(self) -> float:
        """Parse an expression in the expression grammar."""
        result = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
                
        return result

    def parse(self) -> float:
        """Parse the entire expression and return the result."""
        result = self.expr()
        
        # Check if the entire input is consumed
        if self.current_token.type != EOF:
            self.error("EOF")
            
        return result


# Create a cache for storing expression results
expression_cache: Dict[str, float] = {}


def calc(expression: str, use_cache: bool = True) -> Union[float, str]:
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression: A string containing a mathematical expression
        use_cache: Whether to use the cache mechanism
        
    Returns:
        The result of the expression, or an error message string
    """
    # Clean the expression by removing all whitespace
    clean_expr = expression.replace(' ', '')
    
    # Check if result is in cache
    if use_cache and clean_expr in expression_cache:
        print(f"Cache hit for: '{expression}'")
        return expression_cache[clean_expr]
    
    try:
        lexer = Lexer(clean_expr)
        parser = Parser(lexer)
        result = parser.parse()
        
        # Store result in cache
        if use_cache:
            expression_cache[clean_expr] = result
            
        return result
        
    except (ValueError, SyntaxError, ZeroDivisionError) as e:
        return f"Error: {str(e)}"


def pretty_print_result(expression: str, result: Union[float, str]) -> None:
    """Format and print the result of an expression."""
    if isinstance(result, str):  # It's an error message
        print(f"Expression: '{expression}'")
        print(f"{result}")
    else:
        print(f"Expression: '{expression}'")
        # Display as integer if it's a whole number
        if result == int(result):
            print(f"Result: {int(result)}")
        else:
            print(f"Result: {result}")
    print()


def interactive_mode() -> None:
    """Run the calculator in interactive mode."""
    print("Math Expression Calculator")
    print("Type 'exit' or 'quit' to exit")
    print("Type 'cache clear' to clear the cache")
    print("Type 'cache status' to see cache statistics")
    print("-" * 40)
    
    while True:
        try:
            expression = input(">>> ")
            
            if expression.lower() in ('exit', 'quit'):
                break
                
            if expression.lower() == 'cache clear':
                expression_cache.clear()
                print("Cache cleared")
                continue
                
            if expression.lower() == 'cache status':
                print(f"Cache size: {len(expression_cache)} entries")
                print(f"Cached expressions: {list(expression_cache.keys())}")
                continue
                
            result = calc(expression)
            pretty_print_result(expression, result)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Math Expression Calculator')
    parser.add_argument('expression', nargs='?', help='Expression to evaluate')
    parser.add_argument('--no-cache', action='store_true', help='Disable caching')
    
    args = parser.parse_args()
    
    if args.expression:
        # Command line mode
        result = calc(args.expression, not args.no_cache)
        pretty_print_result(args.expression, result)
    else:
        # Interactive mode
        interactive_mode()
