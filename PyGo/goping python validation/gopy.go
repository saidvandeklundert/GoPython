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
	"time"
	"unsafe"

	"github.com/go-ping/ping"
)

type PyGo struct {
	Message string   `json:"message,omitempty"`
	Hosts   []string `json:"hosts,omitempty"`
	Log     bool     `json:"log,omitempty"`
}

type GoPy struct {
	Message string `json:"message,omitempty"`
	PingResults
}

//export goPing
func goPing(py2go_info *C.char) C.struct_PyGo {
	// unmarshall JSON received from Python':
	s := C.GoString(py2go_info)
	Py2GoArgs := new(PyGo)
	err := json.Unmarshal([]byte(s), &Py2GoArgs)
	if err != nil {
		log.Fatal("Cannot unmarshall JSON received from the Python universe")

	}
	if Py2GoArgs.Log == false {
		log.SetOutput(ioutil.Discard)
	}
	log.Printf("Message from the Go runtime:\n%v\n\n-----------\n", Py2GoArgs)
	// Prepare JSON that is going to be returned:

	Go2Py := new(GoPy)
	Go2Py.Message = "Go ping results"
	c := make(chan ping.Statistics)

	for _, host := range Py2GoArgs.Hosts {
		go pinger(host, c)
	}

	for i := 0; i < len(Py2GoArgs.Hosts); i++ {
		stats := <-c

		pingresult := PingResult{
			Host:              stats.Addr,
			PacketsSent:       stats.PacketsSent,
			PacketLossPercent: int(stats.PacketLoss),
			Duplicates:        stats.PacketsRecvDuplicates,
		}
		Go2Py.AddPingResult(pingresult)

	}

	log.Println(Go2Py)

	// Place the data in the C struct so we can communicate to the Python universe
	Go2Py_return, _ := json.MarshalIndent(Go2Py, "", "\t")
	Go2Py_returnArgs := string(Go2Py_return)
	var result C.struct_PyGo
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

// Function that sends an ICMP request to target host and writes the stats to a channel
func pinger(host string, c chan ping.Statistics) {
	pinger, _ := ping.NewPinger(host)
	pinger.Count = 2
	pinger.Timeout = time.Second * 2
	pinger.SetPrivileged(true) // Windows requirement
	err := pinger.Run()
	if err != nil {
		log.Printf("Failed to ping target host: %s", err)
	}
	// Returns ping.Statistics struct: https://github.com/go-ping/ping/blob/master/ping.go#L230
	stats := *pinger.Statistics()
	c <- stats
}

func PrintStats(stats ping.Statistics) {
	fmt.Printf("\n%s results: %d packets transmitted, %d packets received, %d duplicates, %v%% packet loss\n", stats.Addr,
		stats.PacketsSent, stats.PacketsRecv, stats.PacketsRecvDuplicates, stats.PacketLoss)
	fmt.Printf("   round-trip min/avg/max/stddev = %v/%v/%v/%v\n\n",
		stats.MinRtt, stats.AvgRtt, stats.MaxRtt, stats.StdDevRtt)
	fmt.Printf("%T", stats)

}

type PingResult struct {
	Host              string `json:"host,omitempty"`
	PacketsSent       int    `json:"packets-sent,omitempty"`
	PacketLossPercent int    `json:"packetloss-percent,omitempty"`
	Duplicates        int    `json:"duplicates,omitempty"`
}

type PingResults struct {
	PingResults []PingResult `json:"ping-results"`
}

// Method to update the PingResults
func (tpr *PingResults) AddPingResult(pr PingResult) {
	tpr.PingResults = append(tpr.PingResults, pr)
}

func main() {
	// To test the Go functions separately
	c := make(chan ping.Statistics)
	tpr := PingResults{}
	sliceOfHosts := []string{"8.8.8.8", "8.8.4.4"}
	for _, host := range sliceOfHosts {
		go pinger(host, c)
	}

	for _, _ = range sliceOfHosts {
		stats := <-c
		//PrintStats(stats)

		pingresult := PingResult{
			Host:              stats.Addr,
			PacketsSent:       stats.PacketsSent,
			PacketLossPercent: int(stats.PacketLoss),
			Duplicates:        stats.PacketsRecvDuplicates,
		}
		tpr.AddPingResult(pingresult)

	}
	fmt.Println(tpr)

}
