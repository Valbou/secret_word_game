from unittest import TestCase
from unittest.mock import MagicMock, patch

from secret_word import Word, GameLogic, InputError


class TestGameLogic(TestCase):
    def setUp(self):
        super().setUp()

        self.gl = GameLogic(word="hello", limit=42)

    def test_init_game_logic(self):
        self.assertEqual(self.gl.limit, 42)
        self.assertIsInstance(self.gl.guess, Word)
        self.assertEqual(self.gl.guess, "hello")

    def test_init_game_logic_random_word(self):
        gl = GameLogic()
        self.assertIsInstance(gl.guess, Word)
        self.assertGreater(gl.guess.length, 0)

    def test_attempt(self):
        self.gl._input = MagicMock(return_value="e")
        self.assertTrue(self.gl.attempt())
        self.gl._input.assert_called_once()

        self.gl._input = MagicMock(return_value="G")
        self.assertTrue(self.gl.attempt())
        self.gl._input.assert_called_once()

    def test_last_attempt(self):
        self.gl.limit = 1
        self.gl._input = MagicMock(return_value="z")

        self.assertFalse(self.gl.attempt())
        self.gl._input.assert_called_once()

    @patch("secret_word.input", create=True)
    def test_input_lower(self, mock: MagicMock):
        mock.return_value = "h"
        result = self.gl._input()

        self.assertIsInstance(result, str)
        self.assertEqual(result, "h")

    @patch("secret_word.input", create=True)
    def test_input_upper(self, mock: MagicMock):
        mock.return_value = "L"
        result = self.gl._input()

        self.assertIsInstance(result, str)
        self.assertEqual(result, "l")

    @patch("secret_word.input", create=True)
    def test_input_number(self, mock: MagicMock):
        mock.return_value = "1"

        with self.assertRaises(InputError) as e:
            self.gl._input()

        self.assertEqual(f"{e.exception}", "Try again, ASCII letter only")

    @patch("secret_word.input", create=True)
    def test_input_special(self, mock: MagicMock):
        mock.return_value = "@"

        with self.assertRaises(InputError) as e:
            self.gl._input()

        self.assertEqual(f"{e.exception}", "Try again, ASCII letter only")

    @patch("secret_word.input", create=True)
    def test_input_already_proposed(self, mock: MagicMock):
        mock.return_value = "l"

        self.gl.attempt()
        with self.assertRaises(InputError) as e:
            self.gl._input()

        self.assertEqual(f"{e.exception}", "This letter 'l' was already proposed")


class TestWord(TestCase):
    def setUp(self):
        super().setUp()

        self.word = Word("Hello")

    def test_init_word(self):
        self.assertEqual(self.word.length, 5)
        self.assertEqual(self.word.secret, "_" * 5)
        self.assertEqual(self.word, "Hello")

    def test_check(self):
        self.assertTrue(self.word.check("H"))
        self.assertFalse(self.word.check("h"))

    def test_findall(self):
        indexes = self.word._findall("l")

        self.assertEqual(len(indexes), 2)
        self.assertListEqual([2, 3], indexes)

    def test_replace(self):
        self.word.replace("l")

        self.assertEqual(self.word.secret, "__ll_")

        # Assert no secret regression
        self.word.replace("l")

        self.assertEqual(self.word.secret, "__ll_")

    def test_is_found(self):
        self.assertFalse(self.word.is_found())

        self.word.replace("H")
        self.word.replace("e")
        self.word.replace("l")
        self.word.replace("o")

        self.assertTrue(self.word.is_found())
