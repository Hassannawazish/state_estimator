import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os  


if not os.path.exists('results'):
    os.makedirs('results') 
noise_factors = [1/64, 1/16, 1/4, 1, 4, 16, 64]
num_trials = 10
particle_options = [20, 50, 500]  # For Exercise 4(d)

def execute_trial(data_factor, filter_factor, seed, num_particles=100):
    result = subprocess.run(
        ['python', 'localization.py', 'pf',
        '--data-factor', str(data_factor),
        '--filter-factor', str(filter_factor),
        '--seed', str(seed),
        '--num-particles', str(num_particles)],
        capture_output=True, text=True
    )
    output = result.stdout
    try:
        position_error = float(output.split("Mean position error:")[1].split("\n")[0].strip())
        anees_value = float(output.split("ANEES:")[1].strip())
        return position_error, anees_value
    except Exception as e:
        print("Error parsing output:", e)
        print(output)
        return None, None

def run_simulation(data_fixed=True, num_particles=100):
    position_errors = []
    anees_values = []

    for noise_factor in noise_factors:
        errors = []
        anees_list = []
        print(f"\nRunning for noise_factor = {noise_factor}, particles = {num_particles} ...")
        for seed in range(num_trials):
            data_factor = 1 if data_fixed else noise_factor
            filter_factor = noise_factor
            pos_error, anees = execute_trial(data_factor, filter_factor, seed, num_particles)
            if pos_error is not None:
                errors.append(pos_error)
                anees_list.append(anees)
        position_errors.append(np.mean(errors))
        anees_values.append(np.mean(anees_list)) 
    return position_errors, anees_values


print("Exercise 4(b): Vary data + filter noise")
position_errors_b, anees_b = run_simulation(data_fixed=False)

print("\nExercise 4(c): Fix data, vary filter noise only")
position_errors_c, anees_c = run_simulation(data_fixed=True)

position_errors_d = {}
anees_d = {}
for particle_count in particle_options:
    print(f"\nExercise 4(d): Vary noise (noise_factor) with {particle_count} particles")
    e, a = run_simulation(data_fixed=True, num_particles=particle_count)
    position_errors_d[particle_count] = e
    anees_d[particle_count] = a

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.plot(noise_factors, position_errors_b, 'o-', label='4[b]: Data + Filter noise')
plt.plot(noise_factors, position_errors_c, 's--', label='4[c]: Filter noise only')
plt.xlabel('Noise Scaling Factor [r]')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.title('Mean Position Error [4b & 4c]')
plt.legend()


plt.savefig('results/mean_position_error.png')
plt.subplot(1, 3, 2)
plt.plot(noise_factors, anees_b, 'o-', label='4(b): Data + Filter noise')
plt.plot(noise_factors, anees_c, 's--', label='4(c): Filter noise only')
plt.xlabel('Noise Scaling Factor (r)')
plt.ylabel('ANEES')
plt.xscale('log')
plt.title('ANEES [4b & 4c]')
plt.legend() 

plt.savefig('results/anees.png')
plt.subplot(1, 3, 3)
for particle_count in particle_options:
    plt.plot(noise_factors, position_errors_d[particle_count], label=f'{particle_count} particles')
plt.xlabel('Noise Scaling Factor [r]')
plt.ylabel('Mean Position Error')
plt.xscale('log')
plt.title('Effect of Particle Count [4d]')
plt.legend()


plt.savefig('results/effect_of_particle_count.png') 
plt.tight_layout()
plt.show()