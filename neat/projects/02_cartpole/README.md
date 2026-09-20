# Project 2: Pole Balancing (Cart-Pole) Control with NEAT

## 1. Problem Statement
The inverted pendulum on a cart (Cart-Pole) is a classic benchmark in dynamic control theory and reinforcement learning. An unactuated pole is attached by an un-motorized joint to a cart moving along a frictionless 1D track. The controller must apply discrete horizontal forces ($F = \pm 10.0\text{ N}$) to keep the pole balanced vertically within $\pm 12^\circ$ and the cart within the track limits $x \in [-2.4, +2.4]\text{ m}$.

```
       |\    Pole (mass m=0.1 kg, length 2l=1.0 m)
       | \  Angle theta (|theta| <= 12 deg)
       |  \
     [======] Cart (mass M=1.0 kg)
     O      O  Position x (|x| <= 2.4 m), Force F = +/- 10 N
   ====================================================
```

## 2. Mathematical Dynamics (Euler-Lagrange)
The equations of motion are derived from the system Lagrangian $L = T - V$:
$$\ddot{\theta} = \frac{g \sin\theta + \cos\theta \left( \frac{-F - m l \dot{\theta}^2 \sin\theta}{M + m} \right)}{l \left( \frac{4}{3} - \frac{m \cos^2\theta}{M + m} \right)}$$
$$\ddot{x} = \frac{F + m l \left( \dot{\theta}^2 \sin\theta - \ddot{\theta} \cos\theta \right)}{M + m}$$

The state is numerically integrated using the **Symplectic Euler-Cromer** method with time step $\Delta t = 0.02\text{ s}$:
$$\dot{x}_{t+1} = \dot{x}_t + \Delta t \cdot \ddot{x}_t, \quad x_{t+1} = x_t + \Delta t \cdot \dot{x}_{t+1}$$
$$\dot{\theta}_{t+1} = \dot{\theta}_t + \Delta t \cdot \ddot{\theta}_t, \quad \theta_{t+1} = \theta_t + \Delta t \cdot \dot{\theta}_{t+1}$$

## 3. NEAT Controller Specification
- **Inputs (4 normalized state variables)**:
  1. Normalized position: $x / 2.4$
  2. Normalized velocity: $\dot{x} / 3.0$
  3. Normalized pole angle: $\theta / 0.2094$
  4. Normalized angular velocity: $\dot{\theta} / 3.0$
  5. Bias: $1.0$ (automatic)
- **Output (1 neuron)**:
  - Sigmoid activation $a \in [0, 1]$.
  - Force: $+10.0\text{ N}$ if $a > 0.5$ else $-10.0\text{ N}$.
- **Fitness Evaluation**: Evaluated over 3 distinct initial perturbation angles ($\theta_0 \in \{-0.05, 0.0, +0.05\}\text{ rad}$). Total fitness is the sum of steps survived (maximum $3 \times 500 = 1500\text{ steps}$).

## 4. Running the Project
Train the NEAT controller:
```bash
python3 neat/projects/02_cartpole/train_cartpole.py
```

Evaluate the controller over multi-trial validation runs and record telemetry:
```bash
python3 neat/projects/02_cartpole/evaluate_controller.py
```

## 5. Visual Artifacts
Generated in `neat/projects/02_cartpole/output/`:
- `cartpole_trajectory.png`: Telemetry trajectories showing cart position $x(t)$ and pole angle $\theta(t)$ smoothly stabilized over 500 steps.
- `cartpole_fitness.png`: Population fitness convergence history over generations.
- `cartpole_network.png`: Diagram of the evolved neural network controller topology.
