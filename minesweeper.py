# Samuel Hartley, Minesweeper Christmas project
import random
import re

class Cell:
    def __init__(self):
        self._covered = True
        self._num = 0
        self._mine = False
        self._flagged = False
    
    def __str__(self):
        if self._flagged:
            return "F"
        elif self._covered:
            return "-"
        elif self._mine:
            return "M"
        elif self._num != 0:
            return str(self._num)
        else:
            return " "
    
    # Getters
    def isMine(self):
        return self._mine
    def isFlagged(self):
        return self._flagged
    def getNum(self):
        return self._num
    def isCovered(self):
        return self._covered
    def isBlank(self):
        if not self._flagged and not self._covered and not self._mine and self._num == 0:
            return True
        return False
    
    # Setters
    def setMine(self):
        self._mine = True
    def setNum(self, num):
        self._num = num
    def setFlag(self, val):
        # Returns true if the value was changed
        if self._flagged != val:
            self._flagged = val
            return True
        return False
    def uncover(self):
        self._covered = False


# Board for the minesweeper game
class Board:
    def __init__(self):
        self._STARTMINES = 10
        self._numFlags = 10
        self._cells = [[Cell() for j in range(9)] for i in range(9)]
        self._running = True
        self._addedBombs = False

    
    def __str__(self):
        output = """ +---------+
 |  M:{}   |
 +---------+
 |ABCDEFGHI|
 +---------+\n""".format(str(self._numFlags).zfill(2))

        output2 = ""
        for y in range(9):
            line = str(y)+"|"+"".join([str(c) for c in self._cells[y]])+"|"+"\n"
            output2 += line
        
        return output + output2 + " +---------+\n"
    
    def _setup(self, start):
        # Start is a coordinate that cannot be a bomb
        bombsLeft = self._STARTMINES
        while bombsLeft != 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if (x, y) != start and not self._cells[x][y].isMine():
                self._cells[y][x].setMine()
                # Update nums around the bomb
                self._addNumbers((x, y))
                bombsLeft -= 1


    def _addNumbers(self, bomb):
        # Adds 1 all the cells around a bomb
        for y in [-1, 0, 1]:
            y += bomb[1]
            for x in [-1, 0, 1]:
                x += bomb[0]
                if 9 > x > -1 and 9 > y > -1 and (x, y) != bomb:
                    if not self._cells[y][x].isMine():
                        self._cells[y][x].setNum(self._cells[y][x].getNum()+1)


    def _charToNum(self, char: str):
        """Maps a char from [A-I] to [0-8]"""
        return ord(char)-65

    
    def _clearEmpty(self, start, visited=[]):
        """Clears the empty cells around a starting cell"""
        # Clear neighbours
        visited.append(self._cells[start[1]][start[0]])
        for y in [-1, 0, 1]:
            y += start[1]
            for x in [-1, 0, 1]:
                x += start[0]
                if 9 > x > -1 and 9 > y > -1 and (x, y) != start:
                    self._cells[y][x].uncover()
                    if self._cells[y][x].isBlank() and self._cells[y][x] not in visited:
                        self._clearEmpty((x, y), visited)
    

    # Inputs
    def getInput(self, inp: str) -> bool:
        # Checks if an input is valid
        if bool(re.search("[F|U|C]\[[A-I][0-8]\]", inp)):
            x, y = (self._charToNum(inp[2]), int(inp[3]))
            # Add a flag
            if inp[0] == "F":
                if self._cells[y][x].isCovered():
                    if self._cells[y][x].setFlag(True):
                        self._numFlags -= 1
                else:
                    print("Cannot flag an uncovered cell")
            # Undo a flag
            if inp[0] == "U":
                if self._cells[y][x].setFlag(False):
                    self._numFlags += 1
            # Uncover a cell
            if inp[0] == "C":
                if not self._cells[y][x].isFlagged() and self._cells[y][x].isCovered():
                    self._cells[y][x].uncover()
                    if self._addedBombs == False:
                        self._setup((x, y))
                        self._addedBombs = True
                    if self._cells[y][x].isBlank():
                        self._clearEmpty((x, y))
                    
                    if self._cells[y][x].isMine():
                        self._lose()
                else:
                    print("Cannot uncover this cell")

        else:
            print("Invalid Command")
        
        print(self._numFlags)
    
    def checkWin(self):
        if self._running:
            # Win if num of flags left is zero and all are in correct place
            if self._numFlags == 0:
                # Check mine positions
                check = True
                for row in self._cells:
                    for cell in row:
                        if (cell.isFlagged() and not cell.isMine()) or (not cell.isFlagged() and cell.isMine()):
                            check = False
                if check == True:
                    self._win()

    def _win(self):
        self._running = False
        print(str(self))
        print("You Win! Congratulations!")
        input("<Press enter to play again>\n")

    def _lose(self):
        self._running = False
        print("You Lose! You clicked on a mine!")
        input("<Press enter to play again>\n")
    
    def isRunning(self):
        return self._running


def main():
    while True:
        board = Board()
        while board.isRunning():
            print(str(board))
            board.getInput(input("Enter Command:\nF - Flag\nU - Unflag\nC - Uncover\n>>> "))
            board.checkWin()


if __name__ == "__main__":
    main()