import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

noise_factors = [1/64, 1/16, 1/4, 1, 4, 16, 64]
num_repeats = 10

if not os.path.exists('results'):
    os.makedirs('results')

def execute_trial(input_data_factor, filter_noise_factor, random_seed):
    process_result = subprocess.run(
        ['python', 'localization.py', 'ekf',
         '--data-factor', str(input_data_factor),
         '--filter-factor', str(filter_noise_factor),
         '--seed', str(random_seed)],
        capture_output=True, text=True
    )
    output = process_result.stdout
    try:
        position_error = float(output.split("Mean position error:")[1].split("\n")[0].strip())
        anees_value = float(output.split("ANEES:")[1].strip())
        return position_error, anees_value
    except Exception as error:
        print("Error while parsing output:", error)
        print(output)
        return None, None

def perform_experiment(is_data_fixed=True):
    avg_errors = []
    avg_anees = []

    for noise in noise_factors:
        trial_errors = []
        trial_anees = []
        print(f"\nExecuting trials for noise factor = {noise} ...")
        for seed_value in range(num_repeats):
            data_factor = 1 if is_data_fixed else noise
            filter_factor = noise
            pos_error, anees = execute_trial(data_factor, filter_factor, seed_value)
            if pos_error is not None:
                trial_errors.append(pos_error)
                trial_anees.append(anees)
        avg_errors.append(np.mean(trial_errors))
        avg_anees.append(np.mean(trial_anees))

    return avg_errors, avg_anees

print("Initiating Experiment 3[b]: Vary both data and filter noise")
errors_experiment_b, anees_experiment_b = perform_experiment(is_data_fixed=False)

print("\nInitiating Experiment 3[c]: Fix data, vary only filter noise")
errors_experiment_c, anees_experiment_c = perform_experiment(is_data_fixed=True)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(noise_factors, errors_experiment_b, 'o-', label='3[b]: Data & Filter noise vary')
plt.plot(noise_factors, errors_experiment_c, 's--', label='3[c]: Filter noise only')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.legend()
plt.title('Mean Position Error vs. Noise Scaling')

plt.subplot(1, 2, 2)
plt.plot(noise_factors, anees_experiment_b, 'o-', label='3[b]: Data & Filter noise vary')
plt.plot(noise_factors, anees_experiment_c, 's--', label='3[c]: Filter noise only')
plt.xlabel('r (Noise Scaling Factor)')
plt.ylabel('ANEES')
plt.xscale('log')
plt.legend()
plt.title('ANEES vs. Noise Scaling')

plt.tight_layout()
plt.savefig('results/ekf_experiment_results.png')
plt.show()
