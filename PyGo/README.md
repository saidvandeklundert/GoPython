Ensure Python 3 and Go are installed.

Compile the Go using the following:
```
go build -buildmode=c-shared -o gopy.so gopy.go
```

Run it:
```
python gopy.py
Message from the Go runtime:     
&{print 100 1.2 [a b c] map[a:a]}

-----------
send py2go      : {"str": "print", "int": 100, "float": 1.2, "mapping": {"a": "a"}, "slice": ["a", "b", "c"]}
received go2py  : {'str': 'Hello from the Go universe', 'int': 0, 'float': 0, 'slice': None, 'mapping': None}

------------
memory usage is 16.93    go func took 0.00051    n is 0
memory usage is 22.74    go func took 0.0        n is 10000
memory usage is 23.21    go func took 0.0        n is 20000
memory usage is 23.24    go func took 0.0        n is 30000
memory usage is 23.21    go func took 0.0        n is 40000
memory usage is 23.05    go func took 0.0        n is 50000
```