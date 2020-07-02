#装饰器的使用 
#这里使用一个装饰器进行缓存
# 斐波那契额数列初始方法
def memo(func):
    cache = {}
    def wrap(*args):
        res = cache.get(args)
        if not res:
            res = cache[args] = func(*args)
        return res
    return wrap


@memo
def fibonacci(n):
    if n<=1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))


#爬楼梯100节，可以一节到三节，共多少种方法
@memo
def climb(n,steps):
    count = 0
    if n == 0:
        count = 1
    elif n>0:
        for step in steps:
            count += climb(n-step,steps)
    return count

print(climb(100,(1,2,3)))