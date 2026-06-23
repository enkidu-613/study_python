#列表推导式
#老写法
from symbol import pass_stmt

list1 = [1,2,3,4,5]
result1 = []
for item in list1:
    result1.append(item * 10)
print(result1)
# 新写法
list2 = [1,2,3,4,5]
result2 = [item * 10 for item in list2]
print(result2)
#进阶 带筛选条件 只要偶数
result3 = [item * 10 for item in list2 if item % 2== 0]
print(result3)
# 示例 将游戏人物改名
heros = ['hero1', 'hero2', 'hero3']
result4 = [f"super {hero}" for hero in heros]
print(result4)
#生成器 不会爆内存的无限零食机
# 如果你要生成无限数字 尽量不要使用for而是使用生成器，不然会卡死
# 新写法 () 生成器写法，把中括号改为小括号
nums = (i**2 for i in range(1000000))
#此时内存里根本没有生成数字而是记住了方法

#需要他的时候才会吐出来
print(next(nums)) #0
print(next(nums)) #1
print(next(nums)) #4
print(next(nums)) #9

# 使用函数作为生成器
def 摸奖机():
    yield "普通奖励"
    yield "高级奖励"
    yield "金色传说"
抽奖 = 摸奖机()
print(next(抽奖))#普通奖励
print(next(抽奖))#高级奖励
print(next(抽奖))#金色传说

#非典型的生成器
def 非典型生成器():
    try:
        yield "这是步进器弹出的数据"
    finally:
        print("这是finally执行的逻辑")
# 定义一个非典型生成器实例
非典型生成器实例 = 非典型生成器()
try:
    print(next(非典型生成器实例))
    print(next(非典型生成器实例))
except StopIteration:
    pass
# 装饰器
# 如果你要每个函数前面都要加一个正在运行，你要去改100次代码吗？
#解药：装饰器。他像一个外挂直接套在函数外面不修改原来的代码

#这是我们的外挂装备
def 加计时器(原函数):
    def 穿上装备后(*args, **kwargs):
        print("开始运行。。。")
        res = 原函数(*args, **kwargs)
        print("运行结束")
        return res
    return 穿上装备后
@加计时器
def 打怪():
    print("打怪开始")
@加计时器
def 买药水():
    print("买药水开始")
#测试
打怪()
买药水()









