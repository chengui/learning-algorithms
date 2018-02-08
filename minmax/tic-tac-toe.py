#!/usr/bin/env python
# encoding: utf-8

import random
import copy


class Board:
    def __init__(self, size=3):
        self.cubsize = size
        self.markers = [1, -1]
        self.game_over = False
        self.current_player = 0
        self.board = [[0 for i in range(size)] for j in range(size)]

    def __str__(self):
        disp = lambda i: {-1: 'o', 0: '-', 1: 'x'}.get(i, '-')
        return '\n'.join(['\t'.join(map(disp, i)) for i in self.board])

    def isGameOver(self):
        return self.game_over

    def currentPlayer(self):
        return self.current_player

    def chkGameOver(self):
        for i in range(self.cubsize):
            s = 0
            for j in range(self.cubsize):
                s += self.board[i][j]
            if abs(s) == self.cubsize:
                return True

        for i in range(self.cubsize):
            s = 0
            for j in range(self.cubsize):
                s += self.board[j][i]
            if abs(s) == self.cubsize:
                return True

        s = 0
        for i in range(self.cubsize):
            s += self.board[i][i]
        if abs(s) == self.cubsize:
            return True

        s = 0
        for i in range(self.cubsize):
            s += self.board[i][self.cubsize - 1 -i]
        if abs(s) == self.cubsize:
            return True

        if not self.getMoves():
            self.current_player = None
            return True

        return False

    def getMoves(self):
        lst = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    lst.append((i, j))
        return lst

    def makeMove(self, player, move):
        if not move:
            return False

        if move[0] >= self.cubsize or move[1] >= self.cubsize:
            return False

        if self.currentPlayer() != player:
            print('it is not your turn!')
            return False

        if self.board[move[0]][move[1]] != 0:
            print('it is occupied!')
            return False

        self.board[move[0]][move[1]] = self.markers[player]

        if self.chkGameOver():
            self.game_over = True
        else:
            self.current_player = (self.current_player + 1) % 2

        return True

    def copyBoard(self):
        return copy.deepcopy(self)

    def evaluate(self, player):
        if not self.game_over or self.current_player is None:
            return 0

        if self.current_player == player:
            return 10
        else:
            return -10


def minmax(board, player):
    if board.isGameOver():
        return board.evaluate(player), None

    bestMove = None
    curr_player = board.currentPlayer()
    if curr_player == player:
        bestScore = -float('inf')
    else:
        bestScore = float('inf')

    for move in board.getMoves():
        newBoard = board.copyBoard()
        newBoard.makeMove(curr_player, move)
        score, _ = minmax(newBoard, player)
        if curr_player == player:
            if score > bestScore:
                bestScore = score
                bestMove = move
        else:
            if score < bestScore:
                bestScore = score
                bestMove = move

    return bestScore, bestMove


def negamax(board, player):
    if board.isGameOver():
        return board.evaluate(player), None

    bestMove = None
    bestScore = -float('inf')

    for move in board.getMoves():
        newBoard = board.copyBoard()
        newBoard.makeMove(board.currentPlayer(), move)
        score, _ = negamax(newBoard, player)
        score = -score

        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestScore, bestMove


def main(mode='minmax'):
    if mode == 'random':
        random.seed(None)

    board = Board()
    while True:
        if board.isGameOver():
            print(board)
            print('Winner: ', board.currentPlayer())
            break
        print(board)
        loc_str = raw_input('please take your turn: ')
        if not loc_str:
            print('quit..')
            break
        (x, y) = map(int, loc_str.split())
        if not board.makeMove(0, (x, y)):
            continue
        # moves = board.getMoves()
        # if moves:
            # move = moves[random.randint(0, len(moves)-1)]
            # board.makeMove(1, move)
        score, move = minmax(board, 1)
        if move:
            board.makeMove(1, move)


if __name__ == '__main__':
    main()
