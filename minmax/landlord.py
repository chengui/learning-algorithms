#!/usr/bin/env python
# encoding: utf-8

import copy
from itertools import combinations


class Card:
    THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE, TWO, BJOKER, RJOKER = range(3, 18)

    @classmethod
    def convert(cls, cards):
        cards_dict = {
            '3': 3, '4': 4,  '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15, 'Y': 16, 'Z': 17
        }
        return map(lambda i: cards_dict.get(i, None), cards)

    @classmethod
    def revert(cls, values):
        values_dict = {
            3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2', 16: 'Y', 17: 'Z'
        }
        return map(lambda i: values_dict.get(i, None), values)


class CardPattern:
    PASS       = -1
    ROCKET     = 0
    BOMB       = 1
    SINGLE     = 2
    PAIR       = 3
    TRIPLE     = 4
    TRIPLE_ONE = 5
    TRIPLE_TWO = 6

    STRIGHT = 10
    QUADS_ONES = 7
    QUADS_PAIRS = 8
    INVALID = float('inf')

class Move:
    def __init__(self, cards, pattern=None, value=None):
        self.cards = cards
        self.pattern = pattern
        self.value = value

    def parse(self):
        cards = self.cards
        if len(cards) == 0:
            self.pattern = CardPattern.PASS
            self.value = -1
            return
        if len(cards) == 1:
            self.pattern = CardPattern.SINGLE
            self.value = cards[0]
            return
        if len(cards) == 2 and Card.BJOKER in cards and Card.RJOKER in cards:
            self.pattern = CardPattern.ROCKET
            self.value = 100
            return
        if len(cards) == 2 and cards.count(cards[0]) == 2:
            self.pattern = CardPattern.PAIR
            self.value = cards[0]
            return
        if len(cards) == 3 and cards.count(cards[0]) == 3:
            self.pattern = CardPattern.TRIPLE
            self.value = cards[0]
            return
        if len(cards) == 4 and cards.count(cards[0]) == 4:
            self.pattern = CardPattern.BOMB
            self.value = cards[0]
            return
        if len(cards) == 4 and len(set(cards)) == 2:
            self.pattern = CardPattern.TRIPLE_ONE
            self. value = cards[0]
            return
        if len(cards) == 5 and len(set(cards)) == 2 and cards.count(cards[0]) == 3:
            self.pattern = CardPattern.TRIPLE_TWO
            self.value = cards[0]
            return
        if len(cards) == 6 and cards.count(cards[0]) == 4:
            self.pattern = CardPattern.QUADS_ONES
            self.value = cards[0]
            return
        if len(cards) == 8 and cards.count(cards[0]) == 4:
            self.pattern = CardPattern.QUADS_PAIRS
            self.value = cards[0]
            return
        if len(cards) >= 5 and (cards[-1] - cards[0]) == len(cards) - 1:
            self.pattern = len(cards) + 2
            self.value = cards[0]
            return
        if len(cards) >= 6 and (cards[-1] - cards[0]) == len(cards) / 2 - 1:
            self.pattern = len(cards) + 12
            self.value = cards[0]
            return
        return CardPattern.INVALID

    def __str__(self):
        return str(Card.revert(self.cards))

    def __repr__(self):
        return 'Move(%s, %d, %d)' % (self.__str__(), self.pattern, self.value)

    def __cmp__(self, o):
        return cmp(sorted(self.cards), sorted(o.cards))

    def __contains__(self, v):
        return v in self.cards

    def __iter__(self):
        return iter(self.cards)


class Board:
    def __init__(self):
        self.current_player = 0
        self.playerA = []
        self.playerB = []
        self.records = []
        self.patterns = []

    def __str__(self):
        s = ''
        s += 'Lord: %s\n' % Card.revert(sorted(self.playerA, reverse=True))
        s += 'Farmer: %s\n' % Card.revert(sorted(self.playerB, reverse=True))
        # s += 'Records: %s\n' % ', '.join(map(str, self.records))
        return s

    def __hash__(self):
        record = self.records and self.records[-1].cards or []
        return hash(str((sorted(self.playerA), sorted(self.playerB), sorted(record))))

    def isGameOver(self):
        return len(self.playerA) == 0 or len(self.playerB) == 0

    def currentPlayer(self):
        return self.current_player

    def makeMove(self, move):
        if not move:
            move = Move([])

        if self.current_player == 0:
            player = self.playerA
        else:
            player = self.playerB

        for i in move:
            player.remove(i)
        self.records.append(move)

        if not self.isGameOver():
            self.current_player = (self.current_player + 1) % 2

    def unmakeMove(self, move):
        if not self.isGameOver():
            self.current_player = (self.current_player + 1) % 2

        if self.current_player == 0:
            player = self.playerA
        else:
            player = self.playerB

        last_move = self.records.pop()
        for i in last_move:
            player.append(i)
        # player = sorted(player)

    def getNextMoves(self):
        if self.records:
            last_move = self.records[-1]
        else:
            last_move = Move([])

        if self.current_player == 0:
            player = self.playerA
        else:
            player = self.playerB

        return getNextMoves(player, last_move.pattern, last_move.value)


