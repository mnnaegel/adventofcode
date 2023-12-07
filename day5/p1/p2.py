import sys 

def get_seed_pairs():
  seed_input = input().split()[1:]
  seeds = list(map(int,seed_input))  
  
  seed_pairs = []
  i = 0
  while i < len(seeds) - 1:
    seed_pairs.append((seeds[i], seeds[i+1]))
    i += 2
  
  return seed_pairs 

def map_seed_to_location(seed, maps):
  current = seed
  maps_used = [-1 for _ in range(len(maps))]
  for i,mp in enumerate(maps):
    for j, val in enumerate(mp):
      source, dest, map_range = val
      if source <= current <= source + map_range:
        current = dest + (current - source)
        maps_used[i] = j
        break
  return current, tuple(maps_used)

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

def skip_line():
  input()

seed_pairs = get_seed_pairs()
skip_line()
maps = []
try:
  while True:
    maps.append(make_map())
except EOFError:
  pass

min_location = sys.maxsize

for seed,seed_range in seed_pairs:
  # kinda like a substitution network... lets find pools of the same substitution (ranges) and take the lowest one
  l = seed 
  
  while l <= seed + seed_range - 1:
    l_location, l_maps_used = map_seed_to_location(l, maps)
    
    r = seed + seed_range
    while l <= r:
      r_location, r_maps_used = map_seed_to_location(r, maps)
      print("l", l, "r", r, "l_maps_used", l_maps_used, "r_maps_used", r_maps_used)
      
      if l_maps_used == r_maps_used:
        min_location = min(min_location, l_location)
        
        l = r+1

        break
      else:
        r = (l+r)//2
        
print(min_location)

  
  
  