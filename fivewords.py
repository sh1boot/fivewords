#!/usr/bin/env python3

import itertools
import array

anagrams = False
firstletter = [ [ set() for _ in range(f) ] for f in range(26) ]
wordnames = {}

def letter_to_bit(c):
  return 'aesiorunltycdhmpgkbwfvzjxq'.find(c)
  #return ord(c) - ord('a')

with open('words_alpha.txt') as wordlist:
  for word in wordlist.read().split():
    if len(word) == 5:
      mask = 0
      word = word.lower()
      for c in word:
        i = letter_to_bit(c)
        if not (0 <= i and i < 26): break
        b = 1 << i
        if mask & b: break
        mask |= b
      else:
        first = mask.bit_length() - 1
        tmp = mask & (mask - 1)
        last = (mask ^ tmp).bit_length() - 1
        wordnames.setdefault(mask, set()).add(word)
        firstletter[first][last].add(mask)

count = 0
def emit(progress):
  global count
  if anagrams:
    for s in itertools.product(*(wordnames[word] for word in progress)):
      print(*sorted(s))
      count += 1
  else:
    print(*sorted(next(iter(wordnames[word])) for word in progress))
    count += 1

def solve(alphabet, bits_left, progress=array.array('L', (0, 0, 0, 0, 0)), depth=0):
  while bits_left + 5 * depth >= 25:
    first = alphabet.bit_length() - 1
    for last in range(first):
      if ((alphabet >> last) & 1) != 0:
        for mask in firstletter[first][last]:
          if (mask & alphabet) == mask:
            progress[depth] = mask
            if depth >= 4:
              emit(progress)
            else:
              solve(alphabet & ~mask, bits_left - 5, progress, depth + 1)
    alphabet &= ~(1 << first)
    bits_left -= 1

alphabet = (1 << 26) - 1
solve(alphabet, alphabet.bit_count())
print(f'total: {count}')
