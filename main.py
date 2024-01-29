import random
import time
# Author: Mark Warren
# Date: 28/02/2021
# Purpose: Allows the user to play tic tac toe using minmax algorithm and combined classes using user terminal entry

class Player():
    # Acts as a super class to allow for other classes to inherit attributes belonging to this class
    # This particular class initialises norx allowing for the character of the player to be assigned as well as
    # a getter of the move of the player as a means to store moves made by the player in "oxo".

    def __init__(self, norx):
        self.norx = norx

    def get_move(self, oxo):
        pass


class HuPlay(Player):

    # After inheritance, the program reinitialises norx so that the specific character may be assigned to the Human
    # Player. In the get move function however, the program prompts for human input via keyboard entry and assign the integer
    # value to the location set by the player: furthermore, if the space is out of range or is not an enumerated
    # available move space - an error message will be thrown thus re-prompting them to re-enter their move decision.
    
    def __init__(self, norx):
        super().__init__(norx)

    def get_move(self, oxo):

        valid_playloc = False
        loc = None
        while not valid_playloc:
            moveloc = input(self.norx + '\'s turn. Enter Move Location (0-8):')
            try:
                loc = int(moveloc)
                if loc < 0 or loc > 8:
                    raise Exception
                if loc not in oxo.movelocavail():
                    raise ValueError
                valid_playloc = True
            except ValueError:
                print('This is an invalid movement choice. Choose a different location')
            except Exception:
                print("Error: Out of range value entered. Enter Move Location (0-8)")

        return loc


class RandComPlay(Player):
    
    # After inheritance, the program reinitialise norx so that the specific character may be assigned to the Random
    # Computer Player. The program uses a math method to randomly generate a choice available in the enumerated locations.
    
    def __init__(self, norx):
        super().__init__(norx)

    def get_move(self, oxo):
        moveloc = random.choice(oxo.movelocavail())
        return moveloc


