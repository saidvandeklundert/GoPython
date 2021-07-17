import ctypes
import time
import os
import psutil
import json
from pydantic import BaseModel
from typing import Any, List, Optional

# Args from Python to Go:
class Py2GoArgs(BaseModel):
    """Script fields to be passed into the Go runtime"""

    hosts: List[str]
    log: bool

    def JsonOut(self) -> bytes:
        """Output the class as bytes containing a utf8 JSON byte"""
        return json.dumps(self.dict()).encode("utf8")


# Args from Go to Python:
class GoPingRestult(BaseModel):
    """Describes a Ping result"""

    host: str
    packets_sent: int
    packet_los_percent: int
    duplicated: int


class GoPingResults(BaseModel):
    """Describes the Go Ping results"""

    pingResults: List[GoPingRestult]


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


def ReturnFunction(
    lib: ctypes.CDLL,
    function_name: str,
    response_type: Any,
    argument_type: Optional[Any] = None,
):
    """Provide easy access to Ctypes functions"""
    func = lib.__getattr__(function_name)
    func.restype = response_type
    if argument_type:
        func.argtypes = argument_type
    return func


goPing = ReturnFunction(
    lib=ctypes.CDLL("./gopy.so"),
    function_name="goPing",
    response_type=PyGo,
    argument_type=[ctypes.c_char_p],
)
gcPyGo = ReturnFunction(
    lib=ctypes.CDLL("./gopy.so"),
    function_name="gcPyGo",
    response_type=PyGo,
)


# to spice it up
with open("hosts.txt") as f:
    host_list = [line.rstrip() for line in f]

py2goargs = Py2GoArgs(hosts=host_list, log=True)
"""
py2goargs = Py2GoArgs(hosts=["1.1.1.1", "google.nl", "8.8.8.8", "8.8.4.4"], log=False)
"""


def runGoPing(
    py2goargs: Py2GoArgs,
    display: bool = True,
):
    """Call runGoPing"""
    PyGo_data = goPing(py2goargs.JsonOut())
    py2go_str = PyGo_data.py2go.decode()
    go2py_response = PyGo_data.GetGoResponse()

    if display:
        print(
            f"send py2go\t: {py2go_str}\nreceived go2py\t: {go2py_response}\n\n------------"
        )


if __name__ == "__main__":
    start = time.time()
    runGoPing(py2goargs=py2goargs)
    end = time.time()
    mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

    print(
        f"memory usage: {round(mem_usage,2)} MB\t Go func took {round(end - start, 10)} seconds"
    )
    # running it a long time to see if there are memory leaks
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
