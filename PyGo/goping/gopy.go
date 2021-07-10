package main

/*
#include <stdlib.h>
struct PyGo {
  char* py2go;
  char* go2py;
};
*/
import "C"
import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"sync"
	"unsafe"

	"github.com/go-ping/ping"
)

type PyGo struct {
	Message string   `json:"message,omitempty"`
	Hosts   []string `json:"hosts,omitempty"`
	Log     bool     `json:"log,omitempty"`
}

func pinger(host string, wg *sync.WaitGroup) {
	defer wg.Done()
	pinger, _ := ping.NewPinger(host)
	pinger.Count = 2
	pinger.SetPrivileged(true)
	pinger.OnFinish = func(stats *ping.Statistics) {
		fmt.Printf("\n--- %s ping statistics ---\n", stats.Addr)
		fmt.Printf("%d packets transmitted, %d packets received, %d duplicates, %v%% packet loss\n",
			stats.PacketsSent, stats.PacketsRecv, stats.PacketsRecvDuplicates, stats.PacketLoss)
		fmt.Printf("round-trip min/avg/max/stddev = %v/%v/%v/%v\n",
			stats.MinRtt, stats.AvgRtt, stats.MaxRtt, stats.StdDevRtt)
	}
	fmt.Printf("PING %s (%s):\n", pinger.Addr(), pinger.IPAddr())
	err := pinger.Run()
	if err != nil {
		fmt.Printf("Failed to ping target host: %s", err)
	}
}

//export goPing
func goPing(py2go_info *C.char) C.struct_PyGo {

	// turn JSON into 'args':
	s := C.GoString(py2go_info)
	Py2GoArgs := new(PyGo)
	_ = json.Unmarshal([]byte(s), &Py2GoArgs)

	if Py2GoArgs.Log == false {
		log.SetOutput(ioutil.Discard)
	}
	log.Printf("Message from the Go runtime:\n%v\n\n-----------\n", Py2GoArgs)
	// Prepare JSON that is going to be returned:
	var result C.struct_PyGo
	Go2Py := new(PyGo)
	Go2Py.Message = "Hello from the Go universe"
	var wg sync.WaitGroup
	wg.Add(len(Py2GoArgs.Hosts))
	for _, host := range Py2GoArgs.Hosts {
		log.Printf(host)
		go pinger(host, &wg)

	}
	wg.Wait()
	// Place the data in the C struct so we can communicate to the Python universe
	Go2Py_return, _ := json.MarshalIndent(Go2Py, "", "\t")
	Go2Py_returnArgs := string(Go2Py_return)
	result.py2go = C.CString(s)
	result.go2py = C.CString(Go2Py_returnArgs)

	return result
}

//export gcPyGo
func gcPyGo(py2go_info C.struct_PyGo) {
	/*
		This function will garbage collect the struct that was used
		 to facilitate communications between Python and Go.
	*/
	C.free(unsafe.Pointer(py2go_info.py2go))
	C.free(unsafe.Pointer(py2go_info.go2py))
}

func main() {}
