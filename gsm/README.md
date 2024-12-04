# Tests on GSM8K data details

## Description
### Folders
- **data**: jsonl files that are used to create ablations and evolved datasets. For example, top_first_names.jsonl are used to create random names. 
- **gsm_evolved**: 20 python files that create 20 different evolved problems based on 20 problems from the gsm8k dataset. All results from the different python files write to output/gsm_evolved_20.jsonl
- **gsm_evolved_ablations**: jsonl files that contain 100 ablations for each of the 20 evolved problems as listed in gsm_evolved/output/gsm_evolved_20.jsonl
- **gsm_template**: 20 python files that create ablations for 20 questions from the original gsm8k dataset. The abalations are outputted to jsonl files in gsm_template/output

### Code
- **ablate_gsm8k_evolved.ipynb**: run to create ablations for the gsm8k evolved dataset. 
- **ablated_evolved_gsm8k_eval.ipynb**: run to evaluate the performance on the evolved and ablated gsm8k dataset using gpt
- **ablated_gsm8k_eval.ipynb**: run to evaluate the performance on the ablated original gsm8k dataset using gpt
- **gsm8k_eval.ipynb**: run to evaluate the performance on the original gsm8k dataset using gpt
- **gsm8k_evolved_eval.ipynb**: run to evaluate the performance on the evolved gsm8k dataset using gpt

## Results 
Results of different models and temperatures are in the results.xlsx spreadsheet