from tkinter import *
from tkinter import messagebox
from sympy import *

def laba():
    mod = int(entry2.get())


    OPERATORS = {'+': (1, lambda x, y: (x + y) % mod ), '-': (1, lambda x, y: (x - y) % mod),
                '*': (2, lambda x, y: (x * y) % mod), '/': (2, lambda x, y: ((x * (euclid_ext(y,mod)[1] % mod))) % mod)}




    def euclid_ext(a, b):
        if b == 0:  
            return a, 1, 0
        else:
            d, x, y = euclid_ext(b, a % b)
            return d, y, x - y * (a // b)


    formula_string = entry1.get()

    if isprime(mod):
        def eval_(formula_string):
            def parse(formula_string):
                number = ''
                for s in formula_string:
                    if s in '1234567890.': # если символ - цифра, то собираем число
                        number += s  
                    elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                        yield int(number) 
                        number = ''
                    if s in OPERATORS or s in "()": # если символ - оператор или скобка, то выдаём как есть
                        yield s


                if number:  # если в конце строки есть число, выдаём его
                    yield int(number) 

            def shunting_yard(parsed_formula):
                
                stack = []  # в качестве стэка используем список
                for token in parsed_formula:
                    # если элемент - оператор, то отправляем дальше все операторы из стека, 
                    # чей приоритет больше или равен пришедшему,
                    # до открывающей скобки или опустошения стека.
                    # здесь мы пользуемся тем, что все операторы право-ассоциативны
                    if token in OPERATORS: 
                        while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                            yield stack.pop()
                        stack.append(token)
                    elif token == ")":
                        # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                        # а открывающую скобку выкидываем из стека.
                        while stack:
                            x = stack.pop()
                            if x == "(":
                                break
                            yield x
                    elif token == "(":
                        # если элемент - открывающая скобка, просто положим её в стек
                        stack.append(token)
                    elif str(token).isdigit():
                        # если элемент - число, отправим его сразу на выход
                        yield token
                    else:
                        break

                while stack:
                    yield stack.pop()

            def calc(polish):
                stack = []
                try:
                    for token in polish:
                        if token in OPERATORS:  # если приходящий элемент - оператор,
                            if token == '/':
                                y, x = stack.pop(), stack.pop()
                                if y == 0:
                                    print('')
                                else:
                                    stack.append(OPERATORS[token][1](x, y))
                            else:   
                                y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                                stack.append(OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
                        else:
                            stack.append(token)

                    return stack[0] # результат вычисления - единственный элемент в стеке
                except TypeError:
                    messagebox.showerror(title='Ошибка, дядь', message="GG")
                except IndexError:
                    messagebox.showerror(title='Ошибка, дядь', message="GG")

            return calc(shunting_yard(parse(formula_string))) 



        label1.config(text = eval_(formula_string))


    else:
        messagebox.showerror(title='Ошибка, дядь', message="GG")


window = Tk()
window.title("Лаба 1")
window.geometry("500x500+680+300")

entry1 = Entry(width=60)
entry1.place(x=2, y=20)

entry2 = Entry(width=10)
entry2.place(x=425, y=20)

Button = Button(text="", command=laba,width=20,height=3,bg="purple")
Button.pack(expand=True)
Button.place(x=180, y=440)

label1 = Label()
label1.config(font=("Courier", 120))
label1.place(x = 180, y = 150)

label2 = Label(text = 'mod')
label2.place(x = 390, y = 20)
 
window.mainloop()
