times = list(map(int, input().split(":")[1].split())) 
distances = list(map(int, input().split(":")[1].split()))
time_dist_pairs = zip(times, distances)
time_dist_pairs = sorted(time_dist_pairs, key=lambda x: x[0])
print(time_dist_pairs)

def get_number_of_valid_pairs(time_dist_pair):
    time, distance = time_dist_pair
    
    optimal_held_time = time // 2
    optimal_held_distance = optimal_held_time * (time - optimal_held_time)
  
      
    if optimal_held_distance < distance:
        print("invalid")
        return 0    
      
    # perform bsearch to find left valid bound
    time_held = 0
    right = optimal_held_time 
    while time_held < right:
        mid = (time_held + right) // 2
        if mid * (time - mid) <= distance:
            time_held = mid + 1
        else:
            right = mid - 1
    left_bound = right 
    if (right * (time - right)) <= distance:
        left_bound+=1
        
    # perform bsearch to find right valid bound
    left = optimal_held_time 
    right = time
    
    while left < right:
        print("left: ", left, "right: ", right)
        mid = (left + right) // 2
        if mid * (time - mid) <= distance:
            right = mid - 1
        else:
            left = mid + 1
    right_bound = left
    if (left * (time - left)) <= distance:
        right_bound-=1
    
    print("left bound: ", left_bound
          , "right bound: ", right_bound)
    return right_bound - left_bound + 1
  
a = 1
for time_dist_pair in time_dist_pairs:
    a *= get_number_of_valid_pairs(time_dist_pair)
print(a)