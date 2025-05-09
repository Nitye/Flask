# class dog():
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age
  
#   def add_age(self, age):
#     dog.age+=age

# d1 = dog('Tim', 34)
# d2 = dog('Bill', 12)
# d1.add_age(10)
# print(d1.age)
# print(d2.age)
# class A:
#     instances = []
#     def __init__(self):
#         self.__class__.instances.append(self)
# a1 = A()
# a2 = A()
# l3 = [a2,a1]
# print(A.instances)
# print(l3)
# l1  = (1,2,3)
# l2 =  (2,3,1)
# print(l1 == l2)
# dog = [1,22,3]
# dog2 = dog.copy()
# dog.remove(1)
# dog2.remove(1)
# print(dog)
# import cards
# hands = cards.distribute_cards(3)
# print(cards.compare_hands(hands, 3))
l1 = [1,2,40,5]
l1.remove(40)
print(l1)
d2 = {'a':1,'b':2}
d2.pop('b')
print(d2)