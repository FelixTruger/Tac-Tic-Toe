from functools import partial
# partial enables us to make a function wrapper for buttons

import tkinter as tk
import tkinter.messagebox as tkMsg
import game
import connector

MainWindow = tk.Tk()
Buttonsize = 5;

def showMap(Gamesize, bot):
    Size = int(Gamesize)
    game.startGame(Gamesize, int(bot))
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
          buttons[r][c]["command"] = partial(Move, r, c, buttons)
          
    # add Menu button to MainWindow
    def localShowMenu():
        if tkMsg.askyesno("Spiel beenden?", "Möchten Sie das Spiel beenden und in das Menü zurückkehren?"):
            showMenu()
            
    btn_Menu = tk.Button(MainWindow, text='Menü')
    btn_Menu["command"] = localShowMenu
    btn_Menu.config(width=Size*Buttonsize)
    btn_Menu.grid(row=Size, column=0, columnspan=Size) 

def Move(r, c, buttons):
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
            tkMsg.showinfo("Spielende", str(winner)+" hat das Spiel gewonnen!")
            showMenu()

def refresh_field(buttons):
    for r in range(game.getSize()):
        for c in range(game.getSize()):
            buttons[r][c]["text"] = game.getValue(r, c)


def closeMenu():
    MainWindow.destroy()

def showMenu():
    def localStartGame(bot):
        showMap(txt_gamesize.get(), int(bot))

    # hardcoded port for the client-server connection
    port = 5600

    def connectClient():
        ip = txt_IP.get()
        connector.startClient(ip, port)
        
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
    btn_KI["command"] = partial(localStartGame, 1) # 1 means to use bot as opponent
    btn_newGame["command"] = partial(connector.startServer, port)
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