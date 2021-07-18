from pydantic import BaseModel
from typing import List
import json

# Data send to Go:
class Py2GoArgs(BaseModel):
    """Script fields to be passed into the Go runtime"""

    hosts: List[str]
    log: bool

    def JsonOut(self) -> bytes:
        """Output the class as bytes containing a utf8 JSON byte"""
        return json.dumps(self.dict()).encode("utf8")


# Data received from Go:
class GoPingResult(BaseModel):
    """Describes a Ping result"""

    host: str
    packets: int
    packetloss: int
    duplicates: int


class GoPingResults(BaseModel):
    """Describes the Go Ping results"""

    message: str
    results: List[GoPingResult]
