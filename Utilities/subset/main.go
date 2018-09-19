// Takes the first N lines of the CSV file and creates a new,
// smaller subset.
package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
)

// Flags for --file --output to the command line utility.
// The order of initialization is undefined, so both long and short flags
// must be set up with an init function.
var inFilename string
var outFilename string
var numLines int

func init() {
	const (
		defaultLines   = 20
		defaultInFile  = `default.csv`
		defaultOutFile = `subset.csv`
		usageFile      = "Filename to transform"
		usageOutput    = "Filename to save transform"
	)
	flag.StringVar(&inFilename, "file", defaultInFile, usageFile)
	flag.StringVar(&inFilename, "f", defaultInFile, usageFile+" (shorthand)")
	flag.StringVar(&outFilename, "out", defaultOutFile, usageOutput)
	flag.StringVar(&outFilename, "o", defaultOutFile, usageOutput+" (shorthand)")
	flag.IntVar(&numLines, "number", defaultLines, "number of line for subset")
	flag.IntVar(&numLines, "n", defaultLines, "number of lines for subset"+" (shorthand)")
}

func main() {
	flag.Parse()

	path := inFilename
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Opened: %s\n", path)

	newFile, err := os.Create(outFilename)
	if err != nil {
		panic(err)
	}
	defer newFile.Close()
	fmt.Printf("Created: %s\n", outFilename)

	scanner := bufio.NewScanner(f)
	lines := 0
	for scanner.Scan() {
		lines++
		line := scanner.Text()
		line += string('\n')
		_, err := newFile.WriteString(line)
		if err != nil {
			panic(err)
		}

		if lines%10000 == 0 {
			fmt.Println("Parsed line:", lines)
		}
		if lines > numLines {
			break
		}
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}

}
