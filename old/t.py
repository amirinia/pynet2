
l1 = [1,2,2,3]

if (len(l1) != len(set(l1))):
    l3 = set([x for x in l1 if l1.count(x) > 1])
    print(l3)