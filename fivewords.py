#!/usr/bin/env python3

import itertools

anagrams = False
firstletter = [ dict() for _ in range(26) ]

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
        wordlist = firstletter[first].setdefault(mask, set())
        wordlist.add(word)

count = 0
def emit(progress):
  global count
  if anagrams:
    for s in itertools.product(*progress):
      print(*sorted(s))
      count += 1
  else:
    print(*sorted(next(iter(words)) for words in progress))
    count += 1

def solve(alphabet, bits_left, progress=[]):
  depth = len(progress)
  while bits_left + 5 * depth >= 25:
    first = alphabet.bit_length() - 1
    for mask, words in firstletter[first].items():
      if (mask & alphabet) == mask:
        new_progress = progress + [words]
        if depth >= 4:
          emit(new_progress)
        else:
          new_alphabet = alphabet & ~mask
          solve(new_alphabet, bits_left - 5, new_progress)
    alphabet &= ~(1 << first)
    bits_left -= 1

alphabet = (1 << 26) - 1
solve(alphabet, alphabet.bit_count())
print(f'total: {count}')
