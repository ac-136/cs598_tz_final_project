### Code adapted from: https://github.com/yifanzhang-pro/syntax-semantics/blob/main/template-gsm/gsm-0006-1.py

# Origin problem: {"question": "Albert is wondering how much pizza he can eat in one day. 
# He buys 2 large pizzas and 2 small pizzas. A large pizza has 16 slices and a small pizza has 8 slices. 
# If he eats it all, how many pieces does he eat that day?", 
# "answer": "He eats 32 from the largest pizzas because 2 x 16 = <<2*16=32>>32\nHe eats 16 from the small pizza because 2 x 8 = <<2*8=16>>16\nHe eats 48 pieces because 32 + 16 = <<32+16=48>>48\n#### 48"}


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


# Function to generate a problem and its solution
def generate_problem_and_solution_code():
    # Randomly select terms from predefined lists
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    quantity1 = 2
    quantity2 = 2
    # item1, item2 = random.sample(items, 2)
    # place = random.choice(places)
    # county = random.choice(us_counties)
    # county = county['CountyName'] + ", " + county["StateName"]

    # Get initial quantities and their ratios
    # quantity1, quantity2 = get_params_combination()
    item1 = "test"
    item2 = "test"

    # Construct problem statement with specific details
    problem_statement = f"{name} is wondering how much pizza they can eat in one day. "
    problem_statement += f"They buy {quantity1} large pizzas and {quantity2} small pizzas. "
    problem_statement += f"A large pizzas has 16 slices and a small pizza has 8 slices. "
    problem_statement += f"If they eat it all, how many pieces do they eat that day?"

    # Generate solution code with specific variable names and comments
    item1_var = f"packets_of_{item1.replace(' ', '_')}"
    item2_var = f"boxes_of_{item2.replace(' ', '_')}"
    total_var = f"total_pieces"

    solution_code = f"""# Number of pieces in {item1_var}
{item1_var} = {quantity1} * 16  # 16 pieces per large pizza

# Number of pieces in {item2_var}
{item2_var} = {quantity2} * 8  # 8 pieces per small pizza

# Calculating the total number of pieces
{total_var} = {item1_var} + {item2_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    return problem_statement, result

    # # Generate the solution without code (solution_wocode)
    # solution_wocode = f"{name} has {quantity1 * 10} pieces from {quantity1} packets of {item1} and "
    # solution_wocode += f"{quantity2 * 5} pieces from {quantity2} boxes of {item2}. "
    # solution_wocode += f"In total, {name} has {quantity1 * 10} + {quantity2 * 5} = {round(result, 2)} pieces for the gathering."

    # return problem_statement, solution_code, result, solution_wocode

# Function to get integer parameters for quantities
def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate quantities
    quantity1 = random.randint(1, 100)
    quantity2 = random.randint(1, 100)

    return quantity1, quantity2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=100, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/q6--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, result = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "result": str(result), "template_name": 6, "idx": i}) + '\n')
