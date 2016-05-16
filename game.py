from array import *
import random

field = [[]]
player = 'X' # x begins the game
Size = 0
bot = 0

# @return 0 if the move was invalid
# @return 1 if the move was valid
# @return 2 if bot has moved
def setMove(r, c):
  global player
  
  # cant move when already set
  if getValue(r, c):
    print(player+" tried an invalid move")
    return 0
  
  # set the move to the field for player
  field[r][c] = player;
  
  print(player+" moved on ["+str(r)+"] ["+str(c)+"]")
  
  # switch player
  if player is 'X':
    player = 'O'
  else:
    player = 'X'
  
  if bot and player is 'O' and not finished():
    botMove()
    print("Bot has moved")
    return 2

  else:
    print(player+" has the next move")
  
  return 1

def getValue(r, c):
  #print("Value read from ["+str(r)+"] ["+str(c)+"]")
  return field[r][c]

def botMove():
  row = random.randint(0, Size-1)
  col = random.randint(0, Size-1)
  
  # retry if move was not valid
  if not setMove(row, col):
    botMove()
    
# @return 0 if game is not finished
# @return else name of player who has won
def finished():
  global Size
  
   # search for rows all the same value
  for row in range(Size):
    current = 'start'
    for col in range(Size):
      val = getValue(row, col)
      if current is 'start' or current is val and val is not '':
        current = getValue(row, col)
        if col is Size-1:
          return current
      else:
        break 
        
  # search for cols all the same value
  for col in range(Size):
    current = 'start'
    for row in range(Size):
      val = getValue(row, col)
      if current is 'start' or current is val and val is not '':
        current = getValue(row, col)
        if row is Size-1:
          return current
      else:
        break 
  
  # search first diagonal for the same value
  current = 'start'
  for cr in range(Size):
    val = getValue(cr, cr)
    if current is 'start' or current is val and val is not '':
      current = getValue(cr, cr)
      if cr is Size-1:
        return current
    else:
      break     
      
  # search second diagonal for the same value
  current = 'start'
  for cr in range(Size):
    val = getValue(cr, Size-1-cr)
    if current is 'start' or current is val and val is not '':
      current = getValue(cr, Size-1-cr)
      if cr is Size-1:
        return current
    else:
      break   
  
  # last but not least: check whether all fields have been set
  for col in range(Size):
    current = 'start'
    for row in range(Size):
      if getValue(row, col) is '':
        return 0  
  
  # all fields set but no return until now? then the game is over without a winner
  return "Keiner der beiden Spieler"

def startGame(Gamesize, usebot):
  global bot
  global Size
  global player
  
  bot = int(usebot)
  Size = int(Gamesize)
  
  print("Game started with size "+str(Size));
  global field 
  field = [['' for x in range(Size)] for y in range(Size)] 
  #print("Field initialized")
  player = 'X';
  print(player+" starts the game")
  
  if bot:
    print("Opponent is bot")
  else:
    print("Opponent is human")
    
def getSize():
  global Size
  return Size

if __name__ == '__main__':
    print("Tac-Tic-Toe Game module Copyright (C) 2016  Felix & Hagen\n\
    This program comes with ABSOLUTELY NO WARRANTY; for details see GPL.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; see GPL for details.")
    print()
    print(">>>>>This module has no functionality on its own!<<<<<")
    print("Run main.py or use this module in another python script by importing it.")
