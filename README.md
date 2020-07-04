# Pegasus-Language

To compile do:

```
python main.py main.p
```

Variables
```
var x = 5;
var array = ["Hello", "World"];
```

Printing
```
print "Hello World!";
print var:x;
print arr:array[0];
```

Input
```
var x = input();
print var:x;
```

If Else Statements
```
var x = 5;
var myArray = ["x is 5", "x is not 5"];

if x == 5: print arr:myArray[0];
else: print arr:myArray[1];
```

Math
```
var x = Math(1 + 2);

print var:x;
```

Incriment
```
var x = 5;
x = inc(x);
print var:x;
```

Functions
```
function myFunction(): print "Hello World";

myFunction();
```

For Loops
```
for x in range 0, 2: print "hello";
for y in range 0, 3: print var:y;
```

Imports
```
import "secondFile.p";

// Function in secondFile.p
myFunction()

// Variable in secondFile.p
print var:x;
```
