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

type Coordinates struct {
	X, Y int
}

type Gear struct {
	rowIdx int
	columnIdx int
	AdjacentEngineNumbers []EngineNumber
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

func addToGear(gears map[Coordinates]Gear, newEngineNumber EngineNumber, i int, j int) {
	fmt.Printf("adding %v to gear at %v %v\n", newEngineNumber, i, j)
	gear := gears[Coordinates{i, j}]

	if gear.AdjacentEngineNumbers == nil {
		gear.AdjacentEngineNumbers = make([]EngineNumber, 0)
	}
	gear.AdjacentEngineNumbers = append(gear.AdjacentEngineNumbers, newEngineNumber)
	gears[Coordinates{i, j}] = gear
}

func main () {
	// get input from p1.in
	file, _ := os.Open("p2.in")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	
	schematicLines := make([]string, 0)

	// process each line of input from file
	for scanner.Scan() {
		schematicLines = append(schematicLines, scanner.Text())
	}

	// hashmap of gears which takes in a row and column index and returns a gear
	gears := make(map[Coordinates]Gear)

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
					if isValidIndex(i, newEngineNumber.leftColumnIndex-1, schematicLines) && string(schematicLines[i][newEngineNumber.leftColumnIndex-1]) == "*" {
						addToGear(gears, newEngineNumber, i, newEngineNumber.leftColumnIndex-1)
					} else if isValidIndex(i, newEngineNumber.rightColumnIndex+1, schematicLines) && string(schematicLines[i][newEngineNumber.rightColumnIndex+1]) == "*" {
						addToGear(gears, newEngineNumber, i, newEngineNumber.rightColumnIndex+1)
					}

					// above or below the engine number
					for k := newEngineNumber.leftColumnIndex-1; k <= newEngineNumber.rightColumnIndex+1; k++ {
						if isValidIndex(i-1, k, schematicLines) && string(schematicLines[i-1][k]) == "*" {
							addToGear(gears, newEngineNumber, i-1, k)
						} else if isValidIndex(i+1, k, schematicLines) && string(schematicLines[i+1][k]) == "*" {
							addToGear(gears, newEngineNumber, i+1, k)
						}
					}
				}
			}
		}
	}

	total := 0
	for _,j := range gears {
		if len(j.AdjacentEngineNumbers) == 2 {
			total += j.AdjacentEngineNumbers[0].schematicNumber * j.AdjacentEngineNumbers[1].schematicNumber
		}
	}
	fmt.Println(total)
}