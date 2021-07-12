## Calling Go from Python

On the Go-side, when we compile we use `go build -buildmode=c-shared -o <c-lib>.so <go-package>`. This will create 2 files:
- a shared object binary file (.so) exposing Go functions as a C-style APIs
- a C header file, defines C types mapped to Go compatible types


On the Python side, we make use of [ctypes](https://docs.python.org/3/library/ctypes.html) to call functions we exported from Go and to pass Ctypes to CGo.

## Useful resources

### books

[Learning Go by Jon Bodner](https://www.oreilly.com/library/view/learning-go/9781492077206/) \
[CPython Internals](https://realpython.com/products/cpython-internals-book/)

### blogs and articles

https://fluhus.github.io/snopher/ \
https://www.ardanlabs.com/blog/2020/06/python-go-grpc.html \
https://www.ardanlabs.com/blog/2020/07/extending-python-with-go.html \
https://www.ardanlabs.com/blog/2020/08/packaging-python-code.html \
https://www.ardanlabs.com/blog/2020/09/using-python-memory.html \
https://blog.golang.org/cgo \
https://pythonextensionpatterns.readthedocs.io/en/latest/ \
https://github.com/jima80525/ctypes_example \ 