// Takes the first N lines of the CSV file and creates a new,
// smaller subset.
package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
)

var totalLines = 20

const dataRoot = `../../Data`
const csvFilename = `AIS_LA_SD_Jan_1_to_15_2016_Filtered_by_Proximity.csv`
const csvSubset = `Subset_Carib_Jan_17_Pairs.csv`

func main() {
	path := filepath.Join(dataRoot, csvFilename)
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Opened: %s\n", path)

	newFile, err := os.Create(filepath.Join(dataRoot, csvSubset))
	if err != nil {
		panic(err)
	}
	defer newFile.Close()
	fmt.Printf("Created: %s\n", csvSubset)

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
		if lines > totalLines {
			break
		}
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}

}
