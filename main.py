from Game import Game
from GameState import GameState
from Player import PlayerRandom, PlayerHuman
from tqdm import tqdm

player0 = PlayerRandom()
player1 = PlayerRandom()

n = 500
gameLengths = [None] * n

for i in tqdm(range(n)):
    game = Game(player0= player0, player1= player1, isVerbose= False, gameState=GameState())
    game.run()
    gameLengths[i] = game.CurrentGameState.MoveCount

print(f"average game length : {sum(gameLengths)/len(gameLengths)}")

# game = Game(player0= player0, player1= player1, isVerbose=True)
# game.run()