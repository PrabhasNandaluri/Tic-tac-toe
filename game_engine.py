from random import randint
import copy
from dataclasses import dataclass

@dataclass()
class Game_state:
    board = [ [0,0,0],
              [0,0,0],
              [0,0,0] ]
    turn : str = "player" if randint(0, 9) % 2 == 0 else "bot"
    winner : str= None
    won : bool= False
    player : int = 1
    bot : int = -1
    Diagonals = [[(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]
    Rows = [[(0,0), (0,1), (0,2)],[(1,0), (1,1), (1,2)],[(2,0), (2,1), (2,2)]]
    Columns = [[(0,0), (1,0), (2,0)],[(0,1), (1,1), (2,1)],[(0,2), (1,2), (2,2)]]
    checking_list = [Columns, Rows, Diagonals]

def win(board : list, checking_list : list) -> str:
  winner :str = None
  for item in checking_list:
    for pos in item:
      if board[pos[0][0]][pos[0][1]] == board[pos[1][0]][pos[1][1]] == board[pos[2][0]][pos[2][1]] != 0:
        winner = "player" if board[pos[0][0]][pos[0][1]] == 1 else "bot"
        break
  return winner

def playerinput() -> tuple:
  x = int(input("Value x : "))
  y = int(input("Value y : "))
  return (x, y)

def valid(board : list, move : tuple) -> bool:
  return True if board[move[0]][move[1]] == 0 and move[0] < 3 and move[1] < 3 and move[0] >= 0 and move[1] >=0 else False

def empty_squares_count(board : tuple) -> int:
  count : int = 0
  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        count = count + 1
  return count

def empty_sqaures_list(board : tuple) -> list:
  empty_list : list =[]
  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        empty_list.append((i, j))
  return empty_list

def update(board : list, playedby : str , move : tuple):
  board[move[0]][move[1]] = game.player if playedby == "player" else game.bot

class AI:
  def __init__(self) -> None:
    self.cross = [(0, 0) , (0, 2), (2, 0), (0, 2)]
    self.plus = [(0, 1), (2, 1), (1, 0), (1, 2)]

  def move(self, board : list , i : int) -> tuple:
    if i == 0:
      return (0, 0)
    return self._minimax(board, True)[1]

  def _minimax(self, board : list, maximize : bool):
    empty_squares = empty_squares_count(board)
    winner = win(board, game.checking_list)
    if empty_squares == 0 and winner == None:
      return 0, None
    
    if empty_squares > 0 and winner == "player":
      return -1 * (empty_squares + 1), None
    
    if empty_squares > 0 and winner == "bot":
      return 1 * (empty_squares + 1), None

    if maximize:
      max_score : int = -100
      best_move : tuple = None
      empty_sqaures : list = empty_sqaures_list(board)

      for pos in empty_sqaures:
        temp_board = copy.deepcopy(board)
        update(temp_board, "bot", pos)
        eva = self._minimax(temp_board, False)[0]
        if eva > max_score:
          max_score = eva
          best_move = pos 
      return max_score, best_move

    elif not maximize:
      min_score : int = 100
      best_move : tuple = None
      empty_sqaures : list = empty_sqaures_list(board)

      for pos in empty_sqaures:
        temp_board = copy.deepcopy(board)
        update(temp_board, "player", pos)
        eva = self._minimax(temp_board, True)[0]
        if eva < min_score:
          min_score = eva
          best_move = pos
      return min_score, best_move


game = Game_state()

