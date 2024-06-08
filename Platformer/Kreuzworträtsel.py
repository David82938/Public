import random
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
characters = "^1234567890ß´qwertzuiopü+asdfghjklöä#<yxcvbnm,.-°!\"§$%&/()=?`QWERTZUIOPÜ*ASDFGHJKLÖÄ'>YXCVBNM;:_„¡“¶¢[]|{}≠¿'"
l = 0
while l < 10000:
    l += 1
    print(random.choice(abc), end="")