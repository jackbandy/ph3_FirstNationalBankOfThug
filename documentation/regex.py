import re


test = "dog x = 3  y < 3.4, 3...4 3.4."
test.replace(' ', '')
results = re.findall("x[=,>,<]\d*\.?\d+", test)  #[0-9]*[.,]?\d*$[-+]
 
print results
