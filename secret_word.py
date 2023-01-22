#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import ascii_lowercase
from random import choice

from .words import WORD_LIST


class GameLogic:
    letters = set()
    guess = ''

    def __init__(self, limit=10):
        self.limit = limit
        self.guess = Word(choice(WORD_LIST))

    def attempt(self):
        print('', 'Hit left : {}'.format(self._hit_left), sep='\n')
        print('Find the word :', self.guess.secret)
        letter = self._input()
        if self.guess.check(letter):
            print('You found a letter !')
            self.guess.replace(letter)
            return not self.guess.is_found()
        else:
            print('Too bad ! Try again !')
            self.letters.add(letter)
            return self._hit_left

    @property
    def _hit_left(self):
        return self.limit - len(self.letters)

    def _input(self):
        letter = input(
            'Give me a letter (attempt number {})'.format(len(self.letters))
        )[:1].lower()
        if not letter or not letter in ascii_lowercase:
            print('Try again, ASCII letter only')
            return self._input()
        elif letter in self.letters or letter in self.guess.secret:
            print('The letter {} has already been played'.format(letter))
            return self._input()
        return letter


class Word(str):
    length = 0
    secret = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.length = len(self)
        self.secret = "_"*self.length

    def check(self, letter):
        if letter in self:
            return True
        return False

    def _findall(self, letter):
        return [i for i, l in enumerate(self) if l == letter]

    def replace(self, letter):
        indexes = self._findall(letter)
        for p in indexes:
            self.secret = self.secret[:p]+letter+self.secret[p+1:]

    def is_found(self):
        return True if self == self.secret else False


if __name__ == '__main__':
    print(
        '#'*23,
        'Welcome in the v1.0 of',
        'Valbou Secret Word Game',
        '#'*23,
        sep="\n"
    )

    game = GameLogic()
    while game.attempt():
        pass
    if game.guess.is_found():
        print('You Win !')
    else:
        print('You Loose !')
    print('End of game')


