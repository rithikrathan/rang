bct = {2,6,9,11,12,13,15,16}
bcf = {1,3,4,5,7,7,18,14}
rct = {5,8,9,10,12,14,15,16}
rcf = {1,2,3,4,6,7,11,13}

print("isolated from both",bcf&rcf)
print("isolated from top and conn left",bcf&rct)
print("isolated from left and conn top",bct&rcf)
print("connected to both",bct&rct)
