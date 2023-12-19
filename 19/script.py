# Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

import sys

data_file = sys.argv[1]

"""
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

with open(data_file) as f:
    lines = f.read().splitlines()

separator = lines.index("")

workflows_as_strings = lines[:separator]
workflows = {}
# {'px': [('a', '<', '2006', 'qkq'), ..., 'hdj': [('m', '>', '838', 'A'), 'pv']}

# Parse workflows
for workflow in workflows_as_strings:
    # px{a<2006:qkq,m>2090:A,rfg}
    # workflow_name {condition_n: effect_n, next }
    workflow_name, workflow_steps = workflow[:-1].split("{")
    parsed_workflow = []
    for workflow_step in workflow_steps.split(","):
        if ":" in workflow_step:
            # a<2006:qkq
            condition, effect = workflow_step.split(":")
            symbol = condition[0]
            operator = condition[1]
            value = condition[2:]
            parsed_workflow.append((symbol, operator, value, effect))
        else:
            parsed_workflow.append(workflow_step)
    workflows[workflow_name] = parsed_workflow


part_ratings_as_strings = lines[separator + 1 :]
part_ratings = []
# [{'x': '787', 'm': '2655', 'a': '1222', 's': '2876'}, ...]

# Parse part ratings
for part_string in part_ratings_as_strings:
    # {x=787,m=2655,a=1222,s=2876}
    part_rating = {}
    for cateogry_and_value in part_string[1:-1].split(","):
        # x=787
        category, value = cateogry_and_value.split("=")
        part_rating[category] = int(value)
    part_ratings.append(part_rating)

print(f"{len(workflows)} workflows")
print(f"{len(part_ratings)} part ratings")

accepted = []
rejected = []


for part in part_ratings:
    print(f"\nProcessing part {part}")
    current_workflow_name = "in"
    while True:
        if current_workflow_name == "A":
            print("Part accepted.\n")
            accepted.append(part)
            break
        if current_workflow_name == "R":
            print("Part rejected.\n")
            rejected.append(part)
            break
        current_workflow = workflows[current_workflow_name]
        print(f"\nCurrent workflow = {current_workflow_name}: {current_workflow}")
        # Current workflow = in: [('s', '<', '1351', 'px'), 'qqz']
        for workflow_step in current_workflow:
            print(f"Current workflow step = {workflow_step}")
            if type(workflow_step) is tuple:
                symbol, operator, value, effect = workflow_step
                expression = str(part[symbol]) + operator + value
                if eval(expression):
                    current_workflow_name = effect
                    print(f"{expression} (TRUE)")
                    print(f"Continuing to workflow {current_workflow_name}")
                    break
                else:
                    print(f"{expression} (FALSE)")
            else:
                current_workflow_name = workflow_step
                break

print(f"Accepted parts: {accepted}")
print(f"Rejected parts: {rejected}")

total = 0
for part in accepted:
    total += sum(part.values())

print(f"Sum of all the rating numbers for accepted parts: {total}")
