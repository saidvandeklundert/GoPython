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
memory usage is 17.01 MB         Go func took 0.000535965 seconds        Go func called 0 times
memory usage is 22.69 MB         Go func took 0.0 seconds        Go func called 10000 times
memory usage is 23.37 MB         Go func took 0.0 seconds        Go func called 20000 times
memory usage is 23.24 MB         Go func took 0.0 seconds        Go func called 30000 times
memory usage is 23.42 MB         Go func took 0.0 seconds        Go func called 40000 times
memory usage is 23.55 MB         Go func took 0.0 seconds        Go func called 50000 times
memory usage is 23.21 MB         Go func took 0.0 seconds        Go func called 60000 times
memory usage is 23.55 MB         Go func took 0.0 seconds        Go func called 70000 times
memory usage is 23.88 MB         Go func took 0.0 seconds        Go func called 80000 times
memory usage is 23.69 MB         Go func took 0.0 seconds        Go func called 90000 times
memory usage is 23.62 MB         Go func took 0.0 seconds        Go func called 100000 times
```