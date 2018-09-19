// Takes the first N lines of the CSV file and creates a new,
// smaller subset.
package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

const dataRoot = `../../Data`

// Flag for --file --output to the command line utility.
// The order of initialization is undefined, so both long and short flags
// must be set up with an init function.
var inFilename string
var outFilename string
var numLines int

func init() {
	const (
		defaultLines = 20
		defaultInFile = `AIS_LA_SD_Jan_1_to_15_2016_Filtered_by_Proximity.csv`
		defaultOutFile = `Subset_Carib_Jan_17_Pairs.csv`
		usageFile      = "Filename to transform"
		usageOutput    = "Filename to save transform"
	)
	flag.StringVar(&inFilename, "file", defaultInFile, usageFile)
	flag.StringVar(&inFilename, "f", defaultInFile, usageFile+" (shorthand)")
	flag.StringVar(&outFilename, "out", defaultOutFile, usageOutput)
	flag.StringVar(&outFilename, "o", defaultOutFile, usageOutput+" (shorthand)")
	flag.IntVar(&numLines, "number", defaultLines, usageFile)
	flag.IntVar(&numLines, "n", defaultLines, usageFile+" (shorthand)")
}

func main() {
	// Implemented flag is [-f]
	flag.Parse()

	path := filepath.Join(dataRoot, inFilename)
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Opened: %s\n", path)

	newFile, err := os.Create(filepath.Join(dataRoot, outFilename))
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