def getSequence(cards, length, value, num):
    if len(cards) < length * num:
        return []

    card_count = {}
    for card in cards:
        card_count[card] = card_count.get(card, 0) + 1

    res = []
    seq = []
    for card in sorted(card_count.keys()):
        if (len(seq) == 0 and card > value and card <= Card.ACE and card_count[card] >= num) or \
              (len(seq) != 0 and seq[-1] + 1 == card and card <= Card.ACE and card_count[card] >= num):
            seq = seq + [card] * num
        else:
            seq = [card] * num
        if len(seq) == length * num:
            pattern = -1
            if num == 1:
                pattern = length + 2
            elif num == 2:
                pattern = length + 12
            res.append(Move(copy.deepcopy(seq), pattern, seq[0]))
            seq = seq[num:]
    return res

def getPlane(cards, length, size):
    ans = []
    seq = []
    if len(cards) >= length * 4:
        for card in list(set(cards)):
            if ((len(seq) == 0 and card > size and card < 12 and cards.count(card) >= 3) or
                (len(seq) != 0 and seq[-1] + 1 == card and card < 12 and cards.count(card) >= 3)):
                seq = seq + [card] * 3
            else:
                seq = []
            if len(seq) == length * 3:
                cardBs = list(set(cards) - set(seq))
                for case in list(combinations(cardBs, length)):
                    newSeq = seq + list(case)
                    ans.append({ 'c': newSeq, 'p': length + 26, 's': seq[0] })
                seq = seq[3:]
    return ans

