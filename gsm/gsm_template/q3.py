### Code adpated from: https://github.com/yifanzhang-pro/syntax-semantics/blob/main/template-gsm/gsm-0003-1.py

# Origin problem: {"question": "Julie is reading a 120-page book. Yesterday, she was able to read 12 pages and today, she 
# read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages 
# should she read?", "answer": "Maila read 12 x 2 = <<12*2=24>>24 pages today.\n
# So she was able to read a total of 12 + 24 = <<12+24=36>>36 pages since yesterday.\nThere are 120 - 36 = <<120-36=84>>84 pages
# left to be read.\nSince she wants to read half of the remaining pages tomorrow, then she should read 84/2 = <<84/2=42>>42 pages.\n#### 42"}


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


import random
import math

def generate_problem_and_solution_code():
    # Lists of random terms
    # books = ["novel", "biography", "textbook", "cookbook", "guidebook", "manual"]

    # Get initial pages and subsequent reading ratio ensuring an integer result
    # initial_pages, subsequent_ratio = get_params_combination()



    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    book_lenth = 120
    initial_pages = 12
    # book = random.choice(books)
    # day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    # place = random.choice(places)
    # county = random.choice(us_counties)
    # county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} is reading a {book_lenth}-page book. "
    problem_statement += f"Yesterday, they were able to read {initial_pages} pages and today, they read twice as many pages as yesterday. "
    problem_statement += f"If they want to read half of the remaining pages tomorrow, how many pages should they read?"

    # Generate solution code with specific variable names and comments
    pages_var = f"pages_read_on_first_day"
    ratio_var = f"reading_ratio"
    total_var = f"total_pages_read"
    pages_left = f"pages_left"

    solution_code = f"""# Number of pages read by {name} on the first day
{pages_var} = {initial_pages}

# Reading ratio for the second day
{ratio_var} = {2}

# Calculating the amount of pages read on the second day
# by applying the ratio to the initial pages read
second_day_{pages_var} = {pages_var} * {ratio_var}

# Calculating the total number of pages read during the first two days
{total_var} = {pages_var} + second_day_{pages_var}

{pages_left} = {book_lenth} - {total_var}

result = {pages_left} // {2}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])

    return problem_statement, result

    # # Generate the solution without code
    # solution_wocode = f"{name} read {initial_pages} pages on the first day. "
    # solution_wocode += f"On the second day, they read {round(subsequent_ratio*initial_pages)} pages. "
    # solution_wocode += f"In total, {name} read {initial_pages} + {round(subsequent_ratio*initial_pages)} = {round(result)} pages during the first two days."

    # return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Prefer integer parameters and ensure numbers have a finite number of digits.
    """
    while True:
        # Randomly generate initial pages read
        initial_pages = random.randint(10, 300)

        # Randomly generate subsequent reading ratio
        subsequent_ratio = round(random.uniform(1.1, 3.0), 2)

        # Calculate the total pages read on the second day
        total_pages_second_day = initial_pages * subsequent_ratio

        # Check if the total is close to an integer
        if math.isclose(total_pages_second_day, round(total_pages_second_day), rel_tol=1e-15):
            return initial_pages, subsequent_ratio



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=100, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/q3--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, result = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "result": str(result), "template_name": 3, "idx": i}) + '\n')