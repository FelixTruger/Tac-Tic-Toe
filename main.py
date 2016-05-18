from functools import partial
# partial enables us to make a function wrapper for buttons

import tkinter as tk
import tkinter.messagebox as tkMsg
import game
import connector as connection
from enum import Enum


class mode(Enum):
    BOT = 1
    SERVER = 2
    CLIENT = 3

MainWindow = tk.Tk()
MainWindow.title("Tac-Tic-Toe")
Buttonsize = 5

# hardcoded port for the client-server connection
port = 5600


def showMap(Gamesize, Gamemode):
    Size = int(Gamesize)
    game.startGame(Gamesize, Gamemode==mode.BOT)
    buttons = [[None for x in range(Size)] for y in range(Size)]
    
    # in case the window was used before, clean it up
    clearWindow(MainWindow)
    
    # add Gamesize*Gamesize buttons in 2 dimensions to MainWindow
    for r in range(Size):
        for c in range(Size):
          state = str(game.getValue(r, c))
          newButton = tk.Button(MainWindow, text=state, borderwidth=1)
          newButton.config(height=Buttonsize, width=Buttonsize);
          newButton.grid(row=r, column=c)
          buttons[r][c] = newButton
          buttons[r][c]["command"] = partial(Move, r, c, buttons, 1, Gamemode) # 1: it's a move of the player on this end
          
    # add Menu button to MainWindow
    def localShowMenu():
        if tkMsg.askyesno("Spiel beenden?", "Möchten Sie das Spiel beenden und in das Menü zurückkehren?"):
            showMenu()
            
    btn_Menu = tk.Button(MainWindow, text='Menü')
    btn_Menu["command"] = localShowMenu
    btn_Menu.config(width=Size*Buttonsize)
    btn_Menu.grid(row=Size, column=0, columnspan=Size)
    MainWindow.update()
    
    if (Gamemode == mode.CLIENT):
        waitForMove(buttons, Gamemode) # Server has the first move

def Move(r, c, buttons, ownmove, Gamemode):
    result = game.setMove(r, c)
    
    # do things only when the move was valid
    if result:        
        # the bot has moved after player, so the field must be refreshed to 
        # display moves made by bot
        if result is 2 or result is 3:
            refresh_field(buttons)
        else: # update only the button that was set by the player
            buttons[r][c]["text"] = game.getValue(r, c)
            
        winner = game.finished()
        if winner:
            if (ownmove and (Gamemode == mode.SERVER or Gamemode == mode.CLIENT)):
                sendMove(r, c) # send move to opponent, so he also knows who won
            try:
                connection.close()

            finally:
                tkMsg.showinfo("Spielende", str(winner) + " hat das Spiel gewonnen!")
                showMenu()

        
        if (ownmove and (Gamemode == mode.SERVER or Gamemode == mode.CLIENT)):
            sendMove(r, c)
            MainWindow.update()
            waitForMove(buttons, Gamemode)
            
            
def waitForMove(buttons, Gamemode):
    global connection
    if connection is None:
        print("Fehler: Warten auf Zug des Gegenspielers nicht möglich. Es besteht keine Verbindung!")
    else:
        message = connection.receive()
        row = int(message.split('#')[0])
        col = int(message.split('#')[1])
        Move(row, col, buttons, 0, Gamemode)

def sendMove(r, c):
    global connection
    if connection is None:
        print("Fehler: Senden des Zuges nicht möglich. Es besteht keine Verbindung!")
    else:
        message = str(r)+'#'+str(c)
        connection.send(message)

def refresh_field(buttons):
    for r in range(game.getSize()):
        for c in range(game.getSize()):
            buttons[r][c]["text"] = game.getValue(r, c)


def closeMenu():
    MainWindow.destroy()

def showMenu():
    global port

    def localStartGame(mode):
        showMap(txt_gamesize.get(), mode)

    def connectClient():
        ip = txt_IP.get()
        global connection
        if (connection.startClient(ip, port)):
            message = "Someone there?"
            connection.send(message)
            print("Client: Sent message: "+message)
            print("Client: Received message: "+str(connection.receive()))
            showMap(txt_gamesize.get(), mode.CLIENT)
        else:
            print("Connection failed.")
    
    def connectServer():
        global connection
        if (connection.startServer(port)):
            message = str(connection.receive())
            if message:
                print("Server: Received message: "+message)
                message = "Acknowledged!"
                connection.send(message)
                print("Server: Sent message: "+message)
                showMap(txt_gamesize.get(), mode.SERVER)
        else:
            print("Connection failed.")
                
    # in case the window was used before, clean it up
    clearWindow(MainWindow)


    lbl_gamesize = tk.Label(MainWindow)
    txt_gamesize = tk.Entry(MainWindow)
    btn_KI = tk.Button(MainWindow)
    lbl_player = tk.Label(MainWindow)
    btn_newGame = tk.Button(MainWindow)
    btn_join = tk.Button(MainWindow)
    lbl_IP = tk.Label(MainWindow)
    txt_IP = tk.Entry(MainWindow)
    btn_exit = tk.Button(MainWindow)
    lbl_KI = tk.Label(MainWindow)

    lbl_gamesize["text"] = "Spielfeldgröße"
    btn_KI["text"] = "Neues Spiel starten"
    lbl_player["text"] = "Gegen anderen Spieler"
    btn_newGame["text"] = "Neues Spiel starten"
    btn_join["text"] = "an Spiel teilnehmen"
    lbl_IP["text"] = "IP Adresse"
    btn_exit["text"] = "Beenden"
    txt_gamesize.insert(0, "3")
    lbl_KI["text"] = "Gegen KI"

    btn_exit["command"] = closeMenu
    btn_KI["command"] = partial(localStartGame, mode.BOT) # 1 means to use bot as opponent
    btn_newGame["command"] = connectServer
    btn_join["command"] = connectClient

    lbl_gamesize.grid(row=0, column=0)
    txt_gamesize.grid(row=0, column=1)
    lbl_KI.grid(row=1, column=0)
    btn_KI.grid(row=1, column=1)
    lbl_player.grid(row=2, column=0)
    btn_newGame.grid(row=2, column=1)
    btn_join.grid(row=3, column=1)
    lbl_IP.grid(row=4, column=0)
    txt_IP.grid(row=4, column=1)
    btn_exit.grid(row=5, column=1)

    MainWindow.mainloop()

def clearWindow(tkWindow):
	# remove everything from MainWindow
    for widget in tkWindow.winfo_children():
      widget.destroy()

if __name__ == '__main__':
    print("Tac-Tic-Toe  Copyright (C) 2016  Felix & Hagen\n\
    This program comes with ABSOLUTELY NO WARRANTY; for details see GPL.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; see GPL for details.")
    showMenu()