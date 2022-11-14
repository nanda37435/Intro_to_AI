import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
        self.depth = depth
        super(MinimaxPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def fetch_good_move(self, board, legalMoves, curr_depth, curr_symbol):
        if not legalMoves:
            #new_symbol = 'o' if curr_symbol == 'x' else 'x'
            return [None, self.h1(board)]
        
        if self.depth == curr_depth:
            if curr_depth % 2:
                max_move = -10000000
                for curr_move in legalMoves:
                    new_board = game_rules.makeMove(board, curr_move)
                    #new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    temp = self.h1(new_board)
                    if temp > max_move:
                        max_move = temp
                return [None, max_move]

            else:
                min_move = 10000000
                for curr_move in legalMoves:
                    new_board = game_rules.makeMove(board, curr_move)
                    #new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    temp = self.h1(new_board)
                    if temp < min_move:
                        min_move = temp
                return [None, min_move]

        else:
            # maximizer
            if curr_depth % 2:
                max_move = [None, -10000000]
                for each_move in legalMoves:
                    new_board = game_rules.makeMove(board, each_move)
                    new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    new_board_legal_moves = game_rules.getLegalMoves(new_board, new_symbol)

                    temp = self.fetch_good_move(new_board, new_board_legal_moves, curr_depth+1, new_symbol)

                    if temp[1] > max_move[1]:
                        max_move = [each_move, temp[1]]

                return max_move

            else:
                min_move = [None, 1000000]
                for each_move in legalMoves:
                    new_board = game_rules.makeMove(board, each_move)
                    new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    new_board_legal_moves = game_rules.getLegalMoves(new_board, new_symbol)

                    temp = self.fetch_good_move(new_board, new_board_legal_moves, curr_depth+1, new_symbol)

                    if temp[1] < min_move[1]:
                        min_move = [each_move, temp[1]]

                return min_move

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        curr_depth = 1
        if legalMoves:
            if len(legalMoves) == 1:
                return legalMoves[0]
            else:
                good_move = self.fetch_good_move(board, legalMoves, curr_depth, self.symbol)
                return good_move[0]
        else:
            return None



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth):
        self.depth = depth
        super(AlphaBetaPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def find_good_move(self, board, legalMoves, curr_depth, curr_symbol, alpha, beta):
        if not legalMoves:
            #new_symbol = 'o' if curr_symbol == 'x' else 'x'
            return [None, self.h1(board)]
        
        if self.depth == curr_depth:
            if curr_depth % 2:
                max_move = -10000000
                for curr_move in legalMoves:
                    new_board = game_rules.makeMove(board, curr_move)
                    #new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    temp = self.h1(new_board)
                    if temp > max_move:
                        max_move = temp

                    if temp > alpha:
                        alpha = temp

                    if alpha >= beta:
                        break

                return [None, max_move]

            else:
                min_move = 10000000
                for curr_move in legalMoves:
                    new_board = game_rules.makeMove(board, curr_move)
                    #new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    temp = self.h1(new_board)
                    if temp < min_move:
                        min_move = temp

                    if temp < beta:
                        beta = temp

                    if alpha >= beta:
                        break
                return [None, min_move]

        else:
            if curr_depth % 2:
                max_move = [None, -10000000]
                for each_move in legalMoves:
                    new_board = game_rules.makeMove(board, each_move)
                    new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    new_board_legal_moves = game_rules.getLegalMoves(new_board, new_symbol)

                    temp = self.find_good_move(new_board, new_board_legal_moves, curr_depth+1, new_symbol, alpha, beta)

                    if temp[1] > max_move[1]:
                        max_move = [each_move, temp[1]]

                    if temp[1] > alpha:
                        alpha = temp[1]

                    if alpha >= beta:
                        break

                return max_move

            else:
                min_move = [None, 1000000]
                for each_move in legalMoves:
                    new_board = game_rules.makeMove(board, each_move)
                    new_symbol = 'o' if curr_symbol == 'x' else 'x'
                    new_board_legal_moves = game_rules.getLegalMoves(new_board, new_symbol)

                    temp = self.find_good_move(new_board, new_board_legal_moves, curr_depth+1, new_symbol, alpha, beta)

                    if temp[1] < min_move[1]:
                        min_move = [each_move, temp[1]]

                    if beta < temp[1]:
                        beta = temp[1]

                    if alpha >= beta:
                        break

                return min_move

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        curr_symbol = self.symbol
        curr_depth = 1
        if legalMoves:
            if len(legalMoves) == 1:
                return legalMoves[0]
            else:
                good_move = self.find_good_move(board, legalMoves, curr_depth, curr_symbol, NEG_INF, POS_INF)
                return good_move[0]
        return None
    

class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
