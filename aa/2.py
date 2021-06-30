testlist = [1, "哈哈", "123"]
print(testlist[0])
print(testlist[1])
print(testlist[2])

for i in range(5):
    print("%d__%d" % (i, 11))

for i in testlist:
    print(i)


def sum(a, b):

    c = a + b
    return c