def getNextMoves(cards, pattern, value):
    card_count = {}
    for card in cards:
        card_count[card] = card_count.get(card, 0) + 1

    moves = []
    # Rocket
    if Card.BJOKER in cards and Card.RJOKER in cards:
        moves.append(Move([Card.BJOKER, Card.RJOKER], CardPattern.ROCKET, 100))
    # Bomb
    if pattern != CardPattern.ROCKET:
        for card in card_count:
            if card_count[card] == 4 and (pattern != CardPattern.BOMB or (pattern == CardPattern.BOMB and card > value)):
                moves.append(Move([card] * 4, CardPattern.BOMB, card))
    # Single Stright
    if pattern == CardPattern.PASS:
        for length in range(5, 13):
            if length <= len(cards):
                moves = moves + getSequence(cards, length, -1, 1)
    if pattern >= 7 and pattern <= 12:
        moves = moves + getSequence(cards, pattern - 2, value, 1)
    # Double Stright
    if pattern == CardPattern.PASS:
        for length in range(3, 11):
            if length < len(cards):
                moves = moves + getSequence(cards, length, -1, 2)
    if pattern >= 15 and pattern <= 22:
        moves = moves + getSequence(cards, pattern - 12, value, 2)
    # Triple Stright
    if pattern == CardPattern.PASS:
        for length in range(2, 7):
            moves = moves + getSequence(cards, length, -1, 3)
    if pattern >= 23 and pattern <= 27:
        moves = moves + getSequence(cards, pattern - 21, value, 3)
    # Triple with one pair
    if pattern == CardPattern.PASS or pattern == CardPattern.TRIPLE_TWO:
        for card in card_count:
            if card_count[card] >= 3 and card > value:
                for cardB in card_count:
                    if card != cardB and card_count[cardB] >= 2:
                        moves.append(Move([card] * 3 + [cardB] * 2, CardPattern.TRIPLE_TWO, card))
    # Triple with one single
    if pattern == CardPattern.PASS or pattern == CardPattern.TRIPLE_ONE:
        for card in card_count:
            if card_count[card] >= 3 and card > value:
                for cardB in card_count:
                    if card != cardB:
                        moves.append(Move([card] * 3 + [cardB], CardPattern.TRIPLE_ONE, card))
    # Triple
    if pattern == CardPattern.PASS or pattern == CardPattern.TRIPLE:
        for card in card_count:
            if card_count[card] >= 3 and card > value:
                moves.append(Move([card] * 3, CardPattern.TRIPLE, card))
    # Pair
    if pattern == CardPattern.PASS or pattern == CardPattern.PAIR:
        for card in card_count:
            if card_count[card] >= 2 and card > value:
                moves.append(Move([card] * 2, CardPattern.PAIR, card))
    # Single
    if pattern == CardPattern.PASS or pattern == CardPattern.SINGLE:
        for card in card_count:
            if card > value:
                moves.append(Move([card], CardPattern.SINGLE, card))


    # Plane
    if pattern == -1:
        for length in range(2, 7):
            moves = moves + getPlane(cards, length, -1)
    if pattern >= 28 and pattern <= 32:
        moves = moves + getPlane(cards, pattern - 26, value)
    # Quads with two singles
    if pattern == -1 or pattern == 33:
        for card in set(cards):
            if cards.count(card) >= 4 and card > value:
                cardBs = list(set(cards) - set([card]))
                for case in list(combinations(cardBs, 2)):
                    moves.append(Move([card] * 4 + list(case), 33, card))
    # Quads with two pairs
    if pattern == -1 or pattern == 34:
        for card in set(cards):
            if cards.count(card) >= 4 and card > value:
                cardBs = list(set(cards) - set([card]))
                for case in list(combinations(cardBs, 2)):
                    flag = True
                    for element in list(case):
                        if cards.count(element) < 2:
                            flag = False
                            break
                    if flag:
                        moves.append(Move([card] * 4 + list(case) * 2, 34, card))

    # Pass
    if pattern != CardPattern.PASS:
        moves.append(Move([], CardPattern.PASS, -1))

    return moves


def evaluate(board):
    if board.currentPlayer() == 1:
        return 10
    else:
        return -10


def minmax(board, alpha, beta, cache = {}):
    if board.isGameOver():
        if not cache.get(hash(board), None):
            cache[hash(board)] = (evaluate(board), None)
        return evaluate(board), None

    if cache.get(hash(board), None):
        return cache[hash(board)]

    bestMove = None
    if board.currentPlayer() == 1:
        bestScore = -float('inf')
    else:
        bestScore = float('inf')

    for move in board.getNextMoves():
        board.makeMove(move)
        score, _ = minmax(board, alpha, beta)
        board.unmakeMove(move)
        if board.currentPlayer() == 1:
            if score > bestScore:
                bestScore = score
                bestMove = move

            if score > alpha:
                alpha = score

            if alpha >= beta:
                break
        else:
            if score < bestScore:
                bestScore = score
                bestMove = move

            if score < beta:
                beta = score

            if alpha >= beta:
                break

    if not cache.get(hash(board), None):
        cache[hash(board)] = (bestScore, bestMove)
    return bestScore, bestMove


def main():
    board = Board()

    # farmer_cards = raw_input('input lord cards: ')
    # board.playerA = Card.convert(farmer_cards.split())
    # lord_cards = raw_input('input farmer cards: ')
    # board.playerB = Card.convert(lord_cards.split())

    board.playerA = Card.convert('Y A K K Q J 10 9 8 5 4'.split())
    board.playerB = Card.convert('2 A K Q J 10 9 9 7 7 3'.split())

    first_hand = True
    while True:
        if board.isGameOver():
            print(board)
            print('Winner: %s' % board.currentPlayer())
            break
        print(board)

        cards_str = raw_input('please take your turn: ')
        if cards_str == 'q':
            print('quit..')
            break

        your_cards = Card.convert(cards_str.split())
        your_move = Move(your_cards)
        your_move.parse()
        if not first_hand and your_move not in board.getNextMoves():
            print('your cards is not valid!')
            continue
        if first_hand:
            first_hand = False
        board.makeMove(your_move)

        _, move = minmax(board, -float('inf'), float('inf'))
        board.makeMove(move)
        print('your oppenonet\'s turn: %s' % move)


if __name__ == '__main__':
    main()
