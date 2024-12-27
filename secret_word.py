#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import ascii_lowercase
from random import choice

from words import WORD_LIST

class InputError(Exception):
    pass


class GameLogic:
    letters = set()
    guess = ""

    def __init__(self, word: str = "", limit: int = 10):
        self.limit = limit
        self.guess = Word(word.lower()) or Word(choice(WORD_LIST))

    def attempt(self) -> bool:
        print("", f"Hit left : {self._hit_left}", sep="\n")
        print(f"Find the word : {self.guess.secret}")

        result = False

        letter = ""
        while not letter:
            try:
                letter = self._input()
            except InputError as e:
                print(f"Error: {e}")

        if self.guess.check(letter):
            print("You found a letter !")
            self.guess.replace(letter)
            result = not self.guess.is_found()

        else:
            print("Oups ! Try again !")
            self.letters.add(letter)
            result = self._hit_left > 0

        return result

    @property
    def _hit_left(self) -> int:
        return self.limit - len(self.letters)

    def _input(self) -> str:
        letter = input(
            f"Give me a letter (attempt number {len(self.letters)}): "
        )[:1].lower()

        if not letter or not letter in ascii_lowercase:
            raise InputError("Try again, ASCII letter only")

        elif letter in self.letters or letter in self.guess.secret:
            raise InputError(f"This letter '{letter}' was already proposed")

        return letter


class Word(str):
    length = 0
    secret = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.length = len(self)
        self.secret = "_" * self.length

    def check(self, letter) -> bool:
        return letter in self

    def _findall(self, letter) -> list[int]:
        return [i for i, l in enumerate(self) if l == letter]

    def replace(self, letter) -> None:
        indexes = self._findall(letter)
        for p in indexes:
            self.secret = self.secret[:p] + letter + self.secret[p+1:]

    def is_found(self) -> bool:
        return True if self == self.secret else False


if __name__ == "__main__":
    print(
        "#" * 23,
        "Welcome in the v1.0.1 of",
        "Valbou Secret Word Game",
        "#" * 23,
        sep="\n"
    )

    game = GameLogic()
    while game.attempt():
        pass

    if game.guess.is_found():
        print(f"You Win ! The word is '{game.guess.secret}'")

    else:
        print("You Loose !")

    print("End of game")
