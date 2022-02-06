# %%
from utils_2048 import add_two, reverse, transpose, cover_up, merge

# %%
class GameState:
    """ Simple version of the 2048 board with moves, processing, and point system available.
        Use this class to pair with MCTS algorithm. """

    def __init__(self, mat):
        self.matrix = mat
        self.point_count = 0

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
        add_points = temp[2]
        return game, done, add_points

    def down(self):
        game = self.matrix
        game = reverse(transpose(game))
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(reverse(game))
        add_points = temp[2]
        return game, done, add_points

    def left(self):
        game = self.matrix
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        add_points = temp[2]
        return game, done, add_points

    def right(self):
        game = self.matrix
        game = reverse(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = reverse(game)
        add_points = temp[2]
        return game, done, add_points

    def clone(self):
        st = GameState(self.matrix)
        st.point_count = self.point_count
        return st
    
    def do_move(self, move):
        """ Move input should be one of the following: "up", "down", "left", "right"
            Make sure when this function is called, the move is a possible move. """
        move_funcs = {
            'up':       self.up(),
            'down':     self.down(),
            'left':     self.left(),
            'right':    self.right()
        }

        self.matrix, _, add_points = move_funcs[move]
        self.point_count += add_points # Update Points
        
        # Check if there any zeros in the grid.
        zero_exists = False
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    zero_exists = True
                    break
        
        if zero_exists:
            self.matrix = add_two(self.matrix) # Add 2 or 4 in the matrix
            game_over = self.game_state() != 'not over'
            return game_over 
        else:
            game_over = True
            return game_over 
        
    def get_moves(self):
        """ Get all possible moves from this state. """
        _, done_up, _     = self.up()
        _, done_down, _   = self.down()
        _, done_left, _   = self.left()
        _, done_right, _  = self.right()

        move_possible = []
        if done_up:
            move_possible.append("up")
        if done_down:
            move_possible.append("down")
        if done_left:
            move_possible.append("left")
        if done_right:
            move_possible.append("right")
        
        return move_possible

    def get_result(self):
        """ Get the score of the given state."""
        return self.point_count

# %%
if __name__ == "__main__":
    initialMat = [[4,2,4,0],[0,0,4,0],[0,2,0,0],[8,0,2,0]]
    deathMatrix = [[8, 4, 2, 8], [2, 16, 8, 4], [256, 32, 4, 2], [4, 2, 4, 2]]
