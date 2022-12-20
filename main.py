import sys

import pygame
from pygame.locals import *
from game_engine import Game_state
import game_engine
pygame.init()

state = Game_state()
fps = 60
fpsClock = pygame.time.Clock()

BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

BLOCK_SIZE = 75

width, height = 325, 400
screen = pygame.display.set_mode((width, height))

def game_board():
  for i in range(2):
    pygame.draw.line(screen, WHITE, ((i + 1)* BLOCK_SIZE + 50, 50), ((i + 1) * BLOCK_SIZE + 50, 3 * BLOCK_SIZE + 50), 2)
    pygame.draw.line(screen, WHITE, (50, 50 + (i + 1) * BLOCK_SIZE), (3 * BLOCK_SIZE  + 50, 50 + (i + 1) * BLOCK_SIZE), 2)


def X(x : int, y : int) -> None:
  pygame.draw.line(screen, GREEN, (BLOCK_SIZE * y + 50, BLOCK_SIZE * x + 50) ,((y + 1) * BLOCK_SIZE + 50, (x + 1) * BLOCK_SIZE + 50))
  pygame.draw.line(screen, GREEN, (BLOCK_SIZE * (y + 1) + 50, BLOCK_SIZE * x + 50) ,(y * BLOCK_SIZE + 50, (x + 1) * BLOCK_SIZE + 50))

def O(x : int, y : int) -> None:
  pygame.draw.circle(screen, (255, 0, 0), (y * BLOCK_SIZE + 88, x * BLOCK_SIZE  + 88), 35, 2)


board = Game_state.board
turn = Game_state.turn
bot = game_engine.AI()

moves = 0
while moves <= 9:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  game_board()

  for i in range(3):
    for j in range(3):
      if board[i][j] == 1:
        X(i, j)
      elif board[i][j] == -1:
        O(i, j)
  
  if turn == "bot":
    move = bot.move(board, moves)
    game_engine.update(board, turn, move)
    turn = "player"
    moves += 1
  
  elif turn == "player":
    left = pygame.mouse.get_pressed()[0]
    if left:
      x_pos, y = pygame.mouse.get_pos()
      x = (y - 50)//BLOCK_SIZE
      y = (x_pos - 50)//BLOCK_SIZE
      if x >= 0 and y >=0 and x < 3 and y < 3 and game_engine.valid(board, (x ,y)):
        game_engine.update(board, turn, (x, y))
        turn = "bot"
        moves += 1
  
  if moves > 4:
    winner = game_engine.win(board, Game_state.checking_list)
    if moves == 9:
      font = pygame.font.Font('freesansbold.ttf', 32)
      text = font.render(f'Draw.!', True, GREEN, BLACK)
      textRect = text.get_rect()
      textRect.center = (width//2, 350)
      screen.blit(text, textRect)
    if winner:
      font = pygame.font.SysFont('serif', 30)
      text = font.render(winner, True, GREEN, BLACK)
      textRect = text.get_rect()
      text = font.render(f'yay! {winner} won..!!', True, WHITE)
      textRect.center = (width//2 - 75, 350)
      screen.blit(text, textRect)
  
  pygame.display.flip() 
  fpsClock.tick(fps)