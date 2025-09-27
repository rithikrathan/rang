ucf = {1,3,4,5,7,8,10,14}
uct = {2,6,9,11,12,13,15,16}
lct = {10,12,14,16}
lcf = {1,2,3,4,5,6,7,8,9,11,13,15}

print("isolated from both",ucf&lcf)
print("false,tru",ucf&lct)
print("true,false",uct&lcf)
print("connected to both",uct&lct)
