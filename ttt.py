import tkinter as tk
from tkinter import messagebox
import socket

MainWindow = tk.Tk()

def closeMenu():
    global MainWindow
    MainWindow.destroy()

def showMenu():
    global MainWindow

    lbl_gamesize = tk.Label(MainWindow)
    txt_gamesize = tk.Entry(MainWindow)
    btn_KI = tk.Button(MainWindow)
    lbl_player = tk.Label(MainWindow)
    btn_newGame = tk.Button(MainWindow)
    btn_join = tk.Button(MainWindow)
    lbl_IP = tk.Label(MainWindow)
    txt_IP = tk.Entry(MainWindow)
    btn_exit = tk.Button(MainWindow)

    lbl_gamesize["text"] = "Spielfeldgröße"
    btn_KI["text"] = "Gegen KI"
    lbl_player["text"] = "Gegen anderen Spieler"
    btn_newGame["text"] = "Neues Spiel starten"
    btn_join["text"] = "an Spiel teilnehmen"
    lbl_IP["text"] = "IP Adresse"
    btn_exit["text"] = "Beenden"
    txt_gamesize.insert(0, "3")

    btn_exit["command"] = closeMenu

    lbl_gamesize.grid(row=0, column=0)
    txt_gamesize.grid(row=0, column=1)
    btn_KI.grid(row=1, column=1)
    lbl_player.grid(row=2, column=0)
    btn_newGame.grid(row=2, column=1)
    btn_KI.grid(row=3, column=1)
    lbl_IP.grid(row=4, column=0)
    txt_IP.grid(row=4, column=1)
    btn_exit.grid(row=5, column=1)

    MainWindow.mainloop()

if __name__ == '__main__':
    print("Hi")
    showMenu()
