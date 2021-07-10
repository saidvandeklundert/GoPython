import ctypes
import time
import os
import psutil
import json


class PyGo(ctypes.Structure):
    """Generates a struct that is passed into C to be used in Go."""

    _fields_ = [
        ("py2go", ctypes.c_char_p),
        ("go2py", ctypes.c_char_p),
    ]

    def __del__(self):
        """destructor method, calledwhen all references of the object are deleted,
        this method calls a Go func that will free the C memory on the Go side."""
        gcPyGo(self)


# import the Go library:
lib = ctypes.CDLL("./gopy.so")
goPing = lib.goPing
goPing.argtypes = [ctypes.c_char_p]
goPing.restype = PyGo
gcPyGo = lib.gcPyGo
gcPyGo.argtypes = [PyGo]


## Example information that will be send to Go:
with open("hosts.txt") as f:
    host_list = [line.rstrip() for line in f]
# uncomment to define target hosts inline:
# host_list = ["1.1.1.1", "google.nl", "8.8.8.8", "8.8.4.4"]
args_d = {
    "hosts": host_list,
    "log": True,
}
goArgs = json.dumps(args_d).encode("utf8")


def runGoPing():
    """Call GoDoStuff and have the Go runtime print the arguments to screen"""
    PyGo_data = goPing(goArgs)
    py2go_str = PyGo_data.py2go.decode()
    go2py_json = json.loads(PyGo_data.go2py.decode())
    print(f"send py2go\t: {py2go_str}\nreceived go2py\t: {go2py_json}\n\n------------")


if __name__ == "__main__":
    start = time.time()
    runGoPing()
    end = time.time()
    mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

    print(
        f"memory usage: {round(mem_usage,2)} MB\t Go func took {round(end - start, 10)} seconds"
    )
