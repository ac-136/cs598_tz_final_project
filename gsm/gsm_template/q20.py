### Code adapted from https://github.com/yifanzhang-pro/syntax-semantics/blob/main/template-gsm/gsm-0020-1.py

# Origin problem: {"question": "Bella bought stamps at the post office. 
# Some of the stamps had a snowflake design, some had a truck design, and some had a rose design. 
# Bella bought 11 snowflake stamps. She bought 9 more truck stamps than snowflake stamps, and 13 fewer rose stamps than truck stamps. 
# How many stamps did Bella buy in all?", "answer": "The number of truck stamps is 11 + 9 = <<11+9=20>>20.\nThe number of rose stamps is 20 \u2212 13 = <<20-13=7>>7.\nBella bought 11 + 20 + 7 = <<11+20+7=38>>38 stamps in all.\n
# #### 38"}


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
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1 = "snowflake"
    item2 = "truck"
    item3 = "rose"
    # item1, item2, item3 = random.sample(items, 3)
    # place = random.choice(places)
    # county = random.choice(us_counties)
    # county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    item3_var = item3.replace(' ', '_')
    # county_var = county.replace(' ', '_')

    # # Get initial quantity and differences
    # initial_quantity, diff1, diff2 = get_params_combination()



    initial_quantity = 11
    diff1 = 9
    diff2 = 13

    # Construct problem statement
    problem_statement = f"{name} bought stamps at the post office. "
    problem_statement += f"Some of the stamps had a {item1} design, some had a {item2} design, and some had a {item3} design. "
    problem_statement += f"{name} bought {initial_quantity} {item1} stamps. "
    problem_statement += f"They bought {diff1} more {item2} stamps than {item1} stamps, and {diff2} fewer {item3} stamps than {item2} stamps. "
    problem_statement += f"How many stamps did {name} buy in all?"

    # Generate solution code
    solution_code = f"""# Initial quantity of {item1}
{item1_var} = {initial_quantity}

# Quantity of {item2}
{item2_var} = {item1_var} + {diff1}

# Quantity of {item3}
{item3_var} = {item2_var} - {diff2}

# Total quantity collected
total_items = {item1_var} + {item2_var} + {item3_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['total_items']

    return problem_statement, result

    # # Generate the solution without code
    # solution_wocode = f"{name} collected {initial_quantity} {item1}, {initial_quantity + diff1} {item2}, "
    # solution_wocode += f"and {initial_quantity + diff1 - diff2} {item3}. In total, they collected "
    # solution_wocode += f"{initial_quantity} + {initial_quantity + diff1} + {initial_quantity + diff1 - diff2} = "
    # solution_wocode += f"{round(result, 2)} items."

    # return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    initial_quantity = random.randint(1, 100)
    diff1 = random.randint(1, 20)
    diff2 = random.randint(1, 20)
    return initial_quantity, diff1, diff2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=100, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/q20--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, result = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "result": str(result), "template_name":20, "idx": i}) + '\n')