# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# My class is going to keep the students information
# I am going to keep first and last name and age of the student and their macid

# Explanation about Assignment number 5

# Check how arithmetic addressed in Java programming language. See how pointers addressed in it.
# Check how references refered to in Java.
# Then try to find out what would be the affect of arthemtic on object/value.

# Explanation about Assignment Number 6
# In assigment #7 we asked you to define two classes and then try to implement `__eq__` and `__ne__`
# constructors for them. It will be very similar to what I did below. But with different names and attributes.
# Later for question #6, you need to trace what would happen if you compair a Fruit with a Plant. It means:
# 1. What if none of `__eq__` or `__ne__` defined?
# 2. What if none of `__eq__` defined for Plant but not for Fruit?
# 3. What if none of `__eq__` defined for Fruit but not for Plant?
# 4. What if none of `__ne__` defined for Plant but not for Fruit?
# 5. What if none of `__ne__` defined for Fruit but not for Plant?
# 6. What if `__eq__` define for one and `__ne__` define for the other?
# 7. etc.

# You need to discuss how python interpret react in each of the above cases. How decision tree going to work.


class Student(object):
    """
    This is docstring. This class holds information related to mcmaster students
    """

    # Initialize the instance of an object
    def __init__(self, first_name, last_name, mac_id, age=10):
        self.first_name = first_name
        self.last_name = last_name
        self.mac_id = mac_id
        self.age = age

    def __eq__(self, other):
        return (self.age == other.age and self.first_name == other.first_name
                and self.last_name == other.last_name and self.mac_id == other.mac_id)

    # def __eq__(self, other):
    #     return (self.age == other.age)

    # Can keep functions (Define functions)
    # <function Student.greet at 0x104a3ef70>
    # As soon as we define a class, a new class object is created with the same name
    def greet(self):
        print("Hello")

    def get_data(self):
        print(
            f'''You are looking at {self.first_name} {self.last_name} information with MacID = {self.mac_id} and 
            age of {self.age}.''')

class EngFac(Student):
    def __init__(self, first_name, last_name, mac_id, faculity_name, age=10):
        super().__init__(first_name, last_name, mac_id, age)
        self.faculity_name = faculity_name

    # Check the exercise description to find out what you need to next

# Play with the code see how it works
habib = Student('Habib', 'Gh', 'ghaffh1', 10)
tom = Student('Tom', 'Cheng', 'chengt2', 10)


print(habib == tom)

habib.get_data()

class A(object):
    def __eq__(self, other):
        print("A __eq__ called : %r == %r ?" % (self, other))
        return self.value == other


class B(object):
    def __eq__(self, other):
        print("B __eq__ called : %r == %r ?" % (self, other))
        return self.value == other


a = A()
a.value = 3
b = B()
b.value = 4

a == b

# To do the definition for __eq__, __ne__ (What if you do not define ne in one python class?)
# (What if you do not define __eq__)

# Whenver I am calling greet, the first argument that going to be passed to this class is going to be the instance of
# the object (habib)
# print(Student.__doc__)
#
# print(Student.greet)
# print(habib.greet())
