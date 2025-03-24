from typing import Union, Dict
import re

class Calculator:
    def __init__(self):
        self._cache: Dict[str, float] = {}
    
    def calc(self, expression: str) -> Union[float, str]:
        # 检查缓存
        if expression in self._cache:
            return self._cache[expression]
        
        # 清理输入
        expression = expression.replace(' ', '')
        if not self._is_valid_expression(expression):
            return "错误：表达式包含非法字符"
        
        try:
            result = self._evaluate(expression)
            self._cache[expression] = result
            return result
        except Exception as e:
            return f"错误：{str(e)}"
    
    def _is_valid_expression(self, expr: str) -> bool:
        return bool(re.match(r'^[0-9+\-*/().]+$', expr))
    
    def _evaluate(self, expression: str) -> float:
        def parse_number() -> float:
            nonlocal pos
            num = ''
            while pos < len(expression) and (expression[pos].isdigit() or expression[pos] == '.'):
                num += expression[pos]
                pos += 1
            if not num:
                raise ValueError("非法表达式")
            return float(num)
        
        def parse_term() -> float:
            nonlocal pos
            if pos >= len(expression):
                raise ValueError("非法表达式")
                
            if expression[pos] == '(':
                pos += 1
                result = parse_expression()
                if pos >= len(expression) or expression[pos] != ')':
                    raise ValueError("括号不匹配")
                pos += 1
                return result
            
            return parse_number()
        
        def parse_factor() -> float:
            result = parse_term()
            
            while pos < len(expression) and expression[pos] in '*/':
                op = expression[pos]
                pos += 1
                term = parse_term()
                
                if op == '*':
                    result *= term
                else:  # op == '/'
                    if term == 0:
                        raise ValueError("除数不能为零")
                    result /= term
            
            return result
        
        def parse_expression() -> float:
            result = parse_factor()
            
            while pos < len(expression) and expression[pos] in '+-':
                op = expression[pos]
                pos += 1
                factor = parse_factor()
                
                if op == '+':
                    result += factor
                else:  # op == '-'
                    result -= factor
            
            return result
        
        pos = 0
        result = parse_expression()
        if pos < len(expression):
            raise ValueError("表达式解析错误")
        return result

# 创建计算器实例并提供便捷函数
calculator = Calculator()
def calc(expression: str) -> Union[float, str]:
    return calculator.calc(expression)

if __name__ == "__main__":
    test_expressions = [
        "2 + 3 * 4",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "2 + a",
        "1/0",
    ]
    
    for expr in test_expressions:
        print(f"计算: {expr}")
        print(f"结果: {calc(expr)}\n")