class SmartComPlay(Player):
    
    # After inheritance, the program reinitialises norx so that the specific character may be assigned to the Smart
    # Computer Player. The program uses a math command to randomly generate a choice available in the enumerated locations if
    # no previous moves have been made by the other player. Else, the program uses the min max algorithm to generate an optimal
    # move that is left available for the computer.
    
    def __init__(self, norx):
        super().__init__(norx)

    def get_move(self, oxo):
        if len(oxo.movelocavail()) == 9:
            moveloc = random.choice(oxo.movelocavail())
        else:
            moveloc = self.minimax(oxo, self.norx)['position']
        return moveloc

    def minimax(self, state, player):
        
        # The program passes in the state of the current game through stored functions of class OXO. The program also
        # passes in the player class allowing to apply logic to the other player. The program will always generally want
        # the maximising player to be the "smart ai" rather than the other player because they are playing optimally
        # and will want to discern who is currently winning and losing in Tic Tac Toe so the ai can calculate the best
        # next move to be picked against the other player. The program can check whether the previous move has been made by
        # the other player was a winning move or not which will assign a higher or lower value to each grid space
        # depending on how many empty grid spaces are left available - the program assigns the best value of the score to the
        # lowest or highest score in order to calculate the best and worse moves so that the computer can choose the
        # highest assigned value of that move so the computer is always playing the most optimal depending on the
        # minmax algorithm's calculations. After the computer has simulated each move through various game states and
        # has assigned various scores to each possible position on the grid, we undo the move made so that the best
        # optimal move can be assigned to the computer - iterating through each move in order to determine
        # the move's value dependant on the state of play. Thus the program can calculate the best move
        # location to be passed back into the moveloc variable. Both players are maximizers trying to minimize their
        # opponent's total score.
       
        max_player = self.norx
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 2 * (state.emptygridsize() + 1) if other_player == max_player else -2 * (
                        state.emptygridsize() + 1)}
        elif not state.emptygrid():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -8000}
        else:
            best = {'position': None, 'score': 8000}
        for moveposs in state.movelocavail():
            state.make_move(moveposs, player)
            sim_score = self.minimax(state, other_player)  
            # goes through each of the moves left available in the grid
            # then assigns and calculates the most optimal move dependant on the highest calculated score of the various
            # states of play.
            state.grid[moveposs] = ' '
            state.current_winner = None
            sim_score['position'] = moveposs

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class OXO():
    
    # Initialises the oxo class with grid and current winner (set to none)
   
    def __init__(self):
        self.grid = self.grid()
        self.current_winner = None

    @staticmethod
    def grid():
       
        # makes a grid with 9 empty spaces

        return [' ' for _ in range(9)]

    def printgrid(self):
        
        # The program uses self.grid and display each number's value stored in the array held within each space for
        # display purposes including separators and gridlines to ensure clear visual representation of the game area.
        # This will update as each move is made meaning when a space is filled the board when reprinted will update to
        # display a space has been filled with that move. Thus allowing the player to see changes made to the grid.
        
        gline = '================='
        print('\n')
        print(gline)
        print('|| ' + self.grid[0] + ' || ' + self.grid[1] + ' || ' + self.grid[2] + ' ||')
        print(gline)
        print('|| ' + self.grid[3] + ' || ' + self.grid[4] + ' || ' + self.grid[5] + ' ||')
        print(gline)
        print('|| ' + self.grid[6] + ' || ' + self.grid[7] + ' || ' + self.grid[8] + ' ||')
        print(gline)

    @staticmethod
    def Intro():
        
        # Welcomes the user to the game and displays instructions on screen and prints out a digital
        # display of the grid with numbered spaces allowing for an easy visual interpretation of move locations.
        
        gline = '================='
        print('\n')
        print('Welcome to Noughts and Crosses')
        print('Enter a number between 0 - 8 as displayed in this grid to make your move')
        print(gline)
        print('|| ' + '0' + ' || ' + '1' + ' || ' + '2' + ' ||')
        print(gline)
        print('|| ' + '3' + ' || ' + '4' + ' || ' + '5' + ' ||')
        print(gline)
        print('|| ' + '6' + ' || ' + '7' + ' || ' + '8' + ' ||')
        print(gline)
    def make_move(self, moveloc, norx):
        
        # First checks to see if the movement space is empty and then assigns the grid space with the
        # predefined character of that player using self this then checks for if there is a winner after the
        # move was made returning true or false and also assigning a current winner with the current player's icon.
        
        if self.grid[moveloc] == ' ':
            self.grid[moveloc] = norx
            if self.winner(moveloc, norx):
                self.current_winner = norx
            return True
        return False

    def winner(self, moveloc, norx):
        
        # checks for a winner by checking to see if norx is present in each of the defined spaces and returning
        # a true and false statement based on the winning conditions predefined in this function
        
        # check the row (horizontal spaces) - 1st, 2nd, 3rd
        row1 = [self.grid[i] for i in [0, 1, 2]]
        row2 = [self.grid[i] for i in [3, 4, 5]]
        row3 = [self.grid[i] for i in [6, 7, 8]]
        # check the column (vertical spaces) - 1st, 2nd, 3rd
        col1 = [self.grid[i] for i in [0, 3, 6]]
        col2 = [self.grid[i] for i in [1, 4, 7]]
        col3 = [self.grid[i] for i in [2, 5, 8]]
        # check diagonal spaces
        diagonal1 = [self.grid[i] for i in [0, 4, 8]]
        diagonal2 = [self.grid[i] for i in [2, 4, 6]]
        if all([s == norx for s in row1]):
            return True
        if all([s == norx for s in row2]):
            return True
        if all([s == norx for s in row3]):
            return True
        if all([s == norx for s in col1]):
            return True
        if all([s == norx for s in col2]):
            return True
        if all([s == norx for s in col3]):
            return True
        if all([s == norx for s in diagonal1]):
            return True
        if all([s == norx for s in diagonal2]):
            return True
        return False

    def emptygrid(self):
        
        # Checks to see if there are any empty spaces available in the grid.
        
        return ' ' in self.grid

    def emptygridsize(self):
        # Counts how many available empty spaces are available in the grid.

        return self.grid.count(' ')

    def movelocavail(self):

        # Enumerates the available empty spaces left available in the grid
        
        return [i for i, x in enumerate(self.grid) if x == " "]


def play(oxo, x_player, o_player, print_oxo=True):

    # passes in the values of oxo, x_player, o_player and assigns a value of "print_oxo" so the program can determine
    # if we want the game to be visually displayed or not. If it's true, the program reprint the grid after each move has been
    # made, setting the starting player to X. The game will cycle through each "move" only when each move is valid
    # while the grid has empty spaces available - after a move is made and retrieved this will print out the number
    # of the move made by previous player, re-print the grid and check for a winning state - in which the game will
    # return and print out the winner thus ending the loop otherwise this will switch the player to the other player
    # via changing the value of norx hence allowing for seamless function of turn rotation until there are no more
    # available spaces. When the grid has ran out of available spaces and no winner has been previously declared: the
    # program will print out Draw and thus since this is no longer in a loop, will return to the main function.

    if print_oxo:
        oxo.Intro()

    norx = 'X'
    while oxo.emptygrid():
        if norx == 'O':
            moveloc = o_player.get_move(oxo)
        else:
            moveloc = x_player.get_move(oxo)
        if oxo.make_move(moveloc, norx):

            if print_oxo:
                print(norx + ' moves to {}'.format(moveloc))
                oxo.printgrid()
                print('')

            if oxo.current_winner:
                if print_oxo:
                    print(norx + ' wins!')
                return norx  # ends the loop
            norx = 'O' if norx == 'X' else 'X'  # switches player
        time.sleep(1)

    if print_oxo:
        print('Draw!')


