from eval_run import eval_and_save_metrics
import sys

try:
    folderNameOverride = sys.argv[1]
except:
    folderNameOverride = None

folderName = sys.argv[2]

run_results = f'results/{folderName}'
eval_and_save_metrics(run_results, folderNameOverride)


