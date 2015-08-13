# coding: utf-8
# *************************************
#
# ジェネレータ
#	ループ処理やシーケンスを返す場合は
#	ジェネレータの使用を考えるべき
#	リストを返すまえに、ジェネレータの利用を検討すべき
#
# *************************************


def fibonacci():
    a, b = 0., 1.
    while True:
        yield b
        a, b = b, a + b


fib = fibonacci()
b = [next(fib) for i in range(1000)]
print b
