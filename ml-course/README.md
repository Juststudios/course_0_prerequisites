# Applied Machine Learning with Mathematics

## A Complete, Math-First ML Course

This course takes you from **understanding the mathematics** to **building and evaluating models**.

Every algorithm is taught in this exact order:

```
Real Problem
     ↓
Why Machine Learning?
     ↓
Intuition
     ↓
Mathematics (with symbols explained)
     ↓
Tiny numerical example by hand
     ↓
NumPy implementation from scratch
     ↓
Scikit-Learn implementation
     ↓
Visualization
     ↓
Evaluation
     ↓
Limitations
     ↓
Real-world application
```

---

## Prerequisites

You should already know:
- **Python**: variables, conditions, loops, functions, lists (`python-data-tools/` or `lesson.py`)
- **NumPy**: arrays, shapes, operations, statistics (`python-data-tools/lessons/01_numpy/`)
- **Pandas**: DataFrames, filtering, cleaning (`python-data-tools/lessons/02_pandas/`)
- **Matplotlib**: plots and visualization (`python-data-tools/lessons/03_matplotlib/`)
- **Engineering Math**: linear algebra, calculus, probability (`engineering-mathematics/`)

---

## Course Map

### Part 0 — Mathematical Foundations (Python Version)

The engineering-mathematics/ directory taught these concepts in MATLAB.
This part bridges them into Python/NumPy — the tools you'll use for ML.

| Module | Topic | Key Concepts |
|---|---|---|
| [00_foundations/A_vectors_matrices.py](00_foundations/A_vectors_matrices.py) | Vectors & Matrices | dot products, matrix multiply, data representation |
| [00_foundations/B_functions.py](00_foundations/B_functions.py) | Functions | linear/nonlinear, composition, model notation |
| [00_foundations/C_statistics.py](00_foundations/C_statistics.py) | Statistics | mean, variance, std, correlation |
| [00_foundations/D_probability.py](00_foundations/D_probability.py) | Probability | distributions, expected value, uncertainty |
| [00_foundations/E_derivatives.py](00_foundations/E_derivatives.py) | Derivatives | slope, gradient, partial derivatives |
| [00_foundations/F_optimization.py](00_foundations/F_optimization.py) | Optimization | loss functions, gradient descent, minima |

---

### Part 1 — ML Fundamentals

| Module | Topic |
|---|---|
| [01_what_is_ml/](01_what_is_ml/) | Traditional programming vs ML, supervised/unsupervised |
| [02_ml_workflow/](02_ml_workflow/) | Problem → Data → Train → Evaluate pipeline |
| [03_train_test_split/](03_train_test_split/) | Why test sets matter, data leakage |

---

### Part 2 — Classical ML Algorithms (Math-First)

| Module | Topic | Core Math |
|---|---|---|
| [04_linear_regression/](04_linear_regression/) | Linear Regression | ŷ = wx + b, MSE, Normal Equation |
| [05_logistic_regression/](05_logistic_regression/) | Logistic Regression | Sigmoid, Cross-Entropy |
| [06_knn/](06_knn/) | K-Nearest Neighbors | Euclidean distance, voting |
| [07_decision_trees/](07_decision_trees/) | Decision Trees | Entropy, Information Gain |
| [08_random_forest/](08_random_forest/) | Random Forest | Bagging, ensemble averaging |
| [09_svm/](09_svm/) | Support Vector Machines | Hyperplane, margin, kernel |
| [10_kmeans/](10_kmeans/) | K-Means Clustering | Centroid, objective function |
| [11_pca/](11_pca/) | Principal Component Analysis | Eigenvectors, variance, projection |

---

### Part 3 — Neural Networks from Scratch

| Module | Topic | Core Math |
|---|---|---|
| [12_perceptron/](12_perceptron/) | Perceptron | Weighted sum, step function |
| [13_forward_propagation/](13_forward_propagation/) | Forward Propagation | Z = XW + b, layer-by-layer |
| [14_activation_functions/](14_activation_functions/) | Activations | Sigmoid, ReLU, Tanh, Softmax |
| [15_loss_functions/](15_loss_functions/) | Loss Functions | MSE, Cross-Entropy |
| [16_gradient_descent/](16_gradient_descent/) | Gradient Descent | dL/dw, update rule |
| [17_backpropagation/](17_backpropagation/) | Backpropagation | Chain rule, gradient flow |
| [18_numpy_neural_network/](18_numpy_neural_network/) | Manual NN | Full network in NumPy |
| [19_pytorch_bridge/](19_pytorch_bridge/) | PyTorch Bridge | Tensors, autograd, modules |

---

### Part 4 — Evaluation & Engineering

| Module | Topic |
|---|---|
| [20_model_evaluation/](20_model_evaluation/) | Metrics: MAE, RMSE, R², Accuracy, F1, Confusion Matrix |
| [21_bias_variance/](21_bias_variance/) | Overfitting, underfitting, complexity |
| [22_feature_scaling/](22_feature_scaling/) | Normalization, standardization, z-score |
| [23_regularization/](23_regularization/) | L1, L2, Ridge, Lasso |

---

### Part 5 — Projects & Assessment

| Module | Topic |
|---|---|
| [24_complete_project/](24_complete_project/) | End-to-end ML pipeline |
| [25_algorithm_comparison/](25_algorithm_comparison/) | Compare all algorithms on one problem |
| [exercises/](exercises/) | 5-level exercises per topic |
| [reference/](reference/) | Formula sheets and mathematics map |
| [capstone/](capstone/) | Independent project with report |

---

## The Mathematics → ML Map

```
Linear Algebra          Statistics              Calculus
(vectors, matrices,     (mean, variance,        (derivatives,
 dot products,           correlation,            partial derivatives,
 eigenvectors)           distributions)          gradients)
      ↓                       ↓                       ↓
 Data Representation     Evaluation             Optimization
 (X matrix,              (metrics,              (gradient descent,
  feature spaces,         uncertainty,           loss minimization,
  transformations)        model fit)             backpropagation)
           ↘                  ↓                 ↙
                        ML Algorithms
                   (learning = optimization
                    over a loss function
                    defined on data)
```

---

## Running the Course

```bash
# Install dependencies
pip install numpy pandas matplotlib scikit-learn

# Run any lesson directly
python ml-course/04_linear_regression/01_math_and_intuition.py

# Run exercises
python ml-course/exercises/04_linear_regression_questions.py
```

---

## Philosophy

> **"I understand what this algorithm is trying to do, the mathematics behind it,
>   how the mathematics becomes code, how to train it, how to evaluate it,
>   when it is appropriate, and what its limitations are."**

This is the standard every lesson is written to achieve.
