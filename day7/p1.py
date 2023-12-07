hand_bid_pairs = []
try:
  while True:
    hand, bid = input().split()
    hand_bid_pairs.append((hand, int(bid)))
except:
  pass

def is_five_of_a_kind(hand):
  for i in range(len(hand)):
    if hand.count(hand[i]) == 5 or (hand.count(hand[i]) == 4 and hand.count('J')==1) or (hand.count(hand[i]) == 3 and hand.count('J') == 2) or (hand.count(hand[i]) == 2 and hand.count('J') == 3) or (hand.count(hand[i]) == 1 and hand.count('J') == 4):
      return True
  return False

def is_four_of_a_kind(hand):
  for i in range(len(hand)):
    if hand.count(hand[i]) == 4 or (hand.count(hand[i]) == 3 and hand.count('J')==1) or (hand.count(hand[i]) == 2 and hand.count('J') == 2 and 'J' != hand[i]) or (hand.count(hand[i]) == 1 and hand.count('J') == 3):
      return True
  return False

def is_two_pair_no_joker(hand):
  for i in range(len(hand)):
    if hand.count(hand[i]) == 2:
      for j in range(len(hand)):
        if hand.count(hand[j]) == 2 and hand[i] != hand[j] and hand[i] != 'J' and hand[j] != 'J':
          return True
  return False

def is_one_pair_no_joker(hand):
  for i in range(len(hand)):
    if hand.count(hand[i]) == 2 and hand[i] != 'J':
      return True
  return False

def is_full_house(hand):
  # joker case 1: 1 joker and 2 pairs
  if hand.count('J') == 1 and is_two_pair_no_joker(hand):
    return True
  
  # joker case 2: 2 jokers and 1 pair
  if hand.count('J') == 2 and is_one_pair_no_joker(hand):
    return True

  # joker case 4: 4 jokers GG
  if hand.count('J') >= 3:
    return True
  
  for i in range(len(hand)):
    if hand.count(hand[i]) == 3:
      for j in range(len(hand)):
        if hand.count(hand[j]) == 2:
          return True
  return False

def is_three_of_a_kind(hand):
  if hand.count('J') >= 3:
    return True
  
  for i in range(len(hand)):
    if hand.count(hand[i]) == 3 or (hand.count(hand[i]) == 2 and hand.count('J')==1) or (hand.count(hand[i]) == 1 and hand.count('J') == 2):
      return True
  return False

def is_two_pair(hand):
  # 1 joker and 1 pair
  if hand.count('J') == 1 and is_one_pair_no_joker(hand):
    return True
  
  # 2 joker and 0 pair
  if 'J' in hand and hand.count('J') >= 2:
    return True
  
  for i in range(len(hand)):
    if hand.count(hand[i]) == 2:
      for j in range(len(hand)):
        if hand.count(hand[j]) == 2 and hand[i] != hand[j]:
          return True
  return False

def is_one_pair(hand):
  if 'J' in hand:
    return True
  
  for i in range(len(hand)):
    if hand.count(hand[i]) == 2:
      return True
  return False

hand_rankings = {
  0: is_five_of_a_kind,
  1: is_four_of_a_kind,
  2: is_full_house,
  3: is_three_of_a_kind,
  4: is_two_pair,
  5: is_one_pair,
  6: lambda x: True
}

hand_names = {
  0: 'five of a kind',
  1: 'four of a kind',
  2: 'full house',
  3: 'three of a kind',
  4: 'two pair',
  5: 'one pair',
  6: 'highest card'
}

# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
best_cards = {
  'A': 13,
  'K': 12,
  'Q': 11,
  'T': 9,
  '9': 8,
  '8': 7,
  '7': 6,
  '6': 5,
  '5': 4,
  '4': 3,
  '3': 2,
  '2': 1,
  'J': 0
}

def tiebreak_best_card(hand1, hand2):
  for i in range(5):
    if hand1[i] == hand2[i]:
      continue
    else:
      return best_cards[hand1[i]] > best_cards[hand2[i]]

def get_better_hand(hand1, hand2):
  # get hand1 ranking
  for i in range(len(hand_rankings)):
    if hand_rankings[i](hand1) and hand_rankings[i](hand2):
      # tiebreaker best first card
      if tiebreak_best_card(hand1, hand2):
        return hand1
      else:
        return hand2
    elif hand_rankings[i](hand1) and not hand_rankings[i](hand2):
      return hand1
    elif not hand_rankings[i](hand1) and hand_rankings[i](hand2):
      return hand2
    else:
      continue 
    
def merge_sort(hand_bid_pairs):
  if len(hand_bid_pairs) == 1:
    return hand_bid_pairs[:]
  
  mid = len(hand_bid_pairs) // 2
  left = hand_bid_pairs[:mid][:]
  right = hand_bid_pairs[mid:][:]
  
  left = merge_sort(left)
  right = merge_sort(right)
  
  if not right:
    return left
  elif not left:
    return right
  
  new = []
  
  lp = 0
  rp = 0
  while lp < len(left) and rp < len(right):
    if get_better_hand(left[lp][0], right[rp][0]) == left[lp][0]:
      new.append(left[lp])
      lp += 1
    else:
      new.append(right[rp])
      rp += 1
  
  while lp < len(left):
    new.append(left[lp])
    lp += 1
    
  while rp < len(right):
    new.append(right[rp])
    rp += 1
    
  return new


sorted_hands = merge_sort(hand_bid_pairs)[::-1]
def test_all(hand):
  print("is_five_of_a_kind: ", is_five_of_a_kind(hand))
  print("is_four_of_a_kind: ", is_four_of_a_kind(hand))
  print("is_full_house: ", is_full_house(hand))
  print("is_three_of_a_kind: ", is_three_of_a_kind(hand))
  print("is_two_pair: ", is_two_pair(hand))
  print("is_one_pair: ", is_one_pair(hand))

total = 0
for i, hand_bid in enumerate(sorted_hands):
  hand,bid=hand_bid
  total += (i+1) * bid
print(total)