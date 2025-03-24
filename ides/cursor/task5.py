import re
import sys
import argparse
from typing import Dict, List, Tuple, Union, Optional
from functools import lru_cache

class ExpressionError(Exception):
    """用于表示表达式解析或计算错误的异常类"""
    pass

class Calculator:
    """计算器类，支持解析和计算数学表达式"""
    
    def __init__(self):
        """初始化计算器，设置表达式缓存"""
        self.expression_cache: Dict[str, float] = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def tokenize(self, expression: str) -> List[str]:
        """
        将表达式字符串转换为标记列表
        
        参数:
            expression: 要解析的表达式字符串
            
        返回:
            标记列表
            
        抛出:
            ExpressionError: 当表达式包含无效字符时
        """
        # 删除所有空白
        expression = expression.replace(" ", "")
        
        # 定义合法字符模式
        pattern = r'(\d+\.\d+|\d+|[\+\-\*/\(\)])'
        tokens = re.findall(pattern, expression)
        
        # 检查是否有无效字符
        reconstructed = ''.join(tokens)
        if reconstructed != expression:
            invalid_chars = set(char for char in expression if not char.isdigit() and char not in "+-*/().")
            raise ExpressionError(f"表达式包含无效字符: {', '.join(invalid_chars)}")
        
        return tokens
    
    def to_postfix(self, tokens: List[str]) -> List[str]:
        """
        将中缀表达式转换为后缀表达式（逆波兰表示法）
        
        参数:
            tokens: 标记列表
            
        返回:
            后缀表达式列表
            
        抛出:
            ExpressionError: 当括号不匹配时
        """
        # 运算符优先级
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        
        output = []
        operator_stack = []
        
        for token in tokens:
            # 数字直接输出
            if self._is_number(token):
                output.append(token)
            # 左括号入栈
            elif token == '(':
                operator_stack.append(token)
            # 右括号处理
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                    
                if not operator_stack or operator_stack[-1] != '(':
                    raise ExpressionError("括号不匹配: 多余的右括号")
                    
                operator_stack.pop()  # 弹出左括号
            # 运算符处理
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(operator_stack.pop())
                    
                operator_stack.append(token)
            else:
                raise ExpressionError(f"未知标记: {token}")
        
        # 处理剩余的运算符
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ExpressionError("括号不匹配: 多余的左括号")
                
            output.append(operator_stack.pop())
            
        return output
    
    def evaluate_postfix(self, postfix: List[str]) -> float:
        """
        计算后缀表达式的值
        
        参数:
            postfix: 后缀表达式列表
            
        返回:
            表达式的计算结果
            
        抛出:
            ExpressionError: 当表达式格式无效或除以零时
        """
        stack = []
        
        for token in postfix:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ExpressionError("表达式格式无效")
                    
                # 注意操作数的顺序
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ExpressionError("除以零错误")
                    stack.append(a / b)
        
        if len(stack) != 1:
            raise ExpressionError("表达式格式无效")
            
        return stack[0]
    
    def _is_number(self, token: str) -> bool:
        """检查标记是否为数字"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def calc(self, expression: str) -> float:
        """
        计算表达式的值，并使用缓存机制
        
        参数:
            expression: 要计算的表达式字符串
            
        返回:
            表达式的计算结果
            
        抛出:
            ExpressionError: 当表达式无效时
        """
        # 规范化表达式（去除空格）
        normalized_expr = expression.replace(" ", "")
        
        # 检查缓存
        if normalized_expr in self.expression_cache:
            self.cache_hits += 1
            print(f"[缓存命中] 表达式: {expression}")
            return self.expression_cache[normalized_expr]
        
        self.cache_misses += 1
        print(f"[计算] 表达式: {expression}")
        
        try:
            # 解析和计算表达式
            tokens = self.tokenize(expression)
            postfix = self.to_postfix(tokens)
            result = self.evaluate_postfix(postfix)
            
            # 更新缓存
            self.expression_cache[normalized_expr] = result
            return result
            
        except ExpressionError as e:
            # 不缓存无效表达式
            raise e
    
    def get_cache_stats(self) -> Dict[str, int]:
        """返回缓存统计信息"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total) * 100 if total > 0 else 0
        
        return {
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'total': total,
            'hit_rate': hit_rate
        }
    
    def clear_cache(self) -> None:
        """清除表达式缓存"""
        self.expression_cache.clear()
        print("缓存已清除")

def main():
    parser = argparse.ArgumentParser(description='计算数学表达式的命令行工具')
    parser.add_argument('expression', nargs='?', help='要计算的数学表达式')
    parser.add_argument('--stats', action='store_true', help='显示缓存统计信息')
    parser.add_argument('--clear-cache', action='store_true', help='清除表达式缓存')
    
    args = parser.parse_args()
    
    # 创建计算器实例
    calculator = Calculator()
    
    if args.clear_cache:
        calculator.clear_cache()
        return
        
    if args.stats:
        stats = calculator.get_cache_stats()
        print(f"缓存统计信息:")
        print(f"  命中: {stats['hits']}")
        print(f"  未命中: {stats['misses']}")
        print(f"  总请求: {stats['total']}")
        print(f"  命中率: {stats['hit_rate']:.2f}%")
        return
    
    # 交互模式
    if not args.expression:
        print("数学表达式计算器")
        print("支持: +, -, *, /, 和括号")
        print("示例: 2 + 3 * 4")
        print("输入 'exit' 或 'quit' 退出")
        print("输入 'stats' 查看缓存统计")
        print("输入 'clear' 清除缓存")
        print("-" * 40)
        
        while True:
            try:
                expression = input(">>> ")
                
                if expression.lower() in ('exit', 'quit'):
                    break
                elif expression.lower() == 'stats':
                    stats = calculator.get_cache_stats()
                    print(f"缓存统计信息:")
                    print(f"  命中: {stats['hits']}")
                    print(f"  未命中: {stats['misses']}")
                    print(f"  总请求: {stats['total']}")
                    print(f"  命中率: {stats['hit_rate']:.2f}%")
                    continue
                elif expression.lower() == 'clear':
                    calculator.clear_cache()
                    continue
                elif not expression.strip():
                    continue
                
                result = calculator.calc(expression)
                print(f"结果: {result}")
                
            except ExpressionError as e:
                print(f"错误: {e}")
            except KeyboardInterrupt:
                print("\n再见!")
                break
            except Exception as e:
                print(f"发生意外错误: {e}")
    else:
        # 单次计算模式
        try:
            result = calculator.calc(args.expression)
            print(f"结果: {result}")
        except ExpressionError as e:
            print(f"错误: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 