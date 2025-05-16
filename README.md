# EKF and Monte Carlo Localization Documentation

This documentation covers the implementation of the **Extended Kalman Filter (EKF)** and **Monte Carlo Localization (MCL)**, used in the context of robot localization in a soccer field environment. The main goal is to estimate the robot's position based on noisy measurements and actions.

## 1. Extended Kalman Filter (EKF)

The **Extended Kalman Filter (EKF)** is a nonlinear version of the standard Kalman Filter. It works by linearizing the nonlinear process and measurement models using a first-order Taylor series expansion (i.e., Jacobian matrices).

### EKF Algorithm Overview
The EKF consists of two main steps: **Prediction** and **Update**.

#### Prediction Step:
Given the previous state \( \hat{x}_{k-1} \) and control input \( u_k \), the prediction step updates the state estimate \( \hat{x}_k \) and the covariance \( P_k \).

1. **State Prediction:**

$$
\hat{x}_k^- = f(\hat{x}_{k-1}, u_k)
$$

Where \( f(\hat{x}_{k-1}, u_k) \) is the nonlinear state transition function, and \( \hat{x}_k^- \) is the predicted state.

2. **Covariance Prediction:**

$$
P_k^- = F_{k-1} P_{k-1} F_{k-1}^T + Q_k
$$

Where \( F_{k-1} \) is the Jacobian of the state transition function with respect to the state, and \( Q_k \) is the process noise covariance.

#### Update Step:
When a measurement \( z_k \) becomes available, the state estimate is updated.

1. **Kalman Gain Calculation:**

$$
K_k = P_k^- H_k^T (H_k P_k^- H_k^T + R_k)^{-1}
$$

Where \( H_k \) is the Jacobian of the measurement model, and \( R_k \) is the measurement noise covariance.

2. **State Update:**

$$
\hat{x}_k = \hat{x}_k^- + K_k(z_k - h(\hat{x}_k^-))
$$

Where \( h(\hat{x}_k^-) \) is the nonlinear measurement function.

3. **Covariance Update:**

$$
P_k = (I - K_k H_k) P_k^-
$$

Where \( I \) is the identity matrix.

### Mathematics for EKF
The key to EKF is the **Jacobian matrices** which are used to linearize the nonlinear functions \( f(\hat{x}, u) \) and \( h(\hat{x}) \). These Jacobians are calculated as follows:

1. **State Transition Jacobian:**

$$
F_k = \frac{\partial f(\hat{x}_{k-1}, u_k)}{\partial \hat{x}_{k-1}}
$$

2. **Measurement Jacobian:**

$$
H_k = \frac{\partial h(\hat{x}_k)}{\partial \hat{x}_k}
$$

These derivatives describe how small changes in the state or measurements affect the system's behavior.

## 2. Monte Carlo Localization (MCL)

**Monte Carlo Localization (MCL)**, also known as **Particle Filter Localization**, is a popular method for robot localization in unknown environments. The algorithm maintains a set of particles that represent hypotheses of the robot's position. Over time, these particles are updated based on the robot's movements and sensor measurements.

### MCL Algorithm Overview

MCL uses a probabilistic approach with a set of particles \( \{ p_1, p_2, \dots, p_N \} \) to represent the belief distribution over the robot's state. Each particle consists of a state estimate \( x_i \) and a weight \( w_i \), representing the importance of that particle.

#### Prediction Step (Motion Update):

Given the previous state \( x_{i}^{-} \) and control input \( u_k \), each particle is propagated to a new state based on a motion model:

$$
x_i^- = f(x_{i}^{-1}, u_k) + \epsilon
$$

Where \( f(x_{i}^{-1}, u_k) \) is the motion model, and \( \epsilon \) is the process noise.

#### Update Step (Measurement Update):

Each particle's weight is updated based on the likelihood of the current measurement \( z_k \) given the predicted state \( x_i^- \):

$$
w_i = P(z_k | x_i^-)
$$

Where \( P(z_k | x_i^-) \) is the likelihood of the measurement \( z_k \) given the predicted state \( x_i^- \).

#### Resampling Step:

Particles with low weights are less likely to represent the correct position, so resampling is performed to focus on particles with higher weights. After resampling, the weights of all particles are reset to equal values.

$$
\hat{x} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

Where \( N \) is the number of particles.

### Particle Filter Mathematics

1. **Motion Model:**

$$
x_i^- = f(x_{i}^{-1}, u_k) + \epsilon
$$

2. **Measurement Likelihood:**

$$
w_i = P(z_k | x_i^-)
$$

3. **Resampling:**

$$
\hat{x} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

Where \( x_i^- \) are the predicted states, and \( w_i \) are the updated weights after measurement.

## 3. Conclusion

Both EKF and MCL are effective localization algorithms with their own strengths. EKF is well-suited for environments with smooth, continuous dynamics and measurement models, while MCL excels in highly uncertain environments with discrete states and noisy measurements.

To run these algorithms, you can use the provided `localization.py` script. It allows you to visualize the robot's position and compare the results from the EKF and MCL filters.

---

###  How To Run:
Run the run.bat file & also Docker Image is named as state_estimator.tar placed. You can run the docker image or also can run.bat file

```bash
To Create Docker Image, run the following Command;
docker build -t state_estimator

To Run the Docker Image
$ docker run -it --rm state_estimator  python localization.py pf --seed 0
