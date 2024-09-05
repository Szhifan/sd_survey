path = "pre_test.txt"

f = open(path,"r")
for i in f.readlines():
    print(i.split("\b"))