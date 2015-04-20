import re


test = "dog 3  y < 3.4 3...4 3.4."

results = re.findall(r"[x,y][=,>,<][-+]?[0-9]*\.?[0-9]+", test)  #[0-9]*[.,]?\d*$
 
print results
