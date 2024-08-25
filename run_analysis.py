
import os
import subprocess
import time

def run_script(script_name):
    print(f"Running {script_name}...")
    start_time = time.time()
    result = subprocess.run(['python', f'src/{script_name}'], check=True)
    end_time = time.time()
    print(f"Finished running {script_name} in {end_time - start_time:.2f} seconds")
    return result

def main():
    scripts = [
        'data_generation.py',
        'data_import.py',
        'sql_analysis.py',
        'ml_analysis.py',
        'visualizations.py',
        'generate_report.py'
    ]

    for script in scripts:
        try:
            run_script(script)
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
            return

    print("Project execution completed successfully!")
    print("You can find the generated report at: outputs/reports/african_ecommerce_report.pdf")

if __name__ == "__main__":
    main()