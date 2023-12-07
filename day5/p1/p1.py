import sys 

def get_seeds():
  seed_input = input().split()[1:]
  seeds = list(map(int,seed_input))  
  return seeds 

def make_map():
  map_name = input()
  data = input()
  mp = []
  while data.strip() != "":
    dest, source, map_range = list(map(int,data.split()))
    mp.append([source, dest, map_range])
    try:
      data = input()
    except:
      return mp
  return mp

def is_in_range(source, map_range, target):
  if source <= target <= source + map_range:
    return (True, target - source)
  return (False, 0)


def skip_line():
  input()

seeds = get_seeds()
skip_line()
maps = []
try:
  while True:
    maps.append(make_map())
except EOFError:
  pass

min_location = sys.maxsize
for seed in seeds:
  current = seed
  
  for mp in maps:
    
    for source, dest, map_range in mp:
      in_range, offset = is_in_range(source, map_range, current)
      if in_range:
        current = dest + offset
        break
  min_location = min(min_location, current)

print(min_location)