class Person:
    def __init__(self, name, last_name):
        self.name = name
        self.__lastname = last_name

    def fullname(self):
        full_name = "{} {}".format(self.name,self.__lastname)
        return full_name
    def he_said(self):
        return self.__lastname

# Outside class
anh_toi = Person('Trung', 'Nguyen')
print(anh_toi.name)
print(anh_toi.fullname())
print(anh_toi.he_said())
print(anh_toi.__lastname)

class Person:
    def __init__(self, name, last_name):
        self.name = name
        self.__lastname = last_name

    def __love(self, gf_name):
        return "{} love {}".format(self.name, gf_name)
    def said_love(self):
        return self.__love("Phuong")

# Outside class
anh_toi = Person('Trung', 'Nguyen')
print(anh_toi.name)
print(anh_toi.said_love())
print(anh_toi.__love)


