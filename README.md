# isola_python

Isola is a game played on a 7x7 grid. Each player starts on the center square of opposing edges of the grid. On a player's turn, that player moves one space orthogonally or diagonally and then destroys a square of the board, making it impassible terrain forever. The destroyed square does not need to be adjacent to the player. The destroyed square must be an un-destroyed square, and cannot be the current location of either player. If a player cannot make a move, that player loses and the other player wins.

Students create a child class of isola_player (in isola_game.py) which can play the game autonomously, and the bots play against one another.