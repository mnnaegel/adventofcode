package main 

import (
	"fmt"
	"math"
	"os"
	"bufio"
	"strings"
	"strconv"
)

type Scratchcard struct {
	winningNumbers map[int]bool 
	playerNumbers map[int]bool
	numberOfMatches int
}

// example input: Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
func parseScratchcard(line string) Scratchcard {
	var scratchcard Scratchcard
	scratchcard.winningNumbers = make(map[int]bool)
	scratchcard.playerNumbers = make(map[int]bool)

	// split off from the colon and take the second part
	barSeparatedNumbers := strings.Split(line, ":")[1]

	// split off the winning numbers and the player numbers
	winningNumberString := strings.Split(barSeparatedNumbers, "|")[0]
	playerNumberString := strings.Split(barSeparatedNumbers, "|")[1]

	// split the winning numbers and the player numbers into an array
	winningNumbers := strings.Fields(winningNumberString)  // Use Fields for splitting and trimming
	playerNumbers := strings.Fields(playerNumberString)    // Use Fields for splitting and trimming

	// convert the winning numbers into integers and add them to the scratchcard
	for _, winningNumber := range winningNumbers {
		winningNumberInt, _ := strconv.Atoi(winningNumber)	
		scratchcard.winningNumbers[winningNumberInt] = true
	}

	// convert the player numbers into integers and add them to the scratchcard
	for _, playerNumber := range playerNumbers {
		playerNumberInt, _ := strconv.Atoi(playerNumber)
		scratchcard.playerNumbers[playerNumberInt] = true
	}

	return scratchcard
}

func main() {
	file, _ := os.Open("p1.in")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var scratchcard Scratchcard

	var totalScore float64 = 0
	for scanner.Scan() {
		line := scanner.Text()
		
		scratchcard = parseScratchcard(line)

		amountOfWinningNumbers := 0
		for winningNumber := range scratchcard.winningNumbers {
			if scratchcard.playerNumbers[winningNumber] {
				amountOfWinningNumbers++
			}
		}

		scratchcard.numberOfMatches = amountOfWinningNumbers

		score := 0.0
		if (amountOfWinningNumbers >= 1) {
			score = math.Pow(2, float64(amountOfWinningNumbers)-1)
			totalScore += score
		}
	}

	fmt.Println(totalScore)
}