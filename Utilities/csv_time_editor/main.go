// csv_time_editor parses a csv file of AIS entries and allows
// manipulation of the timestamp for the transmission
package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
	"unicode"

	"github.com/FATHOM5/Seattle_Track_2/Utilities/csvAIS"
)

// Start time
const timeFormat = "1/2/2006 03:04:05"
const startDate = "12/3/2017"
const startTime = "09:00:00"

// Flags for filename to modify.
// The order of initialization is undefined, so they must be set up
// with an init function.
var inFile string
var outFile string

func init() {
	const (
		defaultFile = "default.csv"
		usage       = "Input .csv file of AIS rows."
	)
	flag.StringVar(&inFile, "file", defaultFile, usage)
	flag.StringVar(&inFile, "f", defaultFile, usage+" (shorthand)")
	flag.StringVar(&outFile, "out", defaultFile, "Output .csv file")
	flag.StringVar(&outFile, "o", defaultFile, "Output .csv file (shorthand)")
}

func main() {
	// parse flags
	flag.Parse()

	// Open the target csv file and create a scanner
	in, err := os.OpenFile(inFile, os.O_RDONLY, 0666)
	if err != nil {
		panic(err)
	}
	defer in.Close()
	scanner := bufio.NewScanner(in)
	firstLine := oneLine(scanner)

	// Open the output file
	out, err := os.Create(outFile)
	if err != nil {
		panic(err)
	}
	defer out.Close()
	out.WriteString(fmt.Sprintln(firstLine))

	// Set up a base time variable and increment it as scanning
	// goes forward
	combinedStart := startDate + " " + startTime
	start, err := time.Parse(timeFormat, combinedStart)
	if err != nil {
		fmt.Println("unable to parse start string:", startTime)
		os.Exit(1)
	}
	fmt.Println("Starting with base time:", start)

	// Identify the necessary index values
	ti, ok := headerIndex("BaseDateTime", firstLine)
	if !ok {
		panic("cannot find header BaseDateTime")
	}
	fmt.Println("Found BaseDateTime header at index:", ti)

	mi, ok := headerIndex("MMSI", firstLine)
	if !ok {
		panic("cannot find header MMSI")
	}
	fmt.Println("Found MMSI header at index:", mi)

	// Create the CumulativeClock
	var cc CumulativeClock
	cc.Set(start)
	fmt.Println("New cc started at:", cc.Now())

	// if ok := cc.IncrementString("1m"); !ok {
	// 	panic("IncrementString not ok")
	// }
	// fmt.Println("After 1m advance cc at:", cc.Now())
	// if ok := cc.IncrementString("2m15s"); !ok {
	// 	panic("IncrementString not ok")
	// }
	// fmt.Println("After 2m15s advance cc at:", cc.Now())
	// cc.Reset()
	// fmt.Println("After Reset cc at:", cc.Now())

	// Walk through the file one line at a time
	mmsiSet := make(map[string]bool)
	for scanner.Scan() { // already points at the first data line
		line := scanner.Text()
		records := strings.Split(line, ",")
		mmsi := records[mi]
		t := records[ti]
		if _, ok := mmsiSet[mmsi]; !ok {
			// reset the clock the first time a mmsi is seen
			mmsiSet[mmsi] = true
			cc.Reset()
		}
		err := processTime(t, &cc)
		if err != nil {
			panic(err)
		}

		// Create the new line of transoformed data
		records[ti] = cc.Now().String()
		newLine := strings.Join(records, ",")

		//write the line
		out.WriteString(fmt.Sprintln(newLine))
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	fmt.Println("mmsiSet contains:", mmsiSet)

}

// processTime takes the string value of a time duration in seconds
// from the caller and returns a formatted time from the cumulative
// clock.
func processTime(t string, cc *CumulativeClock) error {
	t += "s"
	if err := cc.IncrementBySecReading(t); err != nil {
		return fmt.Errorf("unable to parse time from %s", t)
	}
	fmt.Printf("increment: %s\tprocessTime cc.Now:%s\n", t, cc.Now())
	return nil
}

func oneLine(scanner *bufio.Scanner) string {
	if ok := scanner.Scan(); !ok {
		err := scanner.Err()
		if err != nil {
			panic(err)
		}
	}
	return scanner.Text()
}

// use with int, ok := ... idiom
func headerIndex(targetHeader string, firstLine string) (int, bool) {
	h := csvAIS.NewHeaders(firstLine)
	for i, header := range h {
		if header == targetHeader {
			return i, true
		}
	}
	return 0, false
}

// CumulativeClock takes a start time and keeps track of increments
// through its methods.
type CumulativeClock struct {
	start           time.Time
	current         time.Time
	lastIncrement   string
	incrementedOnce bool
}

// Set the clock at initialization
func (c *CumulativeClock) Set(t time.Time) {
	c.start = t
	c.current = c.start
	c.incrementedOnce = false
	c.lastIncrement = ""
}

// Now returns the c.current
func (c *CumulativeClock) Now() time.Time {
	return c.current
}

// IncrementString advances the current time of the clock by the
// incrment passed as a string.  Increment should be in the format
// compatible with time.ParseDuration(s string)(Duration, error).
// Usage should be with the ok := c.IncrementString idiom
func (c *CumulativeClock) IncrementString(dtString string) bool {
	dt, err := time.ParseDuration(dtString)
	if err != nil {
		return false
	}
	c.current = c.current.Add(dt)
	c.incrementedOnce = true

	return true
}

// IncrementDuration moves the current time of the cumulative clock
// forward.
func (c *CumulativeClock) IncrementDuration(d time.Duration) {
	c.current = c.current.Add(d)
	if !c.incrementedOnce {
		c.incrementedOnce = true
	}
}

// IncrementBySecReading advances the current time of the clock by the
// incrment passed as a string.  Increment should be in the format
// compatible with time.ParseDuration(s string)(Duration, error).
// This takes the unusual circumstance where the target seconds column
// is known and passed in, but the duration must be calculated.
// Passes errors from subordinate functions back to the caller
func (c *CumulativeClock) IncrementBySecReading(dtString string) error {
	const hhssTime = "03:04"
	const date = "12/1/2017"

	if c.incrementedOnce {
		var minuteRolled = false
		// fmt.Println("CumlativeClock.IncrementBySecReading: follow-on increment")

		// Compare the current dtString to the lastIncrement
		// If dt < lastDt then a minute has rolled
		lastDt, _ := time.ParseDuration(c.lastIncrement)
		dt, _ := time.ParseDuration(dtString)
		if dt < lastDt {
			// fmt.Println("CumlativeClock.IncrementBySecReading: minute rolled")
			minuteRolled = true
		}

		d := time.Minute
		trunc := c.Now().Truncate(d)
		var s []rune
		for _, r := range dtString {
			if unicode.IsDigit(r) {
				s = append(s, r)
			}
		}
		secondsString := string(s)
		secondsInt, err := strconv.ParseInt(secondsString, 10, 64)
		if err != nil {
			return (err)
		}

		if minuteRolled {
			// Add a minute plus the seconds
			sec := time.Second * time.Duration(60+secondsInt)
			c.current = trunc.Add(sec)
		} else {
			// else (old hh:mm):(new ss)
			sec := time.Second * time.Duration(secondsInt)
			c.current = trunc.Add(sec)
		}
		c.lastIncrement = dtString

	} else {
		// fmt.Println("CumlativeClock.IncrementBySecReading: first increment")
		c.IncrementString(dtString)
		c.incrementedOnce = true
		c.lastIncrement = dtString
	}
	return nil
}

// Reset the clock to the start time and all other params to baseline
func (c *CumulativeClock) Reset() {
	c.Set(c.start)
}
