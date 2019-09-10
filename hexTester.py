q = -1 #Change this value to simulate the speed and direction
x = q & 0x7F
print(x)
if q & 0x80:
    print("direct 0")
else:
    print("direct 1")
    

