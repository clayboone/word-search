""" Create a word search puzzle."""

import sys
import random


class Puzzle(object):
    def __init__(self, words=None):
        if words is None:
            return
        else:
            assert isinstance(words, list)

        self.grid = []
        self.words = []
        self.size = 1 + len(max(words, key=len))

        # Make initial empty grid
        for y in range(self.size):
            self.grid.append([])
            for x in range(self.size):
                self.grid[y].append(None)

        # Fill in words in random locations
        words = [word.upper() for word in words]

        for word in words:
            if not self._get_possible_locations(word):
                return

            self.words.append(word)

            x, y, direction = random.choice(
                self._get_possible_locations(word))

            for index, letter in enumerate(word):
                if direction == 'acrs':
                    self.grid[y][x+index] = letter
                elif direction == 'down':
                    self.grid[y+index][x] = letter
                else:  # direction == 'diag'
                    self.grid[y+index][x+index] = letter

        # Fill in empty spaces with random letters
        palette = {'sum': 0}
        for word in self.words:
            for letter in word:
                palette['sum'] += 1
                if letter in palette:
                    palette[letter] += 1
                else:
                    palette[letter] = 1

        letters = []
        weights = []
        for key, value in palette.items():
            if key == 'sum':
                continue

            letters.append(key)
            weights.append(value / palette['sum'])

        for x in range(self.size):
            for y in range(self.size):
                if self.grid[y][x] is None:
                    choice = random.choices(letters, weights=weights)[0]
                    self.grid[y][x] = choice

    def __str__(self):
        """Return the puzzle as a formatted string."""
        s = ''

        for line in self.grid:
            for element in line:
                s += ' ' + ('.' if element is None else element) + ' '
            s += '\n'

        return s[:-1]  # Trims trainling newline

    def _get_possible_locations(self, word):
        """Generate a list of tuples of (x, y, direction) for every possible
        location that a given word can populate inside of the current grid.
        """
        ret = []

        d = 'acrs'
        for y in range(self.size):
            for x in range(self.size - len(word)):
                if self._is_valid_location(x, y, d, word):
                    ret.append((x, y, d))

        d = 'down'
        for y in range(self.size - len(word)):
            for x in range(self.size):
                if self._is_valid_location(x, y, d, word):
                    ret.append((x, y, d))

        d = 'diag'
        for y in range(self.size - len(word)):
            for x in range(self.size - len(word)):
                if self._is_valid_location(x, y, d, word):
                    ret.append((x, y, d))

        return ret

    def _is_valid_location(self, x, y, d, word):
        """Return true if a word can populate a given starting point x, y by
        running a given direction d, otherwise false."""
        if d == 'acrs':
            for i, v in enumerate(range(x, x+len(word))):
                if self.grid[y][v] is not None and self.grid[y][v] != word[i]:
                    return False

            return True

        elif d == 'down':
            for i, v in enumerate(range(y, y+len(word))):
                if self.grid[v][x] is not None and self.grid[v][x] != word[i]:
                    return False

            return True

        else:  # 'diag'
            for yv in range(y, y+len(word)):
                for i, xv in enumerate(range(x, x+len(word))):
                    if self.grid[yv][xv] is not None \
                            and self.grid[yv][xv] != word[i]:
                        return False

            return True


def main():
    puzzle = Puzzle([
        'hello',
        'world',
        'one',
        'two',
        'three',
        'dog',
        'cat',
        'briefly',
        'butterfly',
        'shindig',
        'building',
        'very',
        'word',
        'wow',
    ])

    print(puzzle)


if __name__ == '__main__':
    sys.exit(main())
