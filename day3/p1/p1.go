package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	// "strings"
)

type EngineNumber struct {
	rowIdx int
	leftColumnIndex int
	rightColumnIndex int
	schematicNumber int
	isAdjacentToSymbol bool
}

func isDigit(s string) bool {
	// Regular expression for natural numbers
	re := regexp.MustCompile(`^[0-9]$`)
	return re.MatchString(s)
}

func isSymbol(s string) bool {
	// Regular expression for symbols (*+$!@#%^& etc except for period)
	re := regexp.MustCompile(`^[^0-9a-zA-Z\s\.]$`)
	return re.MatchString(s)
}

func isValidIndex(i int, j int, schematicLines []string) bool {
	return i >= 0 && i < len(schematicLines) && j >= 0 && j < len(schematicLines[i])
}

func main () {
	// get input from p1.in
	file, _ := os.Open("p1.in")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	
	schematicLines := make([]string, 0)

	// process each line of input from file
	for scanner.Scan() {
		schematicLines = append(schematicLines, scanner.Text())
	}

	// get list of engine numbers
	engineNumbers := make([]EngineNumber, 0)
	for i, line := range schematicLines {
		number := ""
		for j, char := range line {
			if isDigit(string(char)) {
				number += string(char)
			}

			if !isDigit(string(char)) || j == len(line) - 1 {
				if number != "" {
					numberInt, _ := strconv.Atoi(number)

					var newEngineNumber EngineNumber
					if !isDigit(string(char)) {
						newEngineNumber = EngineNumber{i, j - len(number), j-1, numberInt, false}
					} else {
						newEngineNumber = EngineNumber{i, j - len(number) + 1, j, numberInt, false}
					}
					number = ""
					
					// check if engine number is adjacent to symbol
					// to the left or to the right of the engine number
					if isValidIndex(i, newEngineNumber.leftColumnIndex-1, schematicLines) && isSymbol(string(schematicLines[i][newEngineNumber.leftColumnIndex-1])) {
						newEngineNumber.isAdjacentToSymbol = true
					} else if isValidIndex(i, newEngineNumber.rightColumnIndex+1, schematicLines) && isSymbol(string(schematicLines[i][newEngineNumber.rightColumnIndex+1])) {
						newEngineNumber.isAdjacentToSymbol = true
					}

					// above or below the engine number
					for k := newEngineNumber.leftColumnIndex-1; k <= newEngineNumber.rightColumnIndex+1; k++ {
						if isValidIndex(i-1, k, schematicLines) && isSymbol(string(schematicLines[i-1][k])) {
							newEngineNumber.isAdjacentToSymbol = true
						} else if isValidIndex(i+1, k, schematicLines) && isSymbol(string(schematicLines[i+1][k])) {
							newEngineNumber.isAdjacentToSymbol = true
						}
					}

					engineNumbers = append(engineNumbers, newEngineNumber)
				}
			}
		}
	}

	total := 0
	for _, engineNumber := range engineNumbers {
		if engineNumber.isAdjacentToSymbol {
			total += engineNumber.schematicNumber
		}
	}
	fmt.Println(total)
}