import re
from string import *



test = "dog x = 3  y < 3.4, 3...4 3.4."
print test
test = test.replace(" ", "")

print(test)
re = re.compile("[x,y][=,>,<]\d*\.?\d+")
results = re.findall(test)  #[0-9]*[.,]?\d*$[-+]
 
print results
