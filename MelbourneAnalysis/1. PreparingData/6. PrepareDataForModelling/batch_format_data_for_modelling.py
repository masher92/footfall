# Run the FormatDataForModelling notebook automatically for different buffer sizes
# Additionally creates Temporary notebooks that can be deleted afterwards
# Note that you should FormatDataForModelling.ipynb at least once so the cache
# that links the sensors to census data can be created.
import papermill as pm
import os

# Drop 50m buffer as we should have already run the script once with this buffer size (to create the cache
# needed for linking sensors to census data)
#BUFFER_SIZES = [50, 100, 200, 400, 500, 600, 1000]
BUFFER_SIZES = [50, 100, 200, 500, 600, 1000]  # Default value of 400m removed as this is done in the first run of the script
INPUT_NOTEBOOK = "FormatDataForModelling.ipynb"
OUTPUT_DIR = "."

os.makedirs(OUTPUT_DIR, exist_ok=True)

for BUFFER_SIZE in BUFFER_SIZES:
    OUTPUT_NOTEBOOK = f"{OUTPUT_DIR}/Temp_Notebook_BufferSize_{BUFFER_SIZE}.ipynb"
    print(f"Running for buffer size: {BUFFER_SIZE}: {OUTPUT_NOTEBOOK}")
    pm.execute_notebook(
        INPUT_NOTEBOOK,
        OUTPUT_NOTEBOOK,
        parameters={"buffer_size_m": BUFFER_SIZE}
    )
