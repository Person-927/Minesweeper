import random,os,time

class minesweeper():
    def __init__(self):
        self.nums = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        self.grid_height = 10  # Update later for dif
        self.grid_width = 10  # Update later for dif
        self.output_grid = []
        self.grid = []
        self.mine_count = 25  # Update later for dif
        self.mine_locations = []
        self.flag_locations = []
        self.dug_locations = []
        self.collum = 0
        self.row = 0
        self.play = True
    
    def main(self):
        self.game_start()
        while self.play:
            self.coord_picker()
        
    def clear(self):
        time.sleep(0.5)
        os.system("cls")

    def grid_create(self):  # Creates a Grid
        index = 0
        for i in range(0,self.grid_height):
            self.output_grid.append([])
            self.grid.append([])
            for j in range(0,self.grid_width):
                self.output_grid[index].append("🟩")
                self.grid[index].append(0)
            index += 1

    def grid_output(self):  # Outputs Grid
        # Top Number Line for Grid
        line = " "
        for i in range(0,self.grid_width):
            line = line + "  " + self.nums[i]
        print(line)

        # Fills in rest of the grid
        index = 0
        for i in range(0,self.grid_height):
            line = self.nums[index] + " " # Number at start of line
            index += 1
            for j in range(0,self.grid_width):
                line = line + " " + str(self.output_grid[i][j]) # Fills in all green tiles for grid
            print(line)

    def populate_mines(self):  # Creates Mine Locations
        org_row = self.row
        org_col = self.collum
        mines = 0
        start = str(self.row) + "," + str(self.collum)
        while mines < self.mine_count:
            coord = ""
            self.collum = random.randint(0,self.grid_width-1)
            self.row = random.randint(0,self.grid_height-1)
            coord = str(self.row) + "," + str(self.collum) # Create Random Coords
            if coord not in self.mine_locations and coord != start: # Checks if coords already exist
                self.mine_locations.append(coord)
                self.grid[self.row][self.collum] = "M"
                mines += 1
        self.mine_locations.sort() # Sorts Mine Location list
        self.row = org_row
        self.collum = org_col

    def coord_picker(self): # Lets User enter any location on the board
        self.clear()
        self.grid_output()

        while True: # Enter a valid collum
            self.collum = input("\nEnter Collum Number: ")
            if self.collum.isnumeric():
                self.collum = int(self.collum)
                if self.collum > -1 and self.collum < self.grid_width:
                    break
                else:
                    print("Invalid Collum")
                    time.sleep(0.15)
                    self.clear()
                    self.grid_output()
            else:
                print("Invalid Collum - Not a Number")
                time.sleep(0.15)
                self.clear()
                self.grid_output()        

        while True: # Enter a valid row
            self.row = input("\nEnter Row Number: ")
            if self.row.isnumeric():
                self.row = int(self.row)
                if self.row > -1 and self.row < self.grid_height:
                    break
                else:
                    print("Invalid row")
                    time.sleep(0.15)
                    self.clear()
                    self.grid_output()
                    print(f"\nEnter Row Number: {self.row}")
            else:
                print("Invalid row - Not a Number")
                time.sleep(0.15)
                self.clear()
                self.grid_output()
                print(f"\nEnter Collum Number: {self.collum}")
        
        self.coord_choices()

    def mine_nums(self):    # Puts how many bombs are surrounding a square
        for row in range(0,self.grid_height):
            for collum in range(0,self.grid_width):
                # Check if location has a mine
                if self.grid[row][collum] == "M":
                    continue
                # Check up
                if row > 0 and self.grid[row-1][collum] == "M":
                    self.grid[row][collum] += 1
                # Check Below
                if row < self.grid_height-1 and self.grid[row+1][collum] == "M":
                    self.grid[row][collum] += 1
                # Check Left
                if collum > 0 and self.grid[row][collum-1] == "M":
                    self.grid[row][collum] += 1
                # Check Right
                if collum < self.grid_width-1 and self.grid[row][collum+1] == "M":
                    self.grid[row][collum] += 1
                # Check Top Left
                if collum > 0 and collum > 0 and self.grid[row-1][collum-1] == "M":
                    self.grid[row][collum] += 1
                # Check Top Right
                if row > 0 and collum < self.grid_width-1 and self.grid[row-1][collum+1] == "M":
                    self.grid[row][collum] += 1
                # Check Bottom Left
                if row < self.grid_height-1 and collum > 0 and self.grid[row+1][collum-1] == "M":
                    self.grid[row][collum] += 1
                # Check Bottom Right
                if row < self.grid_height-1 and collum < self.grid_width-1 and self.grid[row+1][collum+1] == "M":
                    self.grid[row][collum] += 1

    def show_mines(self):   # Shows all mine location to main player grid
        for coords in self.mine_locations:
            coords = coords.split(",")
            self.output_grid[int(coords[0])][int(coords[1])] = "💣" # Replace current sqaure with a mine
        self.clear()
        self.grid_output()

    def coord_choices(self):    # Gives options on what can be done with each square
        self.clear()
        self.grid_output()
        print(f"Tile {self.collum},{self.row}\n") # Prints ouy thr tile selected by the user

        square = self.grid[self.row][self.collum] # Identifies what is locaed at the square
        if (str(self.row) + "," + str(self.collum)) in self.dug_locations: # Checks to see if sqaure has been dug already
            print("This Square has already been dug up")
            time.sleep(0.25)
            self.coord_picker()
        elif (str(self.row) + "," + str(self.collum)) in self.flag_locations: # Checks if flag is in the location
            if input("Would you like to remove the flag?: "):
                self.clear()
                self.remove_flag()
            else:
                self.coord_picker()
        else:
            while True: # Menu for what can be done to the square selected
                print("1. Dig\n2. Flag\n3. Cancel")
                choice = input()
                if choice.isnumeric():
                    match int(choice):
                        case 1: # Checks if option 1 - Dig
                            self.dig_square()
                            break
                        case 2: # Checks if option 2 - Flag
                            self.add_flag()
                            break
                        case 3: # Checks if option 3 - Cancel
                            self.coord_picker() 
                            break
                        case other:
                            print("Invalid Input")
                            self.coord_choices()
                else:
                    print("Not a number")
                    self.coord_choices()

    def dig_square(self):   # Digs a square
        if self.grid[self.row][self.collum] == "M":
            self.explode()
        else:
            self.dug_locations.append(str(self.row) + "," + str(self.collum))
            self.output_grid[self.row][self.collum] = "🟨"

    def explode(self):  # If mine hit, then explode all mines
        self.play = False
        self.output_grid[self.row][self.collum] = "💥"
        self.mine_locations.remove(str(self.row) + "," + str(self.collum))
        for coord in self.mine_locations:
            coord = coord.split(",")
            self.output_grid[int(coord[0])][int(coord[1])] = "💥"
            self.clear()
            self.grid_output()
        
    def add_flag(self): # Adds a flag to a square
        coord = str(self.row) + "," + str(self.collum)
        self.flag_locations.append(coord)
        self.output_grid[self.row][self.collum] = "🚩"
        self.clear()
        self.grid_output()

    def remove_flag(self): # Removes a flag from a square
        coord = str(self.row) + "," + str(self.collum)
        self.flag_locations.remove(coord)
        self.output_grid[self.row][self.collum] = "🟩"
        self.clear()
        self.grid_output()

    def game_start(self):   # Start sequence of the game
        self.grid_create() # Creates the output grid and backend grid
        self.grid_output()

        while True: # Enter a valid collum
            self.collum = input("\nEnter Collum Number: ")
            if self.collum.isnumeric():
                self.collum = int(self.collum)
                if self.collum > -1 and self.collum < self.grid_width:
                    break
                else:
                    print("Invalid Collum")
                    time.sleep(0.15)
                    self.clear()
                    self.grid_output()
            else:
                print("Invalid Collum - Not a Number")
                time.sleep(0.15)
                self.clear()
                self.grid_output()        

        while True: # Enter a valid row
            self.row = input("\nEnter Row Number: ")
            if self.row.isnumeric():
                self.row = int(self.row)
                if self.row > -1 and self.row < self.grid_height:
                    break
                else:
                    print("Invalid row")
                    time.sleep(0.15)
                    self.clear()
                    self.grid_output()
                    print(f"\nEnter Row Number: {self.row}")
            else:
                print("Invalid row - Not a Number")
                time.sleep(0.15)
                self.clear()
                self.grid_output()
                print(f"\nEnter Collum Number: {self.collum}")
        
        self.dig_square()
        self.populate_mines()
        self.zero_removal_vert()
        

        # Make it so all squares of 0 are dug up untill it hits number from selected coords outwards 

    def zero_removal_vert(self):
        org_row = self.row

        while self.row > -1:
            if self.grid[self.row][self.collum] == 0:
                self.output_grid[self.row][self.collum] = "🟨"
            else:
                self.output_grid[self.row][self.collum] = "⬜"
                break
            self.zero_removal_hori()
            self.row -= 1
        self.row = org_row

        while self.row < self.grid_height:
            if self.grid[self.row][self.collum] == 0:
                self.output_grid[self.row][self.collum] = "🟨"
            else:
                self.output_grid[self.row][self.collum] = "⬜"
                break
            self.zero_removal_hori()
            self.row += 1

        self.row = org_row


    def zero_removal_hori(self):
        org_col = self.collum

        while self.collum > -1:
            if self.grid[self.row][self.collum] == 0:
                self.output_grid[self.row][self.collum] = "🟨"
            else:
                self.output_grid[self.row][self.collum] = "⬜"
                break
            # self.zero_removal_vert()
            self.collum -= 1
        
        self.collum = org_col

        while self.collum < self.grid_width:
            if self.grid[self.row][self.collum] == 0:
                self.output_grid[self.row][self.collum] = "🟨"
            else:
                self.output_grid[self.row][self.collum] = "⬜"
                break
            # self.zero_removal_vert()
            self.collum += 1
        
        self.collum = org_col
        


        

    # def Number of mines around a square to output grid

test = minesweeper()
test.main()


# "0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"
# 🚩
# ⬜
# ⬛
# 🟨
# 🟩
# 💣
# 💥
# Average 1 Mine / 7 Squares
