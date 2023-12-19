import socket
import tkinter as tk
from gameboard import BoardClass

class Player1():
    """A class to create a Player 1 object that stores player and game information.

    Creates a player object and an object that stores player 1's gameboard. Initializes player 1's username, symbol,
    and socket and prompts the user for player 2's host information to create a socket connection between the two
    players. Uses sockets to send and receive moves from player 2, and uses the gameboard object to store each move.
    The board is checked for wins and ties after each move."""
    def __init__(self) -> None:
        self.p1username = ""
        self.p2username = ""
        self.p1symbol = "X"
        self.p2symbol = "O"
        self.p1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.windowSetup()
        self.connectUI()
        self.runUI()

    def windowSetup(self) -> None:
        """A function to set up the game window for Tkinter."""
        self.win = tk.Tk()
        self.win.title("Tic Tac Toe")
        self.win.geometry("500x500")
        self.win.configure(background='light blue')
        self.win.resizable(0,0)

    def connectUI(self) -> None:
        """A function to set up the GUI for inputting player 2's host information."""
        self.prompt = tk.Label(self.win, text="Enter Player 2's host information to connect:", bg='light blue')
        self.prompt.place(x=130, y=30)

        self.ipLabel = tk.Label(self.win, text="IP Address", bg='light blue')
        self.ipLabel.place(x=100, y=60)

        self.ipaddress = tk.StringVar(self.win)
        self.ipEntry = tk.Entry(self.win, textvariable=self.ipaddress, width=30)
        self.ipEntry.place(x=100, y=80)

        self.portLabel = tk.Label(self.win, text="Port Number", bg='light blue')
        self.portLabel.place(x=100, y=100)

        self.portnumber = tk.StringVar(self.win)
        self.portEntry = tk.Entry(self.win, textvariable=self.portnumber, width=30)
        self.portEntry.place(x=100, y=120)

        self.connectButton = tk.Button(self.win, text='Connect', command=self.tryConnect, width=10)
        self.connectButton.place(x=100, y=160)

        self.connectPrompt = tk.StringVar(self.win)
        self.connectLabel = tk.Label(self.win, bg='light blue', textvariable=self.connectPrompt)
        self.connectLabel.place(x=250, y=200, anchor="n")

    def tryConnect(self) -> None:
        """A function to attempt to connect to player 2 using the host information inputted by player 1.

        If a connection exception occurs, tryAgain function is called."""
        try:
            self.p1socket.connect((self.ipaddress.get(), int(self.portnumber.get())))
            self.connectPrompt.set("Connection Successful!")
            self.ipEntry["state"] = "disabled"
            self.portEntry["state"] = "disabled"
            self.connectButton["state"] = "disabled"
            self.usernameUI()

        except ConnectionRefusedError:
            self.tryAgain()

    def tryAgain(self) -> None:
        """A function to prompt the user after a failed connection.

        If the user clicks the yes button, they can try to connect again. If the user clicks No, the program ends."""
        self.connectPrompt.set("Connection Failed. Try Again?")

        self.tryAgainYes = tk.Button(self.win, text='Yes', width=5, command=self.resetConnect)
        self.tryAgainYes.place(x=180, y=250)

        self.tryAgainNo = tk.Button(self.win, text='No', width=5, command=quit)
        self.tryAgainNo.place(x=275, y=250)

        self.ipEntry["state"] = "disabled"
        self.portEntry["state"] = "disabled"
        self.connectButton["state"] = "disabled"

    def resetConnect(self) -> None:
        """A function to reset the window to restart connection attempt."""
        self.connectPrompt.set(" ")
        self.tryAgainYes.destroy()
        self.tryAgainNo.destroy()

        self.ipEntry["state"] = "normal"
        self.portEntry["state"] = "normal"
        self.connectButton["state"] = "normal"

    def usernameUI(self) -> None:
        """A function to set up the interface for the player to enter their username."""
        self.usernameEntryMessage = tk.Label(self.win, text="Enter an alphanumeric username:", bg='light blue')
        self.usernameEntryMessage.place(x=250, y=280, anchor="n")

        self.p1username = tk.StringVar(self.win)
        self.usernameEntry = tk.Entry(self.win, textvariable=self.p1username)
        self.usernameEntry.place(x=250, y=320, anchor='n')

        self.usernameButton = tk.Button(self.win, text='Enter', command=self.checkUsername, width=10)
        self.usernameButton.place(x=250, y=370, anchor='n')

        self.usernamePrompt = tk.StringVar(self.win)
        self.usernameLabel = tk.Label(self.win, bg='light blue', textvariable=self.usernamePrompt)
        self.usernameLabel.place(x=250, y=410, anchor='n')

    def checkUsername(self) -> None:
        """A function to check if a username is alphanumeric.

        If the username is alphanumeric, it is sent to player 2. The window is cleared and the game starts. If the
        username is invalid, the user is asked to try again."""
        if self.p1username.get().isalnum():
            # sending valid username to player 2
            self.p1username = self.p1username.get()
            p1board.getp1username(self.p1username)
            self.sendData(self.p1username)

            # receiving player 2's username
            self.win.update_idletasks()
            self.p2username = self.receiveData()
            p1board.getp2username(self.p2username)

            self.clearWindow()
            self.gameboardUI()
        else:
            self.usernamePrompt.set("Invalid username, must be alphanumeric.")

    def sendData(self, data: str) -> None:
        """A function to send data strings to player 2.

        Args:
            data: a string to be sent to player 2 using sockets."""
        self.p1socket.sendall(data.encode())

    def receiveData(self) -> str:
        """A function to receive data from player 2.

        Returns:
            a string sent by player 2 using sockets."""
        return self.p1socket.recv(1024).decode()

    def clearWindow(self) -> None:
        """A function to clear the window of all connection and username GUI."""
        self.prompt.destroy()
        self.ipLabel.destroy()
        self.ipEntry.destroy()
        self.portLabel.destroy()
        self.portEntry.destroy()
        self.connectButton.destroy()
        self.connectLabel.destroy()

        self.usernameEntryMessage.destroy()
        self.usernameEntry.destroy()
        self.usernameButton.destroy()
        self.usernameLabel.destroy()

    def gameboardUI(self) -> None:
        """A function to set up the gameboard.

        Resets the gameboard that stores move data and uses the canvas to draw the lines and labels."""
        p1board.resetGameBoard()
        p1board.updateGamesPlayed()

        self.canvas = tk.Canvas(self.win, width=500, height=500, bg='light blue') # create canvas
        self.canvas.pack()

        self.currentplayer = tk.StringVar(self.win)
        self.currentplayerLabel = tk.Label(self.canvas, bg='light blue', textvariable=self.currentplayer)
        self.currentplayerLabel.place(x=250, y=5, anchor='n')
        self.currentplayer.set(f"{self.p1username}'s turn")

        self.movePrompt = tk.StringVar(self.win)
        self.moveLabel = tk.Label(self.canvas, bg='light blue', textvariable=self.movePrompt)
        self.moveLabel.place(x=100, y=50)
        self.movePrompt.set("Click a space to make a move:")

        self.canvas.create_line(200, 100, 200, 400, width=5) #left down
        self.canvas.create_line(300, 100, 300, 400, width=5) #right down
        self.canvas.create_line(100, 200, 400, 200, width=5) #top across
        self.canvas.create_line(100, 300, 400, 300, width=5) #bottom across

        self.createButtons()

    def createButtons(self) -> None:
        """A function to create the buttons for each space on the gameboard and adds them to a button dictionary to keep
        track."""
        self.buttondict = {}

        self.button1 = tk.Button(self.canvas, command=lambda: self.player1move(1, (115, 115)), height=4, width=9)
        self.button1.place(x=115, y=115)
        self.buttondict[1] = self.button1

        self.button2 = tk.Button(self.canvas, command=lambda: self.player1move(2, (215, 115)), height=4, width=9)
        self.button2.place(x=215, y=115)
        self.buttondict[2] = self.button2

        self.button3 = tk.Button(self.canvas, command=lambda: self.player1move(3, (315, 115)), height=4, width=9)
        self.button3.place(x=315, y=115)
        self.buttondict[3] = self.button3

        self.button4 = tk.Button(self.canvas, command=lambda: self.player1move(4, (115, 215)), height=4, width=9)
        self.button4.place(x=115, y=215)
        self.buttondict[4] = self.button4

        self.button5 = tk.Button(self.canvas, command=lambda: self.player1move(5, (215, 215)), height=4, width=9)
        self.button5.place(x=215, y=215)
        self.buttondict[5] = self.button5

        self.button6 = tk.Button(self.canvas, command=lambda: self.player1move(6, (315, 215)), height=4, width=9)
        self.button6.place(x=315, y=215)
        self.buttondict[6] = self.button6

        self.button7 = tk.Button(self.canvas, command=lambda: self.player1move(7, (115, 315)), height=4, width=9)
        self.button7.place(x=115, y=315)
        self.buttondict[7] = self.button7

        self.button8 = tk.Button(self.canvas, command=lambda: self.player1move(8, (215, 315)), height=4, width=9)
        self.button8.place(x=215, y=315)
        self.buttondict[8] = self.button8

        self.button9 = tk.Button(self.canvas, command=lambda: self.player1move(9, (315, 315)), height=4, width=9)
        self.button9.place(x=315, y=315)
        self.buttondict[9] = self.button9

    def player1move(self, space, coord):
        """A function to initiate player 1's turn after a button on the gameboard is pressed.

        After the player clicks where they want to move, the button is destroyed, an X is drawn, and the gameboard data
        is updated. The board is checked for wins and ties."""
        # removes button from board
        self.buttondict[space].destroy()
        del self.buttondict[space]

        # draws X
        self.canvas.create_text(coord[0]+35, coord[1]+35, text=f"{self.p1symbol}", fill="cornflower blue",
            font=('Helvetica 60 bold'))

        # updates gameboard
        p1board.updateGameBoard(p1board.decodeMove(space), self.p1symbol)

        # sends move to player2
        self.sendData(str(space))

        if self.checkBoard("X") == "tie":
            self.endGame("tie")
        elif self.checkBoard("X") == "win":
            self.endGame("win")
        else:
            # starts player 2's turn
            self.player2move()

    def player2move(self) -> None:
        """A function to initiate player 2's turn after a button on the gameboard is pressed.

        After the player clicks where they want to move, the button is destroyed, an X is drawn, and the gameboard data
        is updated. The board is checked for wins and ties."""
        self.currentplayer.set(f"{self.p2username}'s turn")
        self.movePrompt.set(f"Waiting for {self.p2username} to make a move...")

        # disables buttons
        for button in self.buttondict:
            self.buttondict[button]["state"] = "disabled"

        # receives player 2's move
        self.win.update_idletasks()
        space = int(self.receiveData())

        # removes button to draw O on the board
        self.buttondict[space].destroy()
        del self.buttondict[space]
        p1board.updateGameBoard(p1board.decodeMove(space), self.p2symbol)
        coord = p1board.spaceToCoords(space)
        self.canvas.create_text(coord[0] + 35, coord[1] + 35, text=f"{self.p2symbol}", fill="pale violet red",
                                font=('Helvetica 60 bold'))

        # checks gameboard for losses or ties
        if self.checkBoard("O") == "tie":
            self.endGame("tie")
        elif self.checkBoard("O") == "loss":
            self.endGame("loss")
        else:
            # starts player 1's turn
            self.currentplayer.set(f"{self.p1username}'s turn")
            self.movePrompt.set("Click a space to make a move:")
            for button in self.buttondict:
                self.buttondict[button]["state"] = "normal"

    def checkBoard(self, symbol) -> str or bool:
        """A function that uses isWinner() and BoardIsFull() to check the gameboard for wins, losses, or ties.
        If any of the 3 endgame outcomes is found, a string is returned. If there is no result found from the board,
        False is returned.

        Args:
            symbol: the symbol of the player who just made a move

        Returns:
            a string containing the result of the game or False if no result has been found"""
        if p1board.isWinner(symbol) is True:
            if symbol == self.p1symbol:
                return "win"
            elif symbol == self.p2symbol:
                return "loss"
        elif p1board.boardIsFull() is True:
            return "tie"
        else:
            return False

    def endGame(self, outcome) -> None:
        """A function to set up the GUI after a game has ended.

        Prints the result on the screen and prompts the user if they want to play again.

        Args:
            outcome: a string that is either win, loss, or tie to specify the result of the game."""
        self.movePrompt.set(" ")

        self.outcomePrompt = tk.StringVar(self.win)
        self.outcomeLabel = tk.Label(self.canvas, bg='light blue', textvariable=self.outcomePrompt)
        self.outcomeLabel.place(x=250, y=50, anchor='n')

        if outcome == "win":
            p1board.num_wins += 1
            self.outcomePrompt.set("You Win!")
        elif outcome == "loss":
            p1board.num_losses += 1
            self.outcomePrompt.set("You Lose")
        elif outcome == "tie":
            self.outcomePrompt.set("Tie Game")

        self.playAgainPrompt = tk.Label(self.canvas, bg='light blue', text="Play Again?")
        self.playAgainPrompt.place(x=250, y=415, anchor="n")

        self.playAgainYes = tk.Button(self.win, text='Yes', width=5, command=lambda: self.playAgain("yes"))
        self.playAgainYes.place(x=180, y=450)

        self.playAgainNo = tk.Button(self.win, text='No', width=5, command=lambda: self.playAgain("no"))
        self.playAgainNo.place(x=275, y=450)

    def playAgain(self, answer) -> None:
        """A function to send data to player 2 after player 1 decides to play again or not. Calls resetGUI with the
        answer to set up the gameboard to print stats or start a new game."""
        if answer == "yes":
            self.sendData("Play Again")
            self.win.after(2000, self.resetGUI(True))
        elif answer == "no":
            self.sendData("Fun Times")
            self.win.after(2000, self.resetGUI(False))

    def resetGUI(self, playAgain) -> None:
        """A function to clear the canvas of all elements. If player 1 decided to play again, gameboardUI is called to
        setup a new game. If the player decided to end the game, displayStats is called.
        """
        self.canvas.delete("all")
        for button in self.buttondict:
            self.buttondict[button].destroy()
        self.buttondict.clear()
        self.outcomeLabel.destroy()
        self.playAgainPrompt.destroy()
        self.playAgainYes.destroy()
        self.playAgainNo.destroy()
        self.currentplayerLabel
        self.canvas.destroy()

        if playAgain is False:
            self.displayStats()
        elif playAgain is True:
            self.gameboardUI()

    def displayStats(self) -> None:
        """A function to display the game statistics in the window.
        """
        gameStatsLabel = tk.Label(self.win, bg='light blue', text="Game Statistics")
        gameStatsLabel.place(x=250, y=50, anchor="n")
        numGamesLabel = tk.Label(self.win, bg='light blue', text=f"Number of Games: {p1board.computeStats()[2]}")
        numGamesLabel.place(x=250, y=150, anchor="n")
        numWinsLabel = tk.Label(self.win, bg='light blue', text=f"Number of Wins: {p1board.computeStats()[3]}")
        numWinsLabel.place(x=250, y=180, anchor="n")
        numLossesLabel = tk.Label(self.win, bg='light blue', text=f"Number of Losses: {p1board.computeStats()[4]}")
        numLossesLabel.place(x=250, y=210, anchor="n")
        numTiesLabel = tk.Label(self.win, bg='light blue', text=f"Number of Ties: {p1board.computeStats()[5]}")
        numTiesLabel.place(x=250, y=240, anchor="n")
        quitButton = tk.Button(self.win, text='Quit', command=quit, width=10)
        quitButton.place(x=250, y=300, anchor='n')

    def runUI(self) -> None:
        """A function to start the Tkinter mainloop."""
        self.win.mainloop()

if __name__ == "__main__":
    p1board = BoardClass(player_symbol="X", other_symbol="O")
    Player1()

