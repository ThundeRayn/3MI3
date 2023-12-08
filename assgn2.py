class Plant:
    def __init__(self,type_name):
        self.type_name = type_name
        
    def __eq__(self, other): 
        if not isinstance(other, Plant):
            return NotImplemented
        return self.type_name == other.type_name

    def __ne__(self, other): 
        if not isinstance(other, Fruit):
            return NotImplemented
        return True #you can not be sure if you don't taste it
    
    # I set any apple to be sweet here, so we can have differnt type eq
    
class Fruit(Plant):
    def __init__(self,type_name,taste):
        self.type_name = type_name
        self.taste = taste
        
    def __eq__(self, other): 
        if not isinstance(other, Fruit):
            return NotImplemented
        return self.type_name == other.type_name and self.taste == other.taste

    def __eq__(self, other): 
        if not isinstance(other, Plant):
            return NotImplemented
        return self.type_name == other.type_name #sweet apples are apple

def main():
    a = Plant("Maple");
    print(a)
    b = Plant("Maple");

    if a == b:
        print("a and b are equal")
    else:
        print("a and b are not equal");
    if a != b:
        print("a and b are not equal")
    else:
        print("a and b are equal")
        
    c = Fruit("Apple","sweet")
    print(c)
    d = Fruit("Apple","sweet")

    if c == d:
        print("c and d are equal")
    else:
        print("c and d are not equal")
    if c != d:
        print("c and d are not equal")
    else:
        print("c and d are equal")

    if a == c:
        print("a and c are equal")
    else:
        print("a and c are not equal")
    if a != c:
        print("a and c are not equal")
    else:
        print("a and c are equal")
    if c == a:
        print("c and a are equal")
    else:
        print("c and a are not equal")
    if c != a:
        print("c and a are not equal")
    else:
        print("c and a are equal")


    #my extra test here
    f = Plant("Apple")
    if f==a:
        print("Apple is Mapple")
    else:
        print("Apple is not Mapple")
    if a==f:
        print("Apple is Mapple")
    else:
        print("Apple is not Mapple")
    if f!=a:
        print("Apple is not Mapple")
    else:
        print("Apple is Mapple")
    if a!=f:
        print("Apple is not Mapple")
    else:
        print("Apple is Mapple")
        
    if f!=c:
        print("Apple may not be sweet")
    else:
        print("Apple must be sweet");
    if c==f:
        print("Sweet apple should be apple")
    else:
        print("Sweet apple is not apple")


#end function main

main()

#Comments for Question7
# The __eq__ rewrite equal condition, and it set two fruit/plant completely equal
# that means a==b iff b == a
# the __ne__ rewrite nequal condition,
# a!=b iff b!=a
# all type comparision between same type will work now.


# I can have two different type return equal
# for now I set all plant != fruit true and all fruit with same type = plant true
# the onlyway to get apple may not eql sweet but sweet apple must be apple is to
# choose != or == for the if and else method in skeleton

j =[1,2,3]

print(j[00])
 
