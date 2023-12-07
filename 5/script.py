'''
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category.

Each line within a map contains three numbers: the destination range start, the source range start, and the range length.
'''

# Part 1 Plan A
# create full mappings
# run numbers through the maps
# --> memory runs out

# Part 1 Plan B
# Store sections and calculate conversion when needed

# Part 2 Plan A 
# Extend seed list by brute force
# --> memory runs out

# Part 2 Plan B
# Mappings are linear transformations
# Start from the bottom and find the boundaries

with open("input") as f:
    lines = f.read().replace(":", "").split("\n\n")

seeds = lines[0]
seeds = list(map(int, seeds.split("seeds")[1].split()))

# part 2
'''The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range.'''

seed_range_starts = seeds[::2]
seed_range_lengths = seeds[1::2]
seed_ranges = [(start, start+length) for start, length in zip(seed_range_starts, seed_range_lengths)]
seed_ranges.sort(key=lambda x:x[0])

print(f"seed ranges = {list(seed_ranges)}")
print()
# example: [(55, 68), (79, 93)]
# input: [(2637529854, 2860924753), (3007537707, 3511520874), (307349251, 504732786), (3543757609, 3820406009), (2296792159, 2437803014), (116452725, 121613258), (2246652813, 2296420149), (762696372, 923151449), (3960442213, 4066309214), (1197133308, 1235680074)]

#  {'seed-to-soil map': {98: 50, ... , 97: 99}, 'soil-to-fertilizer map': {15: 0, 18: 3, ... ,} ... } # WRONG
mappings = {} 
# {('seed', 'soil'): [((0, 49), (0, 49)), ((98, 99), (50, 51)), ((50, 97), (52, 99))], ('soil', 'fertilizer'): [((15, 51), (0, 36)), ((52, 53), (37, 38)), ((0, 14), (39, 53))], ('fertilizer', 'water'): [((11, 52), (0, 41)), ((0, 6), (42, 48)), ((53, 60), (49, 56)), ((7, 10), (57, 60))], ('water', 'light'): [((0, 17), (0, 17)), ((25, 94), (18, 87)), ((18, 24), (88, 94))], ('light', 'temperature'): [((0, 44), (0, 44)), ((77, 99), (45, 67)), ((64, 76), (68, 80)), ((45, 63), (81, 99))], ('temperature', 'humidity'): [((69, 69), (0, 0)), ((0, 68), (1, 69))], ('humidity', 'location'): [((0, 55), (0, 55)), ((93, 96), (56, 59)), ((56, 92), (60, 96))]} # CORRECT

category_mapping = {}
category_mapping_reversed = {}
# {'soil': 'seed', 'fertilizer': 'soil', 'water': 'fertilizer', 'light': 'water', 'temperature': 'light', 'humidity': 'temperature', 'location': 'humidity'}

# populate mappings and reversed_mapping_categories
for line in lines[1:]:
    map_name, *mapping_sections = line.splitlines()
    # print(f"\n{map_name}, sections={len(mapping_sections)}")
    mapping = []
    lowest_mapping = float("inf")
    for section in mapping_sections:
        destination_start, source_start, length = map(int, section.split())
        source_end = source_start + length - 1
        destination_end = destination_start + + length - 1
        destination = (destination_start, destination_end)
        source = (source_start, source_end)
        mapping.append((source, destination))
        if lowest_mapping > destination_start:
            lowest_mapping = destination_start

    if lowest_mapping > 0:
        mapping.append(((0, lowest_mapping-1), (0, lowest_mapping-1)))
    
    mapping.sort(key=lambda x:x[1][0])
    category_source, category_destination = map_name.split(" map")[0].split("-to-")
    map_type = (category_source, category_destination)
    mappings[map_type] = mapping
    category_mapping[category_source] = category_destination
    category_mapping_reversed[category_destination] = category_source

print(f"mappings = {mappings}")

final_category = list(category_mapping_reversed.keys())[-1] # (=location)
final_category_mappings = mappings[(category_mapping_reversed[final_category], final_category)]
# [((0, 55), (0, 55)), ((93, 96), (56, 59)), ((56, 92), (60, 96))]

