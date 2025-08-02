class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_disks = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
        
    def clear(self):
        self.num_disks = [0] * self.size
        self.items = [[0] * self.size for i in range(self.size)]
        self.points = [0, 0]
    
    def num_free_positions_in_column(self, column):
        return self.size - self.num_disks[column]
    
    def game_over(self):
        disk_counter = 0
        
        for disk in self.num_disks:
            if disk == self.size:
                disk_counter += 1
        
        if disk_counter == self.size:
            return True
        
        else:
            return False
    
    def display(self):
        # Print the game board from bottom to top
        for row in range(self.size-1, -1, -1):
            for column in range(self.size):
                if self.items[column][row] == 1:
                    print("o", end = " ")
                elif self.items[column][row] == 2:
                    print("x", end = " ")
                else:
                    print(" ", end = " ")
            print()
            
        # Print the borders
        print("- " * (self.size))
        
        # Print the column numbers
        for i in range(self.size):
            print(i, end = " ")
            
        print()
        print()
        print(f"Player 1: {self.points[0]}")
        print(f"Player 2: {self.points[1]}")

    def add(self, column, player):
        if self.num_disks[column] >= self.size or column < 0 or column >= self.size:
            return False
        else:
            row = self.num_disks[column]
            self.items[column][self.num_disks[column]] = player
            self.num_disks[column] += 1
            # Update points based on the disk added
            self.points[player-1] += self.num_new_points(column, row, player)
            return True
    
    def num_new_points(self, column, row, player):
        new_points = 0

        # Horizontal Counter
        horizontal_count = 0
        
        # Get the boundaries according to the disk being checked
        start_col = max(0, column - 3)
        end_col = min(self.size - 1, column + 3)
        
        # Go through the game board starting from the start boundary to end boundary
        for i in range(start_col, end_col + 1):
            if self.items[i][row] == player:
                horizontal_count += 1
                if horizontal_count >= 4: # Continue counting points starting from 4, e.g. 5 count = 2 pts, 6 count = 3 pts.
                    new_points += 1
            else:
                horizontal_count = 0 # Reset the count if disk doesn't match

        # Vertical Counter
        vertical_count = 0
        
        # Get the boundaries according to the disk being checked
        start_row = max(0, row - 3)
        end_row = min(self.size - 1, row + 3)
        
        # Go through the game board starting from the start boundary to end boundary
        for i in range(start_row, end_row + 1):
            if self.items[column][i] == player:
                vertical_count += 1
                if vertical_count >= 4: # Continue counting points starting from 4, e.g. 5 count = 2 pts, 6 count = 3 pts.
                    new_points += 1
            else:
                vertical_count = 0 # Reset the count if disk doesn't match
        
        # Diagonal Counter ! 
        
        # Right to Left (this goes in this direction -> / <-)
        rl_diagonal_count = 0

        # RL Up Counter, get the position of current disk
        rl_up_col = column
        rl_up_row = row
        rl_up_counter = 0
        
        # Get the end boundaries, stops when either the counter iterated 4 times or column = 0, and row = size
        while rl_up_col >= 0 and rl_up_row < self.size:
            rl_up_col -= 1
            rl_up_row += 1
            rl_up_counter += 1
            if rl_up_counter == 4:
                break

        # RL Down Counter, get the position of current disk
        rl_down_col = column
        rl_down_row = row
        rl_down_counter = 0
        
        # Get the start boundaries, stops when either the counter iterated 4 times or within 0 and the size
        while rl_down_col < self.size and rl_down_row >= 0:
            rl_down_col += 1
            rl_down_row -= 1
            rl_down_counter += 1
            if rl_down_counter == 4:
                break
        
        # Initialize the boundaries from the calculations above
        rl_start_col = rl_down_col - 1
        rl_start_row = rl_down_row + 1
        rl_end_col = rl_up_col
        rl_end_row = rl_up_row
        
        # Go through the game board and check the matching sequences
        while rl_start_col > rl_end_col and rl_start_row < rl_end_row:
            if self.items[rl_start_col][rl_start_row] == player:
                rl_diagonal_count += 1
                if rl_diagonal_count >= 4:
                    new_points += 1
            else:
                rl_diagonal_count = 0
                
            rl_start_col -= 1
            rl_start_row += 1
            
        # Left to Right (this goes in this direction -> \ <-)
        lr_diagonal_count = 0

        # LR Up Counter, get the position of current disk
        lr_up_col = column
        lr_up_row = row
        lr_down_counter = 0

        # Get the end boundaries, stops when either the counter iterated 4 times or within 0 and the size
        while lr_up_col < self.size and lr_up_row < self.size:
            lr_up_col += 1
            lr_up_row += 1
            lr_down_counter += 1
            if lr_down_counter == 4:
                break

        # LR Down Counter, get the position of current disk
        lr_down_col = column
        lr_down_row = row
        lr_down_counter = 0
        
        # Get the start boundaries, stops when either the counter iterated 4 times or within 0 and the size
        while lr_down_col >= 0 and lr_down_row >= 0:
            lr_down_col -= 1
            lr_down_row -= 1
            lr_down_counter += 1
            if lr_down_counter == 4:
                break
        
        # Initialize the boundaries from the calculations above
        lr_start_col = lr_down_col + 1
        lr_start_row = lr_down_row + 1
        lr_end_col = lr_up_col
        lr_end_row = lr_up_row

        # Go through the game board and check the matching sequences
        while lr_start_col < lr_end_col and lr_start_row < lr_end_row:
            if self.items[lr_start_col][lr_start_row] == player:
                lr_diagonal_count += 1
                if lr_diagonal_count >= 4:
                    new_points += 1
            else:
                lr_diagonal_count = 0
            lr_start_col += 1
            lr_start_row += 1

        return new_points
    
    def free_slots_as_close_to_middle_as_possible(self):
        # A temporary list to store the slots sorted such that the closest to the middle goes first
        templist = []
        free_slots = []
        
        # Check if the size of the gameboard is even
        # Get the two middle values then append the smaller one first
        if self.size % 2 == 0:
            right_middle_index = self.size // 2
            left_middle_index = right_middle_index - 1
            templist.append(left_middle_index)
            templist.append(right_middle_index)
            
            leftindex = left_middle_index
            rightindex = right_middle_index
            
            # Go from the middle in both directions, append the smaller values first always
            for i in range(left_middle_index-1, -1, -1):
                leftindex -= 1
                rightindex += 1
                templist.append(leftindex)
                templist.append(rightindex)
        
        # If the size of the gameboard is odd
        # Get the middle value
        else:
            middle_index = self.size // 2
            templist.append(middle_index)
            
            leftindex = middle_index
            rightindex = middle_index
            
            # Same thing from above, go in both directions and append the values small first
            for i in range(middle_index-1, -1, -1):
                leftindex -= 1
                rightindex += 1
                templist.append(leftindex)
                templist.append(rightindex)
                
        # Check each column based on the sorted temporary list, and append it to the new list that contains free slots only
        for i in templist:
            if self.num_free_positions_in_column(i) > 0:
                free_slots.append(i)
        
        return free_slots
    
    def column_resulting_in_max_points(self, player):
        # Make one list to store max points of that column, and one list to store the column number corresponding to the point list
        points_list = []
        slot_list = []
        
        # Go through all the columns, check if they have free slots
        for i in range(self.size):
            if self.num_free_positions_in_column(i) > 0:
                # Temporarily place the disk to get the maximum points possible from that move
                row = self.num_disks[i]  
                self.items[i][row] = player
                points = self.num_new_points(i, row, player)
                
                # Store the possible points, and its corresponding slot/column number
                points_list.append(points)
                slot_list.append(i)
                
                # Reset the slot to avoid getting miscalculations from the gameboard
                self.items[i][row] = 0
        
        # Get the maximum points
        highest_points = max(points_list)
        
        # Make a temporary list to store the slots/column numbers that hold the value with maximum points
        templist = []
        for i in range(len(points_list)):
            if points_list[i] == highest_points:
                templist.append(slot_list[i])
        
        # Check if the list only has one value, return it along with the points, else, get the slot that is closest to middle
        if len(templist) == 1:
            return templist[0], highest_points
        else:
            free_slots = self.free_slots_as_close_to_middle_as_possible()
            for slot in free_slots:
                if slot in templist:
                    return slot, highest_points

        return templist[0], highest_points

    def menu_pages(self):
        print("Welcome to Connect 4!")
        print("1. Rules and How To Play")
        print("2. Gameplay Example")
        print("3. Tips and Tricks")
        print()
        print("4. Start Game")

    def page_1(self):
        print()
        print("Connect 4: Rules and How To Play")
        print("- - - - - - - - - - - - - - - - -")
        print("1. The game is played by two players.")
        print()
        print("2. There will be a gameboard displayed as a square \nin which it will have n columns * n rows.")
        print()
        print("3. The two players will take turns inserting a disk into any column as long as it is not full.")
        print()
        print("4. Player 1 will be represented by circles 'O' while \nPlayer 2 will be represented by crosses 'X'.")
        print()
        print("5. The goal of the game is to create a 4-in-a-row sequence of the same disk, \nand it can be in a vertical, horizontal, or diagonal direction.")
        print()
        print("6. One 4-in-a-row sequence leads to the player getting 1 point.")
        print()
        print("7. If a 5-in-a-row sequence exists, the player will gain 2 points from that sequence, \nsince there are 2 sets of 4-sequences in the 5-sequence.")
        print()
        print("8. The same applies if there are 6-in-a-row, and more. Once a player hits 4-in-a-row \nand continues to add a matching disk to that sequence, the player gains an additional point every time.")
        print()
        print("9. The game will only end once the gameboard is full \nand no disks can be inserted anymore.")
        print()
        print("10. The player with the highest points wins Connect 4.")
        print()
        print()

        while True:
            page_1_return = input("Enter 1 to go back to the menu: ")
            if page_1_return == "1":
                print()
                print()
                self.menu()
                break

        

    def page_2(self):
        # Horizontal Sequence Example
        print()
        print("Connect 4: Gameplay Example")
        print("Horizontal Sequence")
        
        self.add(0, 1)
        self.add(0, 2)
        self.add(1, 1)
        self.add(1, 2)
        self.add(2, 1)
        self.add(2, 2)
        self.add(3, 1)
        self.display()
        
        print()
        print("The example above shows how to get a point from a 4-in-a-row horizontal sequence.")
        print("As you can see, Player 1 has 1 point because he has 4 matching disks from 0,0 to 3,0.")
        self.clear()
        print()
        print()
        
        while True:
            go_vertical = input("Enter 1 to go to the next example: ")
            if go_vertical.lower() == "1":
                break
            
        # Verftical Sequence Example
        if go_vertical.lower() == "1":
            print()
            print()
            print("Connect 4: Gameplay Example")
            print("Vertical Sequence")
            print()
            print()
            
            self.add(0, 1)
            self.add(1, 2)
            self.add(0, 1)
            self.add(1, 2)
            self.add(0, 1)
            self.add(1, 2)
            self.add(0, 1)
            self.display()
            
            print()
            print("This example shows how to get a point in a vertical sequence.")
            print("Player 1 currently has 1 point as he has 4-in-a-row sequence from 0,0 to 0,3.")
            self.clear()
            print()
            print()

        # Diagonal Sequence Example
        while True:
            go_diagonal = input("Enter 1 to go to the next example: ")
            if go_diagonal.lower() == "1":
                break

        if go_diagonal.lower() == "1":
                print()
                print()
                print("Connect 4: Gameplay Example")
                print("Diagonal Sequence")
                print()
                print()
                
                self.add(0, 1)
                self.add(1, 2)
                self.add(1, 1)
                self.add(3, 2)
                self.add(2, 1)
                self.add(2, 2)
                self.add(2, 1)
                self.add(3, 2)
                self.add(0, 1)
                self.add(3, 2)
                self.add(3, 1)
                self.display()
                
                print()
                print("The example above, this time, shows how to get a point diagonally.")
                print("This works in any direction, as long as you make a sequence in a diagonal manner.")
                print("Player 1 gained 1 point from having a sequence starting from 0,0 to 3,3.")
                self.clear()
                print()
                print()

        while True:
            go_back = input("Enter 1 to go back to the menu: ")
            if go_back == "1":
                print()
                self.menu()
                break
               
                        
            
    def page_3(self):
        print()
        print("Connect 4: Tips and Tricks")
        print("- - - - - - - - - - - - - -")
        print("1. Try to be player one, as they tend to dictate the flow of the game")
        print()
        print("2. Always fill up the middle area of the board, \nas it opens up to lots of potential points later on.")
        print()
        print("3. Avoid rushing to create a sequence, instead, \nspread your disks all over the board for more chances.")
        print()
        print("4. Think one move ahead and always take the move that gives you the most points.")
        print()
        print("5. Try to set up traps for the opponent by baiting them \nto make a move, which in turn can give you even more points.")
        print()
        print("6. Keep playing and stay focused! Experience is essential in this game!")
        print()

        while True:
            page_3_return = input("Enter 1 to go back to the menu: ")
            if page_3_return == "1":
                print()
                print()
                self.menu()
                break
        
        

    def menu(self):
        # Display the main menu
        self.menu_pages()
        print()
        while True:
                page = input("Enter a page: ")
                if page in ("1", "2", "3", "4"):
                    break  
                else:
                    print("Enter a page from 1-3, or 4 to start the game.")
                    
        # Call the rules and conditions
        if page == "1":
            print()
            self.page_1()

        # Call the gameplay example page
        elif page == "2":
            print()
            self.page_2()
            
        # Call the tips and tricks page
        elif page == "3":
            print()
            self.page_3()

        # Start the game
        elif page == "4":
            self.play()
        

    def play(self):
        self.display()
        while self.game_over() == False:
            print()
            move_1 = int(input("Player 1, enter your move: "))
            self.add(move_1, 1)
            self.display()
            print()
            move_2 = int(input("Player 2, enter your move: "))
            self.add(move_2, 2)
            self.display()

        if self.game_over() == True:
            print()
            if self.points[0] > self.points[1]:  
                print("Game Over! Player 1 Wins!")
            elif self.points[0] < self.points[1]:
                print("Game Over! Player 2 Wins!")
            elif self.points[0] == self.points[1]:
                print("Game Over! It's a Tie!")

    
            


               
        

test = GameBoard(4)
test.menu()
