# Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

with open("input") as f:
    lines = f.read().splitlines()
    print("\n".join(lines))

width = len(lines[0])
height = len(lines)

def traverse(start) -> list[tuple[int, int]]:
    
    path = [start]
    x, y = start
    
    if lines[y-1][x] in "|F7": # Up
        y -= 1
    elif lines[y+1][x] in "|LJ": # Down
        y += 1
    elif lines[y][x-1] in "-FL": # Left
        x -= 1
    elif lines[y][x+1] in "-J7": # Right
        x += 1
    
    while True:
            
        pipe = lines[y][x]
        next_x, next_y = x, y
        print(f"At {(x, y)} ({pipe})")
        match pipe:
            case "-":
                if (x-1, y) in path:
                    next_x += 1
                    if (x-1, y) == start and len(path) > 3:
                        break
                else:
                     next_x -= 1
            case "|":
                if (x, y-1) in path:
                    next_y += 1
                    if (x, y-1) == start and len(path) > 3:
                        break
                else:
                    next_y -= 1
            case "J":
                if (x-1, y) in path:
                    next_y -= 1
                    if (x-1, y) == start and len(path) > 3:
                        break
                else:
                    next_x -= 1
            case "L":
                if (x, y-1) in path:
                    next_x += 1
                    if (x, y-1) == start and len(path) > 3:
                        break
                else:
                    next_y -= 1
            case "7":
                if (x-1, y) in path:
                    next_y += 1
                    if (x-1, y) == start and len(path) > 3:
                        break
                else:
                    next_x -= 1
            case "F":
                if (x+1, y) in path:
                    next_y += 1
                    if (x+1, y) == start and len(path) > 3:
                        break
                else:
                    next_x += 1

        path.append((x, y))
        assert(len(path) == len(set(path)))
        assert(len(path) < (width*height))
        x, y = next_x, next_y
        print(f"{len(path)} / {width*height}")

    path.append((next_x, next_y))
    return path


for y in range(height):
    for x in range(width):
        pipe = lines[y][x]
        if pipe == "S":
            start = (x, y)
            print(f"Start coordinates found: {start}")
            path = traverse(start)
            print(f"Path length = {len(path)/2}")