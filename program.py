import math

def main():
    generatePuzzle(1)
    generatePuzzle(2)
    generatePuzzle(3)
    generatePuzzle(4)
    generatePuzzle(5)
    generatePuzzle(6)

# generates and returns a number based on choice and nth number
def generatorEquations(choice, n):
    num = 0
    if choice == 1:
        num = 1 + (math.floor(n * 40 * math.pi**2) % 9)
    elif choice == 2:
        num = 1 + (math.floor(n * 50 * math.e**2) % 9)
    elif choice == 3:
        num = 1 + (math.floor(n * 40 * math.e**3) % 9)
    elif choice == 4:
        num = 1 + (math.floor(n * 50 * math.e**3) % 9)
    elif choice == 5:
        num = 1 + (math.floor(n * 40 * math.e**2) % 9)
    elif choice == 6:
        num = 1 + (math.floor(n * 60 * math.e**3) % 9)
    
    return num


def generatePuzzle(choice):
    n = 1
    count = 0
    numbersList = []
    rawNumbersList = []
    unusedNumber = []

    # generate numbers for puzzle depending on choice
    while count < 27:
        x = generatorEquations(choice, n)
        if numbersList.count(x) < 3:
            numbersList.append(x)
            rawNumbersList.append(x)
            count += 1
        else:
            unusedNumber = [x]
            rawNumbersList.append(unusedNumber)
        n += 1   
    
    slicesList = getSlices(numbersList)
    print("PUZZLE", choice)
    # numbers inside square brackets[] are skipped 
    print("raw numbers list:", str(rawNumbersList)[1:-1])
    print("")
    solvePuzzle(slicesList, True, False)
    print("_______________________________________________")

# converts list of generated numbers in to a list of slices
def getSlices(numList):     
    a = 0
    b = 3
    sliceList = []
    for x in range(9):
        sliceList.append(numList[a:b])
        a = a + 3
        b = b + 3
    return sliceList

# checks if new slice is not an obstacle with the current slices
def isValidSlice(currentSlices, newSlice):
    nums = []
    
    # return true if currentSlices is empty
    if not currentSlices:
        return True
    
    for n in range(3):
        for slice in currentSlices:
            if newSlice[n] == slice[n]:
                return False
    return True

# creates a list of all rotations of every slice in the puzzle
def getAllRotations(slices):
    allRotations = []       
    for s in slices:
        rotateRight = [s[2], s[0], s[1]]
        rotateLeft = [s[1], s[2], s[0]]
        allSliceRotations = [s, rotateRight, rotateLeft]
        allRotations.append(allSliceRotations)
    return allRotations

# creates a list of all rotations and flips of every slice in the puzzle
def getAllRotationsWithFlips(slices):
    allRotationsAndFlips = []
    for s in slices:
        rotateRight = [s[2], s[0], s[1]]
        rotateLeft = [s[1], s[2], s[0]]
        flip = [s[2], s[1], s[0]]
        flipRotateRight = [s[0], s[2], s[1]]
        flipRotateLeft = [s[1], s[0], s[2]]
        allSliceRotationsWithFlips = [s, rotateRight, rotateLeft, flip, flipRotateRight, flipRotateLeft]
        allRotationsAndFlips.append(allSliceRotationsWithFlips)
    return allRotationsAndFlips

# takes list of slices and attempts to find a solution
def solvePuzzle(slices, showResults, allowFlips):    
    if not allowFlips:
        puzzleRotations = getAllRotations(slices)
    else:
        puzzleRotations = getAllRotationsWithFlips(slices)

    rotationNum = len(puzzleRotations[0])
    sliceCount = len(slices)
    # list to hold valid combinations of slices
    solutionSet = []
    # list to keep track of slice rotations
    rotationPosition = [0]
    
    i = 0
    while i < sliceCount and rotationPosition[0] < rotationNum:
        # no rotations for current slice work, must backtrack to next rotation of previous slice
        if rotationPosition[i] >= rotationNum:
            solutionSet.pop()
            rotationPosition.pop()
            i -= 1
            rotationPosition[i] += 1
        # rotation is valid, add to combination list and increment slice counter and start at first rotation of next slice
        elif isValidSlice(solutionSet, puzzleRotations[i][rotationPosition[i]]):
            solutionSet.append(puzzleRotations[i][rotationPosition[i]])
            i += 1
            rotationPosition.append(0)
        # move to next rotation
        else:
            rotationPosition[i] += 1
    
    if showResults:
        if rotationPosition[0] >= rotationNum:
            # no solution, find minimum obstacle and attempt to solve with flips allowed
            minimumObstacle = findMinimumObstacle(slices)
            solvedWithFlips = solvePuzzle(slices, False, True)
            
            print("No Solution   MO =", len(minimumObstacle), "       Flip Solution")
            for s in range(len(slices)):
                print(slices[s], end ="     ")
                if s < len(minimumObstacle):
                    print(minimumObstacle[s], end ="     ")
                else:
                    print(end ="              ")
                print(solvedWithFlips[s])
            return []   
        else:
            for s in range(len(slices)):
                print(slices[s], "   ", solutionSet[s])
            return solutionSet
    else:
        if rotationPosition[0] >= rotationNum:
            return []
        else:
            return solutionSet

# finds the minimum obstacle of a puzzle with no solution
def findMinimumObstacle(slices):
    mininimumObstacle = slices
    poppedSlices = []
    # go through list of slices, popping a slice then checking if there is still an obstacle
    for n in range(len(slices)):
        poppedSlices = slices.copy()
        poppedSlices.pop(n)
        # there is still an obstacle
        if not solvePuzzle(poppedSlices, False, False):
            # recursive call to try to find an even smaller obstacle
            potentialMO = findMinimumObstacle(poppedSlices)
            if len(potentialMO) <= len(mininimumObstacle):
                mininimumObstacle = potentialMO
    return mininimumObstacle

main()