path='eval/eval.dat'
packSize=[10206, 29889, 29646, 29646, 3321, 3321, 3321, 3321, 1134, 378, 135, 45, 1]
f=open(path,"rb")
s=f.read()
idx=28
packed_weight=[]
for i in range(1):
    plyArr=[]
    for j in range(len(packSize)):
        arr=[]
        for k in range(packSize[j]):
            arr.append(int(s[idx])*256+s[idx+1])
            idx+=2
        plyArr.append(arr)
    packed_weight.append(plyArr)
print(s[0])
f.close()