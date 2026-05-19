#运算符（逻辑与成员）
# 比较运算符

from py学习 import fruits

print(5 == 5)
print(5 != 5)
print(5 > 5)
print(5 < 5)
print(5 >= 5)
print(5 <= 5)
# 逻辑运算符
# 在py这些逻辑运算符不是&& 或者 ||  而是英文单词
print(True and False) # 逻辑与
print(True or False)# 逻辑或
print(not True)# 逻辑非
# 成员运算符
fruits = ["apple", "banana", "cherry"]
if "apple" in fruits: # 判断元素是否在列表中
    print("apple is in the list")
if "orange" not in fruits: # 判断元素是否不在列表中
    print("orange is not in the list")

#while 循环 只要条件为真，就一直循环（小心死循环）
count = 0
while count < 3:
    print(count)
    count += 1
#break 直接跳出循环 和 continue 跳过本次循环
for i in range(5): # 只会输出0 1 3
    if i==2:
        continue #跳过2直接输出3
    if i==4:
        break #终止循环
    print(i)
# 字符串
text = "Hello, Python!"
#切片 索引0到4的字符
print(text[0:5])
print(text.lower())#字符串全部转小写
print(text.replace("Python", "World")) #替换字符串中的内容
words = "apple, banana, orange"
print(words.split(",")) #用逗号分割字符串，返回一个列表
name = " enkidu "
print(name.strip()) #去除字符串两端的空格

#数据类型补充：集合
# 有列表元组字典还差一个：元组
# 特点 用大括号{}，里面的数据没有顺序，且不能重复
# 最常见的用途，给列表去重
nums = [1, 2, 2, 3, 4, 4, 5]
unique_nums = set(nums)
print(unique_nums)
#列表操作方法
fruits = ["apple", "banana", "cherry"]
# 删除指定元素
fruits.remove("banana")
print(fruits)
#弹出最后一个元素 也可以弹出指定位置
last_fruit = fruits.pop()
print(last_fruit) # 输出为 cherry
# 列表合并
other_fruits = ["dog","cat"]
all_things = fruits + other_fruits
print(all_things) # 输出为 ['apple', 'dog', 'cat']
# 函数进阶 默认参数与不定长参数
# 你的函数都是必须传参的，但实际开发中经常需要可选参数
def say_hello(name="匿名"):
    print(f"hello {name}")
say_hello()
say_hello("Alice")
#*args 接收任意数量参数，打包成元组
def calc_sum(*args):
    total = 0
    for n in args:
        total += n
    print(total)
calc_sum(1, 2, 3, 4, 5)
#匿名函数
multiply = lambda x,y: x*y
print(multiply(3,4))
#异常处理
# 程序总会遇到bug，如果不处理程序会直接崩溃
try: # 尝试执行的代码
    num = int(input("请输入一个数字："))
    result = 10 / num
    print(f"结果是{result}")
except ValueError as e:
    # 如果上面的值报错比如输入了abc字母
    print("error 你输入的不是数字")
except ZeroDivisionError as e:
    # 如果上面报错除以0错误
    print("error 除以0错误")
finally:
    # 无论程序是否报错，都会执行
    print("程序结束")

# 文件操作
#写入文件 w 代表写入 a 代表追加
with open("../test.txt", "w", encoding="utf-8") as file:
    file.write("第一行文字\n")
    file.write("第二行文字\n")
# 读取文件 r 代表读取
with open("../test.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
# 模块导入
import math #导入py自带的数学模块
print(math.sqrt(16)) # 输出4.0 开平方 开平方就是找哪个数乘以自己等于目标数
import random #导入py自带的随机模块
print(random.randint(1,10)) #输出1到10的随机整数
# 只导入time模块的 sleep 函数
from time import sleep
print("开始等待")
sleep(2)
print("继续运行")

# oop 继承
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(f"{self.name} 发出了声音")
class Dog(Animal):
    def speak(self):
        print(f"{self.name} 说汪汪汪")
class Cat(Animal):
    def speak(self):
        print(f"{self.name} 说喵喵喵")
dog = Dog("旺财")
dog.speak()