def get_seed_ranges(mapping_range: tuple[int, int], category: str) -> tuple[list[tuple[int, int]], str]:

    # [((69, 69), (0, 0)), ((0, 68), (1, 69))],
    # input = (0, 55) 
    # output = (69, 69), (0, 54)

    #  [((0, 44), (0, 44)), ((77, 99), (45, 67)), ((64, 76), (68, 80)), ((45, 63), (81, 99))],
    # input (0, 54)
    # output (0, 44), (77, 87)

    target_start, target_end = mapping_range # (0, 55)
    source_category = category_mapping_reversed[category] # temperature
    if source_category == "seed":
        return ([mapping_range], source_category)
    
    source_of_source_category = category_mapping_reversed[source_category] # humidity
    source_mapping_key = (source_of_source_category, source_category)

    # print(f"input = {mapping_range}, category = {category}")
    return_ranges = []
    for mapping in mappings[source_mapping_key]:
        
        source_range, destination_range = mapping
        source_start, source_end = source_range
        destination_start, destination_end = destination_range
        range_start = max(target_start, destination_start)
        range_end = min(target_end, destination_end)

        # print(f"section: {mapping[0]} --> {mapping[1]}")
        if (destination_start > target_end) or (target_start > destination_end):
            if (target_start, target_end) not in return_ranges:
                return_ranges.append((target_start, target_end))
            continue
        
        # print(f"target_start = {target_start}, target_end = {target_end}")
        # print(f"destination_start = {destination_start}, destination_end = {destination_end}")
        # print(f"source_start = {source_start}, source_end = {source_end}")
        delta = destination_start - source_start
        # print(f"range_start = {range_start-delta}, range_end = {range_end-delta}")

        if (range_start-delta, range_end-delta) not in return_ranges:
            return_ranges.append((range_start-delta, range_end-delta))

        # print(f"  {range_start-delta} --> {range_start} +({delta})")
        # print(f"  {range_end-delta} --> {range_end} +({delta})")
        # print()

    return (list(set(return_ranges)), source_category)

matching_ranges = []
matching_seed_starts = []
for initial_mapping_range in final_category_mappings:
    initial_location, initial_source = initial_mapping_range
    mapping_ranges = [(initial_location, final_category)]
    # print("--------------------------------------------")
    # print(final_category_mappings)
    # print(f"Searching with {initial_location}\n")
    while mapping_ranges:
        current_mapping = mapping_ranges.pop()
        mapping_range, category = current_mapping
        next_ranges, next_category = get_seed_ranges(mapping_range, category)
        if next_category == "seed":
            found_seed_range = next_ranges[0]
            # print(f"Potential seed range found: {found_seed_range} (A)")
            for seed_range in seed_ranges:
                found_seed_range_start, found_seed_range_end = found_seed_range
                seed_range_start, seed_range_end = seed_range
                if (found_seed_range_end < seed_range_start) or (found_seed_range_start > seed_range_end):
                    # print(f"  Seed range {seed_range} not suitable")
                    continue
                initial_start, initial_end = initial_location
                matching_seed_range_start = max(found_seed_range_start, seed_range_start)
                # print(found_seed_range_start)
                # print(seed_range_start)
                matching_seed_range_end = min(found_seed_range_end, seed_range_end)
                # print(found_seed_range_end)
                # print(seed_range_end)
                matching_seed_range = (matching_seed_range_start, matching_seed_range_end)
                # print(f"  Matching seed range found: {matching_seed_range}!")
                # print(f"  Initial location = {initial_location}")
                # print(f"  Matching seed range = {matching_seed_range}")
                matching_ranges.append(matching_seed_range)
                matching_seed_starts.append(matching_seed_range_start)

        if next_ranges:
            next_range_lengths = 0
            for next_range in next_ranges:
                next_range_lengths += (next_range[1] - next_range[0]) + 1
            mapping_range_length = mapping_range[1] - mapping_range[0] + 1
            if (mapping_range_length != next_range_lengths):
                next_ranges.append((mapping_range[1]-mapping_range[0], mapping_range[1]))
                next_range_lengths += (next_ranges[-1][1] - next_ranges[-1][0]) + 1
            # print(f"\nSource ranges for {mapping_range} ({category}): {next_ranges} ({next_category})")
                    # Source ranges for (0, 55) (location): [(69, 69), (0, 54)] (humidity)
            # print("\n----------------\n")
            for next_range in next_ranges:
                if next_category != "seed":
                    mapping_ranges.append((next_range, next_category))


