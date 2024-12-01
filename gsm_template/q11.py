### Code adapted from https://github.com/yifanzhang-pro/syntax-semantics/blob/main/template-gsm/gsm-0011-1.py

# Origin problem: {"question": "Tobias is buying a new pair of shoes that costs $95. 
# He has been saving up his money each month for the past three months. 
# He gets a $5 allowance a month. He also mows lawns and shovels driveways. 
# He charges $15 to mow a lawn and $7 to shovel. After buying the shoes, he has $15 in change. 
# If he mows 4 lawns, how many driveways did he shovel?", 
# "answer": "He saved up $110 total because 95 + 15 = <<95+15=110>>110\nHe saved $15 from his allowance because 3 x 5 = <<3*5=15>>15\nHe earned $60 mowing lawns because 4 x 15 = <<4*15=60>>60\nHe earned $35 shoveling driveways because 110 - 60 - 15 = <<110-60-15=35>>35\nHe shoveled 5 driveways because 35 / 7 = <<35/7=5>>5\n
# #### 5"}


import random
import math
import json
import argparse
import jsonlines
import os

random.seed(42) # Consistent random generation

first_names = []
with jsonlines.open('../data/top_first_names.jsonl') as reader:
    for line in reader:
        first_names.append(line['first_name'])

last_names = []
with jsonlines.open('../data/top_last_names.jsonl') as reader:
    for line in reader:
        last_names.append(line['last_name'])

# items = []
# with jsonlines.open('../data/items-llm.jsonl') as reader:
#     for line in reader:
#         items.append(line)

# places = []
# with jsonlines.open('../data/places-llm.jsonl') as reader:
#     for line in reader:
#         places.append(line)

# us_counties = []
# with jsonlines.open('../data/us_counties.jsonl') as reader:
#     for line in reader:
#         us_counties.append(line)


def generate_problem_and_solution_code():
    # Lists of random terms
    # activities = ["painting fences", "washing cars", "walking dogs", "babysitting", "tutoring"]
    # objects = ["bicycle", "tablet", "guitar", "camera", "pair of sneakers"]
    
    # Get initial amount and subsequent ratio that ensure an integer result
    # cost, allowance_per_month, charge_per_first_activity, months, change_after_purchase, charge_per_second_activity = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    # first_activity = random.choice(activities)
    # second_activity = random.choice([activity for activity in activities if activity != first_activity])
    # object_to_buy = random.choice(objects)
    # place = random.choice(places)
    # county = random.choice(us_counties)
    # county = county['CountyName'] + ", " + county["StateName"]
    cost = 95
    months = 3
    allowance_per_month = 5
    charge_per_first_activity = 15
    charge_per_second_activity = 7
    change_after_purchase = 15
    num_first_activity = 4

    # Construct problem statement with specific details
    problem_statement = f"{name} is buying a new pair of shoes that costs ${cost}. "
    problem_statement += f"They have been saving up their money each month for the past {months} months. "
    problem_statement += f"They get a ${allowance_per_month} allowance a month. "
    problem_statement += f"They also mow lawns and shovel driveways. "
    problem_statement += f"They charge ${charge_per_first_activity} to mow a lawn and ${charge_per_second_activity} to shovel. "
    problem_statement += f"After buying the shoes, they have ${change_after_purchase} in change. "
    problem_statement += f"If they mow {num_first_activity} lawns, how many driveways did they shovel?"

    object_to_buy = "shoes"
    first_activity = "mow"
    second_activity = "shovel"

    # Generate solution code with specific variable names and comments
    total_savings_var = f"total_savings_for_{object_to_buy.replace(' ', '_')}"
    allowance_var = f"total_allowance"
    first_activity_income_var = f"income_from_{first_activity.replace(' ', '_')}"
    second_activity_times_var = f"{second_activity.replace(' ', '_')}_times"

    solution_code = f"""# Total amount saved for the {object_to_buy}
{total_savings_var} = {cost} + {change_after_purchase}

# Total allowance received
{allowance_var} = {months} * {allowance_per_month}

# Income from {first_activity}
{first_activity_income_var} = {num_first_activity} * {charge_per_first_activity}

# Calculating the number of times {second_activity} was performed
{second_activity_times_var} = ({total_savings_var} - {allowance_var} - {first_activity_income_var}) // {charge_per_second_activity}

result = {second_activity_times_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    return problem_statement, result

    # # Generate the solution without code (solution_wocode)
    # total_savings = cost + change_after_purchase
    # total_allowance = months * allowance_per_month
    # first_activity_income = months * charge_per_first_activity
    # solution_wocode = f"{name} saved up ${total_savings} total because ${cost} + ${change_after_purchase} = ${total_savings}\n"
    # solution_wocode += f"They saved ${total_allowance} from their allowance because {months} x ${allowance_per_month} = ${total_allowance}\n"
    # solution_wocode += f"They earned ${first_activity_income} by {first_activity} because {months} x ${charge_per_first_activity} = ${first_activity_income}\n"
    # solution_wocode += f"They performed {second_activity} {result} times because ${total_savings} - ${first_activity_income} - ${total_allowance} = {result}"

    # return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate cost, allowance, charge, and change
        cost = random.randint(50, 500)
        allowance_per_month = random.randint(5, 20)
        charge_per_first_activity = random.randint(10, 30)
        months = random.randint(1, 12)
        change_after_purchase = random.randint(1, 49)
        charge_per_second_activity = random.randint(10, 30)

        # Calculate total savings
        total_savings = cost + change_after_purchase

        # Ensure the total savings minus allowance and first activity income is non-negative
        remaining_amount = total_savings - (months * allowance_per_month) - (months * charge_per_first_activity)
        if remaining_amount >= 0 and remaining_amount % charge_per_second_activity == 0:
            return cost, allowance_per_month, charge_per_first_activity, months, change_after_purchase, charge_per_second_activity



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=100, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/q11--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, result = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "result": str(result), "template_name": 11, "idx": i}) + '\n')