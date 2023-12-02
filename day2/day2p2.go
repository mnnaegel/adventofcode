package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Game struct {
	id int 
	sets []Set
}

type Set struct {
	redCount int
	blueCount int
	greenCount int
}

// ex input: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
func createGame(line string) Game {
	parts := strings.SplitN(line, ":", 2)

	// Parse the game ID
	id, _ := strconv.Atoi(strings.Split(parts[0], " ")[1])
	
	sets := make([]Set, 0)
	// Parse the sets
	setParts := strings.Split(parts[1], ";")
	for _, setPart := range setParts {
		set := Set{}
		colors := strings.Split(setPart, ",")
		for _, color := range colors {
			color = strings.TrimSpace(color)
			colorParts := strings.Split(color, " ")
			count, _ := strconv.Atoi(colorParts[0])
			switch colorParts[1] {
			case "red":
				set.redCount = count
			case "blue":
				set.blueCount = count
			case "green":
				set.greenCount = count
			}
		}
		sets = append(sets, set)
	}

	return Game{id, sets}
}

func main() {
	filepath := "p1.in"
	file, _ := os.Open(filepath)
	
	defer file.Close()

	scanner := bufio.NewScanner(file)

	powerSum := 0
	for scanner.Scan() {
		line := scanner.Text()
		game := createGame(line)
		maxRed := 0
		maxBlue := 0
		maxGreen := 0

		for _, set := range game.sets {
			if set.redCount > maxRed {
				maxRed = set.redCount
			}
			if set.blueCount > maxBlue {
				maxBlue = set.blueCount
			}
			if set.greenCount > maxGreen {
				maxGreen = set.greenCount
			}
		}

		powerSum += maxRed*maxBlue*maxGreen
	}
	fmt.Println("Total: ", powerSum)
}