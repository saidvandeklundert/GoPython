from goping import runGoPing
from models.models import Py2GoArgs
import time
from sys import argv
import psutil
import os
from sys import argv
from sys import path

py2goargs = Py2GoArgs(
    hosts=["1.1.1.1", "google.nl", "8.8.8.8", "8.8.4.4", "5.5.5.5"], log=False
)


if __name__ == "__main__":
    start = time.time()
    runGoPing(py2goargs=py2goargs, display=True)

    end = time.time()
    mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

    print(
        f"memory usage: {round(mem_usage,2)} MB\t Go func took {round(end - start, 10)} seconds"
    )
    if len(argv) >= 2:
        with open(f"{path[0]}/hosts.txt") as f:
            host_list = [line.rstrip() for line in f]
        py2goargs = Py2GoArgs(hosts=host_list, log=True)
        runGoPing(py2goargs=py2goargs, display=True)