if __name__ == '__main__':

    # This acts as the main function of the game - user is welcomed and then displayed options
    # in order to select different game modes: the WhoGo variable acts as the user input for this purpose - after they
    # have made a selection the values of x_player and o_player will be assigned to the classes which have predefined within
    # this program, this will also create an new instance of our game using start and the OXO class and then pass these
    # values into the play function along with assigning true to our print_oxo command. This will then only loop through
    # that choice selected else the try catch method will throw back an exception message to stop any
    # invalid entries causing problems and thus re-prompts the user for a valid numeric entry.
    # After which the game will then ask for another input thus re-prompting the same options if they have entered 1.
    # Anything else entered will cause the program to exit thus allowing the program to act naturally and only
    # execute commands when valid entries are made. 
    
        print("Welcome to the Tic Tac Toe Program")
        print("1. Human vs Computer")
        print("2. Computer vs Human")
        print("3. Human vs Human")
        print("4. Computer vs Computer")
        print("5. Human vs Random Computer")
        WhoGo = 0
        while WhoGo == 0:
            try:
                WhoGo= float(input("Enter a choice from the above:"))
                if WhoGo < 1 or WhoGo > 5:
                    raise Exception
            except Exception:
                print("Invalid Entered Choice. Choose Choice above (1-5)")
            else:
                if WhoGo == 1:
                    x_player = HuPlay('X')
                    o_player = SmartComPlay('O')
                    Start = OXO()
                    play(Start, x_player, o_player, print_oxo=True)
                    gameplease = float(input("Enter 1 to start a new Game:"))
                elif WhoGo == 2:
                    x_player = SmartComPlay('X')
                    o_player = HuPlay('O')
                    Start = OXO()
                    play(Start, x_player, o_player, print_oxo=True)
                    gameplease = float(input("Enter 1 to start a new Game:"))
                elif WhoGo == 3:
                    x_player = HuPlay('X')
                    o_player = HuPlay('O')
                    Start = OXO()
                    play(Start, x_player, o_player, print_oxo=True)
                    gameplease = float(input("Enter 1 to start a new Game:"))
                elif WhoGo == 4:
                    x_player = SmartComPlay('X')
                    o_player = SmartComPlay('O')
                    Start = OXO()
                    play(Start, x_player, o_player, print_oxo=True)
                    gameplease = float(input("Enter 1 to start a new Game:"))
                elif WhoGo == 5:
                    x_player = HuPlay('X')
                    o_player = RandComPlay('O')
                    Start = OXO()
                    play(Start, x_player, o_player, print_oxo=True)
                    gameplease = float(input("Enter 1 to start a new Game:"))
                if gameplease != 1:
                    exit;
                while gameplease == 1:
                    print("Welcome to the Tic Tac Toe Program")
                    print("1. Human vs Computer")
                    print("2. Computer vs Human")
                    print("3. Human vs Human")
                    print("4. Computer vs Computer")
                    print("5. Human vs Random Computer")
                    WhoGo = 0
                    while WhoGo == 0:
                        try:
                            WhoGo = float(input("Enter a choice from the above:"))
                            if WhoGo < 1 or WhoGo > 5:
                                raise Exception
                        except Exception:
                                print("Invalid Entered Choice. Choose Choice above (1-5)")
                        else:
                            if WhoGo == 1:
                                x_player = HuPlay('X')
                                o_player = SmartComPlay('O')
                                Start = OXO()
                                play(Start, x_player, o_player, print_oxo=True)
                                gameplease = float(input("Enter 1 to start a new Game:"))
                            elif WhoGo == 2:
                                x_player = SmartComPlay('X')
                                o_player = HuPlay('O')
                                Start = OXO()
                                play(Start, x_player, o_player, print_oxo=True)
                                gameplease = float(input("Enter 1 to start a new Game:"))
                            elif WhoGo == 3:
                                x_player = HuPlay('X')
                                o_player = HuPlay('O')
                                Start = OXO()
                                play(Start, x_player, o_player, print_oxo=True)
                                gameplease = float(input("Enter 1 to start a new Game:"))
                            elif WhoGo == 4:
                                x_player = SmartComPlay('X')
                                o_player = SmartComPlay('O')
                                Start = OXO()
                                play(Start, x_player, o_player, print_oxo=True)
                                gameplease = float(input("Enter 1 to start a new Game:"))
                            elif WhoGo == 5:
                                x_player = HuPlay('X')
                                o_player = RandComPlay('O')
                                Start = OXO()
                                play(Start, x_player, o_player, print_oxo=True)
                                gameplease = float(input("Enter 1 to start a new Game:"))