# print(matching_ranges)

def get_location_by_seed(seed: int, show=False):
    # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    current_value = seed
    current_category = "seed"
    while True:
        next_category = category_mapping[current_category]
        next_mappings = mappings[(current_category, next_category)]
        next_value = None
        for section in next_mappings:
            source, destination = section
            source_start, source_end = source
            destination_start, destination_end = destination
            delta = destination_start - source_start
            if source_start <= current_value <= source_end:
                next_value = current_value + delta
        if not next_value:
            next_value = current_value 
        if show:
            print(f"  {current_category} {current_value} --> {next_category} {next_value}")
        current_value = next_value
        current_category = next_category
        if current_category == final_category:
            return current_value

#assert(get_location_by_seed(79) == 82)
#assert(get_location_by_seed(14) == 43)
#assert(get_location_by_seed(13) == 35)

'''
smallest_locations = []
print("\nHumidity-Location mappings:")
print(mappings[('humidity', 'location')])
print("\nMatching ranges:")
for matching_range in matching_ranges:
    seed_range, initial_range = matching_range
    # print(f"Initial range = {initial_range}, seed range = {seed_range}:")
    location = get_location_by_seed(seed_range[0])
    if location not in smallest_locations:
        smallest_locations.append(location)
'''

final_locations = {}
for seed_start in set(matching_seed_starts):
    location = get_location_by_seed(seed_start)
    final_locations[location] = seed_start

# print(f"final locations = {final_locations}")
smallest_location = min(final_locations.keys())
print(f"\nSmallest seed: {smallest_location}")
print()
get_location_by_seed(final_locations[smallest_location], show=True)

