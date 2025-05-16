import subprocess
import numpy as np
import matplotlib.pyplot as plt

r_values = [1/64, 1/16, 1/4, 1, 4, 16, 64]
num_trials = 10
particle_counts = [20, 50, 500]

def run_trial(data_factor, filter_factor, seed, num_particles=100):
    result = subprocess.run(
        ['python', 'localization.py', 'pf',
         '--data-factor', str(data_factor),
         '--filter-factor', str(filter_factor),
         '--seed', str(seed),
         '--num-particles', str(num_particles)],
        capture_output=True, text=True
    )
    out = result.stdout
    try:
        pos_error = float(out.split("Mean Position Error :")[1].split("\n")[0].strip())
        anees = float(out.split("ANEES:")[1].strip())
        return pos_error, anees
    except Exception as e:
        print("Error parsing output:", e)
        print(out)
        return None, None

def run_experiment(data_fixed=True, num_particles=100):
    mean_errors = []
    mean_anees = []

    for r in r_values:
        errors = []
        anees_values = []
        print(f"\nRunning for r = {r}, particles = {num_particles} ...")
        for seed in range(num_trials):
            data_factor = 1 if data_fixed else r
            filter_factor = r
            pos_error, anees = run_trial(data_factor, filter_factor, seed, num_particles)
            if pos_error is not None:
                errors.append(pos_error)
                anees_values.append(anees)
        mean_errors.append(np.mean(errors))
        mean_anees.append(np.mean(anees_values))

    return mean_errors, mean_anees

print("Exercise 4(b): Vary data + filter noise")
errors_b, anees_b = run_experiment(data_fixed=False)

print("\nExercise 4(c): Fix data, vary filter noise only")
errors_c, anees_c = run_experiment(data_fixed=True)

errors_d = {}
anees_d = {}

for n in particle_counts:
    print(f"\nExercise 4(d): Vary noise (r) with {n} particles")
    e, a = run_experiment(data_fixed=True, num_particles=n)
    errors_d[n] = e
    anees_d[n] = a

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.plot(r_values, errors_b, 'o-', label='4(b): Data + Filter noise')
plt.plot(r_values, errors_c, 's--', label='4(c): Filter noise only')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.title('Mean Position Error (4b & 4c)')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(r_values, anees_b, 'o-', label='4(b): Data + Filter noise')
plt.plot(r_values, anees_c, 's--', label='4(c): Filter noise only')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('ANEES')
plt.xscale('log')
plt.title('ANEES (4b & 4c)')
plt.legend()

plt.subplot(1, 3, 3)
for n in particle_counts:
    plt.plot(r_values, errors_d[n], label=f'{n} particles')
plt.xlabel('r (noise scaling factor)')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.title('Effect of Particle Count (4d)')
plt.legend()

plt.tight_layout()
plt.show()
