# 基础类型
from xxlimited import new

message = "hello world"
Message = "你好世界"  # 变量大小写区分，开头禁止数字和部分符号除了_
age = 18
pi = 3.14
is_student = True
print(message, age, pi, is_student)
print(type(message), type(age), type(pi), type(is_student))
# 列表
fruits = ["apple", "banana", "cherry"]
print(fruits)
print(fruits[0])  # 输出为 apple
fruits[0] = 'plum'
print(fruits)
fruits.append('watermelon')
print(fruits)
# 元组 元组内的数据不能被添加删除修改
fruits_tuple = ("apple", "banana", "cherry", "orange")
#
for fruit in fruits:
    print(fruit)
# range 从零开始计数到指定的数字
for i in range(10):
    print(i ** 2)  # 输出i的平方，**是幂运算符 意思为 i*i 也就是i的i次方
# for循环求和
total = 0
num = [1, 2, 3, 4, 5]
for n in num:
    total += n

print(total)

# if 语句
age = 65
if age < 18:
    print("未成年")
elif age < 65:
    print("成年")
else:
    print("老年")

# 字典 dict 是一个键值对的集合
person = {
    "name": "Alice",
    "age": 18,
    "city": "New York"
}
# 如果想要访问字典中的值，可以使用键名
print(person["name"])
# 如果想要获取对象所有的键
print(person.keys())
# 如果想要获取对象所有的值
print(person.values())
# 如果想要获取对象所有的键值对
print(person.items())
# 使用键值对做一个for循环
for k, v in person.items():
    print(k, ":", v)


# 函数
def hello_world():
    print("hello world")


hello_world()


# 带参数的函数
def hello_world(name):
    print("hello world", name)


hello_world("Alice")


# 使用f字符串来构建上面的函数，类似于js的模板字符串 ``
def hello_world(name):
    print(f"hello world {name}")


hello_world("Alice")


def square(num):
    return num ** 2


print(square(5))


def sum_fun(arr):
    total_value = 0
    for num_value in arr:
        total_value += num_value
    return total_value


print(sum_fun([1, 2, 3, 4, 5]))

#oop
class Calculator:
    def __init__(self, num):
        self.num = num
    def sum(self):
        total = 0
        for i in self.num:
            total += i
        return total
    def avg(self):
        return self.sum() / len(self.num)

calc = Calculator(num)
print(calc.sum())
print(calc.avg())