''' OUTPUT:
# ---------

λ script
seed ranges = [(116452725, 121613258), (307349251, 504732786), (762696372, 923151449), (1197133308, 1235680074), (2246652813, 2296420149), (2296792159, 2437803014), (2637529854, 2860924753), (3007537707, 3511520874), (3543757609, 3820406009), (3960442213, 4066309214)]

mappings = {('seed', 'soil'): [((30748436, 509305211), (0, 478556775)), ((890067010, 1121869539), (478556776, 710359305)), ((576061773, 890067009), (710359306, 1024364542)), ((1121869540, 1886439716), (1024364543, 1788934719)), ((0, 30748435), (1788934720, 1819683155)), ((509305212, 576061772), (1819683156, 1886439716))], ('soil', 'fertilizer'): [((307861200, 328491492), (0, 20630292)), ((205631872, 215506277), (20630293, 30504698)), ((101283437, 124027421), (30504699, 53248683)), ((215506278, 307861199), (53248684, 145603605)), ((166806183, 205631871), (145603606, 184429294)), ((124027422, 166806182), (184429295, 227208055)), ((0, 101283436), (227208056, 328491492)), ((2201866248, 2286946660), (730037950, 815118362)), ((1688321922, 1704832212), (815118363, 831628653)), ((3866378386, 4002766746), (831628654, 968017014)), ((3370246093, 3427660870), (968017015, 1025431792)), ((3427660871, 3650305028), (1025431793, 1248075950)), ((2775815067, 2910044567), (1248075951, 1382305451)), ((2065165179, 2068943952), (1382305452, 1386084225)), ((4200760960, 4231885104), (1386084226, 1417208370)), ((1449362522, 1647814533), (1417208371, 1615660382)), ((3128249668, 3258368022), (1615660383, 1745778737)), ((3272163457, 3370246092), (1745778738, 1843861373)), ((3725216194, 3756833621), (1843861374, 1875478801)), ((3756833622, 3762642502), (1875478802, 1881287682)), ((1988934358, 2065165178), (1881287683, 1957518503)), ((1068122989, 1073802716), (1957518504, 1963198231)), ((3098529992, 3128249667), (1963198232, 1992917907)), ((4002766747, 4187480977), (1992917908, 2177632138)), ((4231885105, 4266444705), (2177632139, 2212191739)), ((2910044568, 3098529991), (2212191740, 2400677163)), ((1023403912, 1068122988), (2400677164, 2445396240)), ((816829001, 1023403911), (2445396241, 2651971151)), ((3650305029, 3725216193), (2651971152, 2726882316)), ((4266444706, 4294967295), (2726882317, 2755404906)), ((1647814534, 1688321921), (2755404907, 2795912294)), ((1389905204, 1449362521), (2795912295, 2855369612)), ((1073802717, 1082088845), (2855369613, 2863655741)), ((1884082338, 1988934357), (2863655742, 2968507761)), ((2068943953, 2201866247), (2968507762, 3101430056)), ((730037950, 816829000), (3101430057, 3188221107)), ((1082088846, 1318303541), (3188221108, 3424435803)), ((4187480978, 4200760959), (3424435804, 3437715785)), ((2286946661, 2775815066), (3437715786, 3926584191)), ((1318303542, 1389905203), (3926584192, 3998185853)), ((3762642503, 3866378385), (3998185854, 4101921736)), ((3258368023, 3272163456), (4101921737, 4115717170)), ((1704832213, 1884082337), (4115717171, 4294967295))], ('fertilizer', 'water'): [((2087573570, 2111757596), (0, 24184026)), ((1102417398, 1130660148), (24184027, 52426777)), ((0, 42548208), (52426778, 94974986)), ((341413667, 409711427), (94974987, 163272747)), ((80266080, 257727975), (163272748, 340734643)), ((1624436234, 2049845517), (340734644, 766143927)), ((2147127897, 2260891441), (766143928, 879907472)), ((764333687, 897499178), (879907473, 1013072964)), ((2111757597, 2147127896), (1013072965, 1048443264)), ((602610298, 722677905), (1048443265, 1168510872)), ((722677906, 758955041), (1168510873, 1204788008)), ((970813056, 1102417397), (1204788009, 1336392350)), ((257727976, 263379055), (1336392351, 1342043430)), ((1130660149, 1351697382), (1342043431, 1563080664)), ((758955042, 764333686), (1563080665, 1568459309)), ((42548209, 80266079), (1568459310, 1606177180)), ((2049845518, 2087573569), (1606177181, 1643905232)), ((409711428, 515956967), (1643905233, 1750150772)), ((263379056, 341413666), (1750150773, 1828185383)), ((897499179, 970813055), (1828185384, 1901499260)), ((2260891442, 2291430342), (1901499261, 1932038161)), ((1351697383, 1624436233), (1932038162, 2204777012)), ((515956968, 539688171), (2204777013, 2228508216)), ((539688172, 602610297), (2228508217, 2291430342)), ((2628693938, 2709578465), (2317094055, 2397978582)), ((3434006892, 3494200838), (2397978583, 2458172529)), ((4127689236, 4203009035), (2458172530, 2533492329)), ((3494200839, 3801741355), (2533492330, 2841032846)), ((2709578466, 2728527489), (2841032847, 2859981870)), ((4203009036, 4294967295), (2859981871, 2951940130)), ((3927342522, 4014822610), (2951940131, 3039420219)), ((2338591428, 2628693937), (3039420220, 3329522729)), ((2799034919, 2903448575), (3329522730, 3433936386)), ((2728527490, 2799034918), (3433936387, 3504443815)), ((3801741356, 3821183275), (3504443816, 3523885735)), ((4014822611, 4127689235), (3523885736, 3636752360)), ((3821183276, 3927342521), (3636752361, 3742911606)), ((2903448576, 3434006891), (3742911607, 4273469922)), ((2317094055, 2338591427), (4273469923, 4294967295))], ('water', 'light'): [((130098134, 201997254), (0, 71899120)), ((201997255, 241053373), (71899121, 110955239)), ((241053374, 279218055), (110955240, 149119921)), ((0, 130098133), (149119922, 279218055)), ((1366401345, 1421187550), (496126127, 550912332)), ((2299639191, 2316420570), (550912333, 567693712)), ((1443415170, 1486911571), (567693713, 611190114)), ((1486911572, 1551009053), (611190115, 675287596)), ((4169571318, 4294967295), (675287597, 800683574)), ((2316420571, 2625614673), (800683575, 1109877677)), ((2647277659, 2667479330), (1109877678, 1130079349)), ((865464335, 1065408319), (1130079350, 1330023334)), ((1421187551, 1443415169), (1330023335, 1352250953)), ((496126127, 500429409), (1352250954, 1356554236)), ((502551806, 644489505), (1356554237, 1498491936)), ((2667479331, 2679479131), (1498491937, 1510491737)), ((1551009054, 1759996386), (1510491738, 1719479070)), ((4141978550, 4169571317), (1719479071, 1747071838)), ((1759996387, 1865108283), (1747071839, 1852183735)), ((3256553708, 3262777902), (1852183736, 1858407930)), ((727333449, 739672812), (1858407931, 1870747294)), ((791060221, 809853276), (1870747295, 1889540350)), ((644489506, 727333448), (1889540351, 1972384293)), ((809853277, 865464334), (1972384294, 2027995351)), ((1865108284, 1931266149), (2027995352, 2094153217)), ((1065408320, 1080253020), (2094153218, 2108997918)), ((4080669158, 4141978549), (2108997919, 2170307310)), ((2679479132, 2720485562), (2170307311, 2211313741)), ((4025672872, 4080669157), (2211313742, 2266310027)), ((3923624438, 3946384505), (2266310028, 2289070095)), ((3946384506, 4025672871), (2289070096, 2368358461)), ((2236802000, 2299639190), (2368358462, 2431195652)), ((1273931904, 1366401344), (2431195653, 2523665093)), ((3878500457, 3913042115), (2523665094, 2558206752)), ((3247863932, 3256553707), (2558206753, 2566896528)), ((1931266150, 2236801999), (2566896529, 2872432378)), ((3633289978, 3878500456), (2872432379, 3117642857)), ((3262777903, 3633289977), (3117642858, 3488154932)), ((3913042116, 3923624437), (3488154933, 3498737254)), ((3217956599, 3247863931), (3498737255, 3528644587)), ((1080253021, 1273931903), (3528644588, 3722323470)), ((2720485563, 2990467797), (3722323471, 3992305705)), ((2625614674, 2647277658), (3992305706, 4013968690)), ((739672813, 791060220), (4013968691, 4065356098)), ((2990467798, 3217343430), (4065356099, 4292231731)), ((3217343431, 3217956598), (4292231732, 4292844899)), ((500429410, 502551805), (4292844900, 4294967295))], ('light', 'temperature'): [((1671284, 48305626), (0, 46634342)), ((2549881333, 2577982375), (46634343, 74735385)), ((1566215004, 1998304999), (74735386, 506825381)), ((1211085022, 1311086420), (506825382, 606826780)), ((48305627, 452077212), (606826781, 1010598366)), ((3054998249, 3259651350), (1010598367, 1215251468)), ((1998305000, 2116563254), (1215251469, 1333509723)), ((2683491079, 2832994078), (1333509724, 1483012723)), ((2119418493, 2123929712), (1483012724, 1487523943)), ((2344091207, 2549881332), (1487523944, 1693314069)), ((534124760, 887597566), (1693314070, 2046786876)), ((3309446729, 3405255587), (2046786877, 2142595735)), ((2832994079, 2937379482), (2142595736, 2246981139)), ((2123929713, 2150538468), (2246981140, 2273589895)), ((3259651351, 3309446728), (2273589896, 2323385273)), ((2937379483, 3054998248), (2323385274, 2441004039)), ((1311086421, 1566215003), (2441004040, 2696132622)), ((887597567, 1211085021), (2696132623, 3019620077)), ((2577982376, 2683491078), (3019620078, 3125128780)), ((522041548, 528154086), (3125128781, 3131241319)), ((452077213, 522041547), (3131241320, 3201205654)), ((0, 1671283), (3201205655, 3202876938)), ((2150538469, 2344091206), (3202876939, 3396429676)), ((528154087, 534124759), (3396429677, 3402400349)), ((2116563255, 2119418492), (3402400350, 3405255587)), ((4209824659, 4294967295), (4100438569, 4185581205)), ((4100438569, 4209824658), (4185581206, 4294967295))], ('temperature', 'humidity'): [((1046981232, 1106926809), (0, 59945577)), ((717988362, 915086593), (59945578, 257043809)), ((1628903919, 1727295187), (257043810, 355435078)), ((1106926810, 1628903918), (355435079, 877412187)), ((0, 717988361), (877412188, 1595400549)), ((915086594, 1046981231), (1595400550, 1727295187)), ((3825097816, 4294967295), (3115915735, 3585785214)), ((3115915735, 3825097815), (3585785215, 4294967295))], ('humidity', 'location'): [((413575139, 551749092), (0, 138173953)), ((4119345931, 4206715746), (138173954, 225543769)), ((4100328990, 4106051038), (225543770, 231265818)), ((49632084, 413575138), (231265819, 595208873)), ((2352115884, 2649651093), (595208874, 892744083)), ((3060513252, 3435411967), (892744084, 1267642799)), ((3435411968, 3457476376), (1267642800, 1289707208)), ((0, 49632083), (1289707209, 1339339292)), ((864931319, 1403209834), (1339339293, 1877617808)), ((1403209835, 1553868403), (1877617809, 2028276377)), ((1553868404, 2352115883), (2028276378, 2826523857)), ((2649651094, 2854901454), (2826523858, 3031774218)), ((2854901455, 3060513251), (3031774219, 3237386015)), ((3457476377, 4100328989), (3237386016, 3880238628)), ((4106051039, 4119345930), (3880238629, 3893533520)), ((551749093, 864931318), (3893533521, 4206715746))]}

Smallest seed: 79874951

  seed 3969171811 --> soil 3969171811
  soil 3969171811 --> fertilizer 934422079
  fertilizer 934422079 --> water 1865108284
  water 1865108284 --> light 2027995352
  light 2027995352 --> temperature 1244941821
  temperature 1244941821 --> humidity 493450090
  humidity 493450090 --> location 79874951

# ----------
CODE GRAVEYARD

print("\nSmallest locations:")
print(smallest_locations)
print("\nSorted:")
print(sorted(smallest_locations))

end_locations = []
for seed_location in smallest_locations:
    end_locations.append((seed_location, get_location_by_seed(seed_location)))

end_locations.sort(key=lambda x:x[1])
print(end_locations)

print(f"\nSmallest location = {end_locations[0][1]}")
get_location_by_seed(end_locations[0][0], show=True)

# location_mappings = [((0, 55), (0, 55)), ((93, 96), (56, 59)), ((56, 92), (60, 96))]
# What is the lowest location number that corresponds to any of the initial seed numbers?
locations = []
for seed in seeds:
    temp = seed
    for mapping in mappings:
        # ('seed', 'soil'): [((98, 99), (50, 51)), ((50, 97), (52, 99))]
        for section in mappings[mapping]:
            source, destination = section
            source_start, source_end = source
            destination_start, destination_end = destination
            delta = destination_start - source_start
            if source_start <= temp <= source_end:
                temp += delta
                break
    locations.append(temp)
#print(f"\nLowest location number = {min(locations)}")

print("\nStarting the search...\n")

def find_seed(current_category: str, current_value: int) -> None:
    
    print(f"\nCategory: {current_category}")
    print(f"Current value: {current_value}")

    if current_category == "seed":
        for seed_range in seed_ranges:
            start, end = seed_range
            if start <= current_value <= end:
                print(f"Seed {current_value} found")
                return
            else:
                print(f"Seed {current_value} not found")
                return
    else:        
        next_category = reversed_mapping_categories[current_category]
        for boundary in boundaries[next_category]:
            # [((0, 56), 0), ... ]
            current_value = boundary[0][0]
            delta = boundary[1]
            find_seed(next_category, current_value + delta)

for boundary in location_mappings:
    boundary_start, boundary_end = boundary[0]
    print(f"Boundary: {boundary_start}-{boundary_end}")


for boundary in location_mappings:
    # ((0, 56), 0)
    boundaries, delta = boundary
    boundary_start, boundary_end = boundary[0]
    delta = boundary[1]
    print(f"\nStarting from boundary: {boundary_start}-{boundary_end}:")

#find_seed(final_category, current_value + delta)

'''