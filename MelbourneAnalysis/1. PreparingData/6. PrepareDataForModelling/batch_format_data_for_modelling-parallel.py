#Parallel version of the script. See the other script for more details.
import papermill as pm
import os
from concurrent.futures import ThreadPoolExecutor

# Drop 50m buffer as we should have already run the script once with this buffer size
BUFFER_SIZES = [100, 200, 400, 500, 600, 1000]
INPUT_NOTEBOOK = "FormatDataForModelling.ipynb"
OUTPUT_DIR = "."

os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_notebook(buffer_size):
    OUTPUT_NOTEBOOK = f"{OUTPUT_DIR}/Temp_Notebook_BufferSize_{buffer_size}.ipynb"
    print(f"Running for buffer size: {buffer_size}: {OUTPUT_NOTEBOOK}")
    pm.execute_notebook(
        INPUT_NOTEBOOK,
        OUTPUT_NOTEBOOK,
        parameters={"buffer_size_m": buffer_size}
    )

# Use ThreadPoolExecutor to run the notebooks in parallel
with ThreadPoolExecutor() as executor:
    executor.map(run_notebook, BUFFER_SIZES)