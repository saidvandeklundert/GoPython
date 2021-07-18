import ctypes
import json
from models.models import Py2GoArgs, GoPingResults
from sys import path


class PyGo(ctypes.Structure):
    """Generates a struct that is passed into C to be used in (C)Go."""

    _fields_ = [
        ("py2go", ctypes.c_char_p),
        ("go2py", ctypes.c_char_p),
    ]

    def GetGoResponse(self):
        go2py_data = self.go2py.decode()
        return json.loads(go2py_data)

    def __del__(self):
        """destructor method, calledwhen all references of the object are deleted,
        this method calls a Go func that will free the C memory on the Go side."""
        gcPyGo(self)


lib = ctypes.CDLL(f"{path[0]}/gopy.so")
goPing = lib.goPing
goPing.argtypes = [ctypes.c_char_p]
goPing.restype = PyGo
gcPyGo = lib.gcPyGo
gcPyGo.argtypes = [PyGo]


def runGoPing(
    py2goargs: Py2GoArgs,
    display: bool = False,
):
    """Call runGoPing"""
    PyGo_data = goPing(py2goargs.JsonOut())
    go2py_response = PyGo_data.GetGoResponse()
    results = GoPingResults(**go2py_response)
    alives = []
    if display:
        for gopingresult in results.results:
            if gopingresult.packetloss > 0:
                print(f"Packet loss detected for host: {gopingresult.host}")
            elif gopingresult.packetloss == 0:
                alives.append(gopingresult.host)
        print(f"Number of hosts with 0% packet loss: {len(alives)}")


if __name__ == "__main__":

    import time

    import psutil
    import os

    py2goargs = Py2GoArgs(
        hosts=["1.1.1.1", "google.nl", "8.8.8.8", "8.8.4.4", "5.5.5.5"], log=False
    )
    runGoPing(py2goargs=py2goargs, display=True)
    # running it a long time to see if there are memory leaks

    with open("hosts.txt") as f:
        host_list = [line.rstrip() for line in f]
    py2goargs = Py2GoArgs(hosts=host_list, log=True)
    n = 0
    while True:
        start = time.time()
        runGoPing(py2goargs=py2goargs, display=False)
        end = time.time()
        mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        print(
            f"memory usage is {round(mem_usage,2)} MB\t Go func took {round(end - start, 10)} seconds\t Go func called {n} times"
        )
        n = n + 1