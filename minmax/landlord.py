#!/usr/bin/env python
# encoding: utf-8

class Player:
    def __init__(self, name):
        self.name = name
        self.board = None
        self.cards = None

    def __str__(self):
        return self.name

    def setCards(self, cards):
        self.cards = cards

    def emptyCards(self):
        return len(self.cards) == 0

    def getAvailableMoves(self, cards):
        return filter(lambda i: i > cards[0], self.cards)

    def handOut(self, cards):
        self.board.turn(cards)
        for card in cards:
            self.cards.remove(card)


class Board:
    def __init__(self):
        self.current = 0
        self.players = []
        self.records = []

    def __str__(self):
        s = ''
        for player in self.players:
            s += '%s: %s\n' % (player, player.cards)
        s += 'Records: %s' % self.records
        return s

    def join(self, player):
        self.players.append(player)
        player.board = self

    def turn(self, cards):
        self.records.append(cards)
        self.current = (self.current + 1) % len(self.players)

    def currentPlayer(self):
        return self.players[self.current]

    def isGameOver(self):
        for player in self.players:
            if player.emptyCards():
                return True
        return False


def main():
    board = Board()

    playerA = Player('A')
    playerB = Player('B')

    playerA.setCards(['1', '2', '3'])
    playerB.setCards(['1', '2', '3'])

    board.join(playerA)
    board.join(playerB)

    while True:
        if board.isGameOver():
            print('Winner: %s' % board.currentPlayer())
            break
        print(board)

        cards_str = raw_input('please take your turn: ')
        if not cards_str:
            print('quit..')
            break

        cards = cards_str.split()
        print(cards)
        playerA.handOut(cards)

        moves = playerB.getAvailableMoves(cards)
        if moves:
            playerB.handOut([moves[0]])
        else:
            playerB.handOut([])


main()
