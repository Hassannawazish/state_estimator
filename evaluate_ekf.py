import subprocess
import numpy as np
import matplotlib.pyplot as plt

r_values = [1/64, 1/16, 1/4, 1, 4, 16, 64]
num_trials = 10

def run_trial(data_factor, filter_factor, seed):
    result = subprocess.run(
        ['python', 'localization.py', 'ekf',
         '--data-factor', str(data_factor),
         '--filter-factor', str(filter_factor),
         '--seed', str(seed)],
        capture_output=True, text=True
    )
    out = result.stdout
    try:
        pos_error = float(out.split("Mean position error:")[1].split("\n")[0].strip())
        anees = float(out.split("ANEES:")[1].strip())
        return pos_error, anees
    except Exception as e:
        print("Error parsing output:", e)
        print(out)
        return None, None

def run_experiment(data_fixed=True):
    mean_errors = []
    mean_anees = []

    for r in r_values:
        errors = []
        anees_values = []
        print(f"\nRunning for r = {r} ...")
        for seed in range(num_trials):
            data_factor = 1 if data_fixed else r
            filter_factor = r
            pos_error, anees = run_trial(data_factor, filter_factor, seed)
            if pos_error is not None:
                errors.append(pos_error)
                anees_values.append(anees)
        mean_errors.append(np.mean(errors))
        mean_anees.append(np.mean(anees_values))

    return mean_errors, mean_anees

print("Running Exercise 3(b): Vary both data & filter noise")
errors_b, anees_b = run_experiment(data_fixed=False)

print("\nRunning Exercise 3(c): Fix data, vary only filter noise")
errors_c, anees_c = run_experiment(data_fixed=True)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(r_values, errors_b, 'o-', label='3(b): Data & Filter noise vary')
plt.plot(r_values, errors_c, 's--', label='3(c): Filter noise only')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.legend()
plt.title('Mean Position Error vs. Noise Scaling')

plt.subplot(1, 2, 2)
plt.plot(r_values, anees_b, 'o-', label='3(b): Data & Filter noise vary')
plt.plot(r_values, anees_c, 's--', label='3(c): Filter noise only')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('ANEES')
plt.xscale('log')
plt.legend()
plt.title('ANEES vs. Noise Scaling')

plt.tight_layout()
plt.show()
