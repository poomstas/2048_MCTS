# %%
from utils_2048 import add_two, reverse, transpose, cover_up, merge

# %%
class GameState:
    """ Simple version of the 2048 board with moves, processing, and point system available.
        Use this class to pair with MCTS algorithm. """
    def __init__(self, mat):
        self.matrix = mat
        self.pointCount = 0

    def __str__(self):
        s = ""
        for i in range(4):
            for j in range(4):
                s += "\t"
                s += str(self.matrix[i][j])
                if j == 3:
                    s += "\n"
        return s

    def game_state(self):
        mat = self.matrix
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]==2048:
                    return 'win'
        for i in range(len(mat)-1): # Intentionally reduced to check the row on the right and below
            for j in range(len(mat[0])-1): # More elegant to use exceptions but most likely this will be their solution
                if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                    return 'not over'
        for i in range(len(mat)): # Check for any zero entries
            for j in range(len(mat[0])):
                if mat[i][j]==0:
                    return 'not over'
        for k in range(len(mat)-1): # To check the left/right entries on the last row
            if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
                return 'not over'
        for j in range(len(mat)-1): # Check up/down entries on last column
            if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
                return 'not over'
        return 'lose'

    # Done indicates whether the move does anything
    def up(self):
        game = self.matrix
        game = transpose(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(game)
        addPoints = temp[2]
        return game, done, addPoints

    def down(self):
        game = self.matrix
        game = reverse(transpose(game))
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(reverse(game))
        addPoints = temp[2]
        return game, done, addPoints

    def left(self):
        game = self.matrix
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        addPoints = temp[2]
        return game, done, addPoints

    def right(self):
        game = self.matrix
        game = reverse(game)
        game,done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = reverse(game)
        addPoints = temp[2]
        return game, done, addPoints

    def clone(self):
        st = GameState(self.matrix)
        st.pointCount = self.pointCount
        return st
    
    def do_move(self, move):
        """ Move input should be one of the following: "up", "down", "left", "right"
            Make sure when this function is called, the move is a possible move. """
        moveFuncs = {
            'up':       self.up(),
            'down':     self.down(),
            'left':     self.left(),
            'right':    self.right()
        }

        self.matrix, _, addPoints = moveFuncs[move]
        self.pointCount += addPoints # Update Points
        
        # Check if there any zeros in the grid.
        zeroExists = False
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    zeroExists = True
                    break
        
        if zeroExists:
            self.matrix = add_two(self.matrix) # Add 2 or 4 in the matrix
            gameOver = self.game_state() != 'not over'
            return gameOver 
        else:
            gameOver = True
            return gameOver 
        
    def get_moves(self):
        """ Get all possible moves from this state. """
        _, doneUp, _     = self.up()
        _, doneDown, _   = self.down()
        _, doneLeft, _   = self.left()
        _, doneRight, _  = self.right()

        movePossible = []
        if doneUp:
            movePossible.append("up")
        if doneDown:
            movePossible.append("down")
        if doneLeft:
            movePossible.append("left")
        if doneRight:
            movePossible.append("right")
        
        return movePossible

    def get_result(self):
        """ Get the score of the given state.
        """
        return self.pointCount

# %%
if __name__ == "__main__":
    initialMat = [[4,2,4,0],[0,0,4,0],[0,2,0,0],[8,0,2,0]]
    deathMatrix = [[8, 4, 2, 8], [2, 16, 8, 4], [256, 32, 4, 2], [4, 2, 4, 2]]
