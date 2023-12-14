# What is the sum of these extrapolated values?

with open("input") as f:
    lines = f.read().splitlines()

def allzeros(input: list[int]) -> bool:
    return all([True if x == 0 else False for x in input])

def extrapolate(input: list[int], previous=False) -> int:
    layers = [input]
    
    while True:
        new_layer = []
        last_layer = layers[-1]
        layer_str = '   '.join(map(str, (last_layer)))
        depth = len(input) - len(last_layer)
        print(f"{depth * '  '}{layer_str}")
        if allzeros(last_layer):
            break
        if len(last_layer) == 1:
            print(f"No interpolation exists for {input}")
            return 0
        for i in range(len(last_layer) - 1):
            new_number = last_layer[i+1] - last_layer[i]
            new_layer.append(new_number)
        layers.append(new_layer)
    interpolation = 0
    if previous:
        sign = True
        for layer in layers:
            if sign:
                interpolation += layer[0]
                sign = False
            else:
                interpolation -= layer[0]
                sign = True
        print(f"Previous = {interpolation}")
    else:
        for layer in layers:    
            interpolation += layer[-1]
        print(f"Next = {interpolation}")
    return interpolation

total1 = []
total2 = []
for line in lines:
    numbers = list(map(int, line.split()))
    print("")
    # total1.append(extrapolate(numbers))
    total2.append(extrapolate(numbers, previous=True))

print(f"\nTotal {sum(total1)}")
print(total1)

print(f"\nTotal {sum(total2)} (previous)")
print(total2)

# Part 2 
# Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?