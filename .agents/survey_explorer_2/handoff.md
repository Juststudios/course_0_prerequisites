# Comprehensive Survey Report: Level 3 & Level 4 Curriculum
**Author:** `survey_explorer_2` (Survey Explorer)  
**Date:** 2026-09-11T19:12:00Z  
**Scope:** Levels 3 & 4 (Machine Learning, Deep Learning, and associated modules) at `/home/settings/Documents/pearl`  
**Protocol:** Manual inspection protocol without automated audit scripts.

---

## 1. Observation

### 1.1 High-Level Architecture & Repository Organization
Direct manual inspection of the workspace root and documentation revealed the following structural layout:
- **`machine-learning/README.md:12-18`**:
  ```markdown
  | Level | Package | Topics |
  |-------|---------|--------|
  | **Level 1** | Python Data Tools | NumPy, Pandas, Matplotlib — the foundation of all data work |
  | **Level 2** | Engineering Mathematics | Linear Algebra, Calculus, Probability, Statistics with MATLAB |
  | **Level 3** | **Machine Learning** ← *You are here* | Supervised Learning, Unsupervised Learning, Model Evaluation |
  | **Level 4** | **Deep Learning** ← *Also here* | PyTorch, Neural Networks, CNNs, Transformers |
  ```
- **Level 3 & 4 Co-location**: Both Level 3 and Level 4 are housed within the `/home/settings/Documents/pearl/machine-learning/` directory.
- **Phantom Directory (`ml-course/`)**: A separate directory `/home/settings/Documents/pearl/ml-course/` exists, containing only a single file `ml-course/README.md` (6,378 bytes) describing a 25-module "Math-First ML Course" with modules `00_foundations/` through `25_algorithm_comparison/`. `list_dir` confirmed that no source code, subdirectories, or exercises exist in `ml-course/`.
- **Higher Levels**: `neat/README.md` and `game-ai/README.md` indicate the existence of higher curriculum tiers (Level 5: NEAT / Neuroevolution; Level 6: Game AI & Search Algorithms).

---

### 1.2 Detailed Directory & File Inventory: Level 3 & Level 4

The active curriculum in `/home/settings/Documents/pearl/machine-learning` is organized into 11 teaching modules, 1 capstone, and 6 auxiliary directories.

#### **Level 3: Classical Machine Learning (Modules 01–06)**
| Module Directory | Files Present | Stated Scope & Topics |
|---|---|---|
| `01_ml_fundamentals/` | `README.md` (7.8 KB)<br>`01_what_is_ml.py` (11.0 KB)<br>`02_ml_workflow.py` (14.2 KB)<br>`03_data_and_features.py` (12.1 KB)<br>`04_train_test_split.py` (12.7 KB)<br>`exercises.py` (7.1 KB)<br>`output/` | Traditional vs ML paradigm, 8-step ML workflow, features vs targets, categorical encoding, scaling, train/test split, overfitting, R² and MAE. |
| `02_scikit_learn/` | `README.md` (6.8 KB)<br>`01_sklearn_api.py` (9.5 KB)<br>`02_preprocessing.py` (13.3 KB)<br>`03_pipelines.py` (9.7 KB)<br>`exercises.py` (8.8 KB)<br>`output/` | Estimator API (`fit`, `predict`, `transform`, `score`), scalers (`StandardScaler`, `MinMaxScaler`, `RobustScaler`), `OneHotEncoder`, `SimpleImputer`, `ColumnTransformer`, `Pipeline`, data leakage prevention, `GridSearchCV`. |
| `03_regression/` | `README.md` (6.4 KB)<br>`01_linear_regression.py` (8.4 KB)<br>`02_polynomial_regression.py` (7.6 KB)<br>`03_regularization.py` (9.5 KB)<br>`exercises.py` (7.0 KB)<br>`output/`<br>`solutions/` (EMPTY) | Simple and multiple linear regression, MSE cost, Normal Equation derivation, Polynomial regression, Ridge (L2), Lasso (L1 feature selection), ElasticNet, `RidgeCV`, `LassoCV`. |
| `04_classification/` | `README.md` (7.1 KB)<br>`01_logistic_regression.py` (12.6 KB)<br>`02_decision_trees.py` (11.4 KB)<br>`03_random_forests.py` (12.8 KB)<br>`04_svm.py` (13.5 KB)<br>`05_knn.py` (11.9 KB)<br>`exercises.py` (7.6 KB) | Logistic regression, Sigmoid function, Decision trees, Gini impurity, Random forests, bagging, out-of-bag (OOB) score, Support Vector Machines (margins, RBF kernel, C parameter), K-Nearest Neighbors, distance metrics. |
| `05_clustering/` | `README.md` (6.9 KB)<br>`01_kmeans.py` (9.6 KB)<br>`02_hierarchical_clustering.py` (8.8 KB)<br>`03_dbscan.py` (9.0 KB)<br>`04_dimensionality_reduction.py` (9.9 KB)<br>`exercises.py` (8.0 KB)<br>`output/` | Unsupervised learning, K-Means clustering, Elbow method, Silhouette score, Hierarchical agglomerative clustering, dendrograms, linkage criteria (Ward, complete, average), DBSCAN (density, core points, noise detection), PCA (variance preservation, scree plots). |
| `06_model_evaluation/` | `README.md` (6.0 KB)<br>`01_metrics.py` (14.1 KB)<br>`02_cross_validation.py` (14.2 KB)<br>`03_hyperparameter_tuning.py` (14.5 KB)<br>`04_bias_variance_tradeoff.py` (9.5 KB)<br>`05_imbalanced_data.py` (11.6 KB)<br>`exercises.py` (8.1 KB)<br>`output/` | Accuracy trap, Precision, Recall, F1, ROC-AUC, PR-AUC, K-Fold, Stratified K-Fold, TimeSeriesSplit, Leave-One-Out, GridSearchCV, RandomizedSearchCV, Bias-Variance decomposition, learning curves, severe class imbalance, class weights. |

#### **Level 4: Deep Learning (Modules 07–11)**
| Module Directory | Files Present | Stated Scope & Topics |
|---|---|---|
| `07_deep_learning_intro/` | `README.md` (6.5 KB)<br>`01_tensors.py` (10.0 KB)<br>`02_autograd.py` (9.4 KB)<br>`03_linear_model_in_pytorch.py` (9.2 KB)<br>`04_datasets_and_dataloaders.py` (10.7 KB)<br>`exercises.py` (7.1 KB)<br>`output/` | PyTorch CPU tensors (creation, operations, indexing, numpy bridge), dynamic computational graphs, automatic differentiation (`backward()`, chain rule), `nn.Module`, `nn.Linear`, 5-step canonical training loop, `Dataset`, `DataLoader`, mini-batching. |
| `08_pytorch_fundamentals/` | `README.md` (6.3 KB)<br>`01_nn_module.py` (14.1 KB)<br>`02_loss_functions.py` (14.0 KB)<br>`03_optimizers.py` (13.5 KB)<br>`04_training_loop.py` (11.4 KB)<br>`05_mlp_classification.py` (10.2 KB)<br>`exercises.py` (8.0 KB)<br>`output/` | Custom `nn.Module` subclassing, parameter registration, regression vs classification loss (`MSELoss`, `L1Loss`, `BCEWithLogitsLoss`, `CrossEntropyLoss`), optimizers (SGD, Momentum, Adam), learning rate scheduling, validation loops, early stopping, checkpointing, end-to-end MLP classifier project. |
| `09_neural_networks/` | `README.md` (5.0 KB)<br>`01_activation_functions.py` (8.4 KB)<br>`02_backpropagation_and_deep_mlp.py` (9.3 KB)<br>`exercises.py` (8.7 KB)<br>`output/` | **CRITICAL DISCREPANCY:** Only 2 lesson files exist. Covers non-linear activations (ReLU, Sigmoid, Tanh, GELU), vanishing gradients, step-by-step backprop derivation with manual chain rule vs PyTorch autograd, deep MLP design patterns. |
| `10_cnns/` | `README.md` (9.4 KB)<br>`01_convolution.py` (13.9 KB)<br>`02_pooling_and_architecture.py` (19.4 KB)<br>`03_cnn_for_images.py` (11.1 KB)<br>`04_transfer_learning.py` (13.7 KB)<br>`exercises.py` (9.3 KB)<br>`output/` | Parameter sharing, 2D convolution filters, Sobel kernels, manual numpy convolution, stride, padding, MaxPooling, AveragePooling, AdaptiveAvgPool2d, `BatchNorm2d`, Conv-BN-ReLU-Pool architecture block, image classification, transfer learning (frozen backbone vs fine-tuning). |
| `11_transformers/` | `README.md` (3.5 KB)<br>`01_attention_and_transformers.py` (15.0 KB)<br>`exercises.py` (10.6 KB)<br>`output/` | **THIN COVERAGE:** Only 1 lesson script. Covers self-attention intuition, Q/K/V linear projections, Scaled Dot-Product Attention formula, Multi-Head Attention, causal masking, Transformer encoder layer (`nn.TransformerEncoderLayer`), sequence classification. |

#### **Combined & Auxiliary Modules**
| Directory | Files Present | Scope & Status |
|---|---|---|
| `12_capstone/` | `README.md` (6.5 KB)<br>`generate_capstone_data.py` (9.6 KB)<br>`starter_template.py` (10.9 KB) | Predictive Failure Detection System (8 sensors, regression for RUL, 3-class fault severity classification). Dataset generator produces train/test CSVs. Starter template provided. **Missing:** `capstone_solution.py`. |
| `assessment/` | `FINAL_ASSESSMENT.md` (9.0 KB)<br>`practical_test.py` (6.9 KB) | 100-point comprehensive exam across 3 sections (Conceptual, Implementation, Capstone). Automated test runner verifies 23 lesson scripts and file presence for 43 core files. |
| `datasets/` | `industrial_sensor_train.csv` (54.1 KB)<br>`industrial_sensor_test.csv` (10.9 KB) | Generated dataset with 1,000 training and 200 test samples. |
| `reference/` | `ml_cheat_sheet.md` (9.1 KB)<br>`pytorch_cheat_sheet.md` (10.3 KB) | Quick reference cheat sheets. **Missing:** `ml_mathematics.md` and `algorithm_guide.md` (promised in master README). |
| `solutions/` | `ml_fundamentals_solutions.py` (6.2 KB)<br>`sklearn_regression_clustering_solutions.py` (11.0 KB)<br>`pytorch_neural_net_solutions.py` (10.5 KB)<br>`output/` | **BROKEN DECOUPLING:** Only 3 consolidated solution files exist. All exercise files reference nonexistent decoupled files (`classification_solutions.py`, `cnn_solutions.py`, etc.). Multiple modules lack solutions completely. |
| `exercises/` | EMPTY directory | Redundant/orphaned folder. Exercises are located within each individual module folder. |
| `projects/` | EMPTY directory | Redundant/orphaned folder. No separate project directories exist. |

---

### 1.3 Mathematical Derivations & From-Scratch vs Library Verification

Manual reading of code and markdown files revealed the following evidence of mathematical substance:

1. **Closed-Form Normal Equation (`03_regression/01_linear_regression.py:173-207`)**:
   - Explicitly derives and compares the analytical ordinary least squares (OLS) solution against scikit-learn:
     ```python
     w_normal = np.linalg.pinv(X_demo.T @ X_demo) @ X_demo.T @ y_demo
     ```
2. **From-Scratch Gradient Descent (`solutions/sklearn_regression_clustering_solutions.py:89-136`)**:
   - `LinearRegressionGD` implements mini-batch gradient descent in NumPy:
     ```python
     dw = (2 / n_b) * Xb.T @ (y_pred - yb)
     db = (2 / n_b) * (y_pred - yb).sum()
     self.w -= self.lr * dw
     self.b -= self.lr * db
     ```
3. **Manual 2D Convolution (`10_cnns/01_convolution.py:76-120`)**:
   - Implements `convolve2d_manual(image, kernel, stride, padding)` using explicit nested loops, image padding, output size calculation, and sub-patch dot products (`np.sum(patch * kernel)`).
4. **Manual Backpropagation Chain Rule (`09_neural_networks/02_backpropagation_and_deep_mlp.py:65-100`)**:
   - Traces forward pass: $z = xW + b$, $y = \text{ReLU}(z)$, $L = (y - y_{\text{true}})^2$.
   - Computes analytical gradients manually:
     ```python
     dL_dy = 2 * (y_pred - y_true)
     dy_dz = (z > 0).float()
     dL_dW_manual = (dL_dy * dy_dz).T @ x
     dL_db_manual = (dL_dy * dy_dz).sum()
     ```
   - Confirms numerical equivalence with `torch.allclose(W.grad, dL_dW_manual)`.
5. **From-Scratch Two-Layer Neural Network (`solutions/pytorch_neural_net_solutions.py:123-193`)**:
   - Implements `TwoLayerNetSolution` with manual Xavier weight initialization, manual forward pass, numerically stable manual cross-entropy (`cross_entropy_manual`), autograd backward, and manual SGD tensor parameter updates.
6. **From-Scratch Scaled Dot-Product Attention (`11_transformers/01_attention_and_transformers.py:80-111` & `solutions/pytorch_neural_net_solutions.py:200-243`)**:
   - Step-by-step computation: $Q = X W_Q$, $K = X W_K$, $V = X W_V$, scores $= \frac{Q K^T}{\sqrt{d_k}}$, `attn_weights = torch.softmax(scores, dim=-1)`, `output = attn_weights @ V`.
7. **From-Scratch K-Means Clustering (`solutions/sklearn_regression_clustering_solutions.py:161-232`)**:
   - `KMeansScratch` implements random centroid initialization, vectorized Euclidean distance matrix calculation:
     $$\|x - c\|^2 = \|x\|^2 - 2 x c^T + \|c\|^2$$
     cluster assignment, centroid updating by cluster means, and convergence tolerance checking.
8. **Mathematical Gaps Identified**:
   - **PCA (`05_clustering/04_dimensionality_reduction.py`)**: Purely uses `sklearn.decomposition.PCA`. Does NOT implement or derive the sample covariance matrix $\frac{1}{n-1} X^T X$ or eigenvalue decomposition (`np.linalg.eigh`) from scratch.
   - **Logistic Regression (`04_classification/01_logistic_regression.py`)**: Demonstrates $\sigma(z) = \frac{1}{1 + e^{-z}}$, but relies entirely on `sklearn.linear_model.LogisticRegression`. Does NOT implement gradient descent on binary cross-entropy loss from scratch in the lesson.
   - **KNN (`04_classification/05_knn.py`)**: Explains distance metrics, but the from-scratch `KNNClassifier` is only given as an incomplete exercise template; no completed solution exists anywhere in the repository.

---

### 1.4 Broken References and Missing Files Observed

1. **Missing Files in `reference/`**:
   - `machine-learning/README.md:135-138` lists:
     ```
     ├── reference/
     │   ├── ml_cheat_sheet.md
     │   ├── pytorch_cheat_sheet.md
     │   ├── ml_mathematics.md      <-- MISSING
     │   └── algorithm_guide.md     <-- MISSING
     ```
   - Only `ml_cheat_sheet.md` and `pytorch_cheat_sheet.md` exist.
2. **Missing Module 09 Lessons**:
   - `09_neural_networks/README.md:117-126` promises 5 lessons:
     - `01_activation_functions.py` (Present)
     - `02_weight_initialization.py` (**MISSING**)
     - `03_batch_normalization.py` (**MISSING**)
     - `04_dropout.py` (**MISSING**)
     - `05_deep_mlp_project.py` (**MISSING**)
     - `exercises_solutions.py` (**MISSING**)
   - Only `01_activation_functions.py` and `02_backpropagation_and_deep_mlp.py` exist in the directory.
3. **Broken Solution Decoupling**:
   - `machine-learning/README.md:123-132` states that `solutions/` contains 9 distinct solution files:
     `ml_fundamentals_solutions.py`, `sklearn_solutions.py`, `regression_solutions.py`, `classification_solutions.py`, `clustering_solutions.py`, `model_evaluation_solutions.py`, `pytorch_solutions.py`, `advanced_dl_solutions.py`, `capstone_solution.py`.
   - In reality, only **3** consolidated files exist:
     - `ml_fundamentals_solutions.py`
     - `sklearn_regression_clustering_solutions.py`
     - `pytorch_neural_net_solutions.py`
   - Every module's `exercises.py` points students to a missing file (e.g., `03_regression/exercises.py:190` points to `solutions/regression_solutions.py`; `04_classification/exercises.py:211` points to `solutions/classification_solutions.py`; `10_cnns/exercises.py:260` points to `solutions/cnn_solutions.py`; `11_transformers/exercises.py:288` points to `solutions/transformer_solutions.py`).
   - Module 04 (Classification), Module 10 (CNNs), and Module 12 (Capstone) have **ZERO** reference solutions anywhere in the repository.
4. **Empty Directories**:
   - `/home/settings/Documents/pearl/machine-learning/exercises/` is empty.
   - `/home/settings/Documents/pearl/machine-learning/projects/` is empty.
   - `/home/settings/Documents/pearl/machine-learning/03_regression/solutions/` is empty.
   - `/home/settings/Documents/pearl/ml-course/` contains 0 code files.

---

## 2. Logic Chain

1. **Observation 1.1** showed that Level 3 (Classical ML, Modules 1–6) and Level 4 (Deep Learning, Modules 7–11) are co-located in `machine-learning/`. Furthermore, `ml-course/` is an abandoned alternate blueprint with no code.  
   $\rightarrow$ *Inference 1:* All analysis and future remediation for Levels 3 and 4 must target `/home/settings/Documents/pearl/machine-learning/`. The `ml-course/` directory is dead weight that should either be archived or cleaned up.

2. **Observation 1.2 & 1.4** showed that while all 11 modules and the capstone have functioning `README.md` and `exercises.py` files, Module 09 has a major discrepancy between its specification (which promised 5 detailed lessons on weight init, batch norm, dropout, and a deep MLP project) and its actual state (only 2 lesson files), and Module 11 has only 1 lesson file.  
   $\rightarrow$ *Inference 2:* Level 4 content completeness drops significantly in Modules 09 and 11. Core deep learning engineering topics (Weight Initialization theory/experiments, Batch Normalization dynamics, and Dropout regularisation) lack dedicated lesson files and must be expanded to meet stated learning objectives.

3. **Observation 1.3** showed that mathematical substance is exceptionally high in certain modules (e.g., OLS Normal Equation in Mod 3, manual 2D convolution in Mod 10, manual backprop derivative matching in Mod 9, manual self-attention in Mod 11), but has notable gaps where scikit-learn is used purely as a black box (PCA in Mod 5 without covariance eigen-decomposition, and Logistic Regression in Mod 4 without from-scratch binary cross-entropy gradient descent).  
   $\rightarrow$ *Inference 3:* To satisfy the curriculum requirement of "understanding the mathematics and from-scratch implementations rather than just black-box library calls," modules 4 (Logistic Regression) and 5 (PCA) require mathematical augmentation with NumPy from-scratch implementations.

4. **Observation 1.4** proved that the exercise solution architecture is fractured. The exercises instruct students to inspect specific solution files, but the repository author consolidated some solutions into 3 ad-hoc files and omitted solutions for Classification (Mod 4), CNNs (Mod 10), and the Capstone project (Mod 12).  
   $\rightarrow$ *Inference 4:* The curriculum fails acceptance criteria regarding complete, decoupled reference solutions for every exercise. A student completing exercises in Modules 4, 10, or 12 has no reference solution to consult.

5. **Observation 1.4** proved that `reference/ml_mathematics.md` and `reference/algorithm_guide.md` are missing from disk, and `machine-learning/exercises/` and `machine-learning/projects/` are empty.  
   $\rightarrow$ *Inference 5:* The reference section and project packaging are incomplete relative to the claims made in `machine-learning/README.md`.

---

## 3. Caveats

- **No Execution of Non-Lesson Scripts**: In adherence to the benchmark integrity mode and read-only constraints, we did not execute scripts or generate training artifacts during this survey turn; findings are based strictly on textual and structural code inspection.
- **Scope Boundary**: This survey focused strictly on Level 3 and Level 4 (`machine-learning/`). Other curriculum levels (`python-data-tools` for Level 1, `engineering-mathematics` for Level 2, `neat` for Level 5, `game-ai` for Level 6) were examined only at their root README level to verify curriculum boundaries.
- **Assessment Validation**: `assessment/practical_test.py` was inspected statically; its internal list of 23 test targets reflects what the previous authors considered passing, but `practical_test.py` itself ignores the missing solutions and missing Module 09 files.

---

## 4. Conclusion

The Level 3 and Level 4 curriculum at `/home/settings/Documents/pearl/machine-learning` provides a comprehensive, pedagogically sound, and well-commented instructional suite. It features strong engineering motivations, clear visualizations, and 4-tier progressive exercises across all 11 modules.

However, the repository exhibits **four major deficiency clusters** that prevent it from being considered fully complete:

1. **Module 09 Content Deficit**: `09_neural_networks/README.md` promises 5 granular lessons (`01_activation_functions.py`, `02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`), but only 2 exist (`01_activation_functions.py`, `02_backpropagation_and_deep_mlp.py`).
2. **Broken Solution Architecture & Missing Solutions**:
   - Exercise files cross-reference 9 individual module solution files that do not exist.
   - Only 3 partial solution scripts exist in `solutions/`.
   - **Module 04 (Classification)**, **Module 10 (CNNs)**, and **Module 12 (Capstone)** have **no solutions whatsoever**.
   - Levels 1, 2, and 3 exercises across most modules lack solutions in the consolidated files.
3. **Missing Reference Documentation**:
   - `reference/ml_mathematics.md` is missing.
   - `reference/algorithm_guide.md` is missing.
4. **Mathematical From-Scratch Gaps**:
   - PCA (`05_clustering/04_dimensionality_reduction.py`) relies exclusively on `sklearn.decomposition.PCA` without demonstrating covariance matrix construction and eigenvector decomposition in NumPy.
   - Logistic Regression (`04_classification/01_logistic_regression.py`) lacks a from-scratch gradient descent implementation for binary cross-entropy loss.
   - The Capstone (`12_capstone/`) is missing `capstone_solution.py`.

---

## 5. Verification Method

To independently verify all findings in this report:

1. **Verify Directory Structure & Missing Files**:
   ```bash
   # Confirm missing reference files
   ls /home/settings/Documents/pearl/machine-learning/reference/
   # Expected: only ml_cheat_sheet.md and pytorch_cheat_sheet.md exist.

   # Confirm Module 09 file count discrepancy
   ls /home/settings/Documents/pearl/machine-learning/09_neural_networks/
   # Expected: only 01_activation_functions.py and 02_backpropagation_and_deep_mlp.py exist.

   # Confirm missing solution files
   ls /home/settings/Documents/pearl/machine-learning/solutions/
   # Expected: only ml_fundamentals_solutions.py, pytorch_neural_net_solutions.py, and sklearn_regression_clustering_solutions.py exist.
   ```

2. **Verify Solution Cross-References**:
   - Inspect `/home/settings/Documents/pearl/machine-learning/04_classification/exercises.py:211` to observe reference to nonexistent `solutions/classification_solutions.py`.
   - Inspect `/home/settings/Documents/pearl/machine-learning/10_cnns/exercises.py:260` to observe reference to nonexistent `solutions/cnn_solutions.py`.
   - Inspect `/home/settings/Documents/pearl/machine-learning/11_transformers/exercises.py:288` to observe reference to nonexistent `solutions/transformer_solutions.py`.

3. **Verify Empty Directories**:
   - Check `ls -A /home/settings/Documents/pearl/machine-learning/exercises` (returns empty).
   - Check `ls -A /home/settings/Documents/pearl/machine-learning/projects` (returns empty).
   - Check `ls -A /home/settings/Documents/pearl/machine-learning/03_regression/solutions` (returns empty).
   - Check `ls -A /home/settings/Documents/pearl/ml-course` (returns only `README.md`).

---

## 6. Mandatory Reading Record

Every file listed below was opened, read, and evaluated manually using `view_file` without automated scanning scripts:

1. `/home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md` (Project brief & non-negotiable audit protocol)
2. `/home/settings/Documents/pearl/.agents/PROJECT.md` (Level 2 specification and curriculum architecture map)
3. `/home/settings/Documents/pearl/README.md` (Repository root README and curriculum navigation)
4. `/home/settings/Documents/pearl/ml-course/README.md` (Alternative/abandoned 25-module ML curriculum map)
5. `/home/settings/Documents/pearl/machine-learning/README.md` (Master Level 3 & Level 4 curriculum syllabus and module map)
6. `/home/settings/Documents/pearl/game-ai/README.md` (Level 6 curriculum context)
7. `/home/settings/Documents/pearl/neat/README.md` (Level 5 curriculum context)
8. `/home/settings/Documents/pearl/hshs/README.md` (Flutter demo project inspection)
9. `/home/settings/Documents/pearl/lesson3.py` (Root script verification — 0 bytes)
10. `/home/settings/Documents/pearl/machine-learning/requirements.txt` (Level 3/4 dependencies and version constraints)
11. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/README.md` (Module 1 overview, learning objectives, concept map)
12. `/home/settings/Documents/pearl/machine-learning/02_scikit_learn/README.md` (Module 2 overview, Estimator API, Pipeline architecture)
13. `/home/settings/Documents/pearl/machine-learning/03_regression/README.md` (Module 3 overview, OLS mathematics, regularisation)
14. `/home/settings/Documents/pearl/machine-learning/04_classification/README.md` (Module 4 overview, classifiers, decision boundaries)
15. `/home/settings/Documents/pearl/machine-learning/05_clustering/README.md` (Module 5 overview, unsupervised clustering, metrics)
16. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/README.md` (Module 6 overview, metrics, cross-validation, imbalance)
17. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/README.md` (Module 7 overview, tensors, autograd, PyTorch ecosystem)
18. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/README.md` (Module 8 overview, nn.Module, 5-step recipe)
19. `/home/settings/Documents/pearl/machine-learning/09_neural_networks/README.md` (Module 9 overview, 4 pillars of deep networks)
20. `/home/settings/Documents/pearl/machine-learning/10_cnns/README.md` (Module 10 overview, convolution, pooling, feature hierarchy)
21. `/home/settings/Documents/pearl/machine-learning/11_transformers/README.md` (Module 11 overview, attention mechanism, encoder block)
22. `/home/settings/Documents/pearl/machine-learning/12_capstone/README.md` (Module 12 capstone specification, 200-point rubric)
23. `/home/settings/Documents/pearl/machine-learning/assessment/FINAL_ASSESSMENT.md` (100-point comprehensive exam across 3 sections)
24. `/home/settings/Documents/pearl/machine-learning/assessment/practical_test.py` (Test validation runner inspecting 23 lessons)
25. `/home/settings/Documents/pearl/machine-learning/reference/ml_cheat_sheet.md` (Classical ML reference sheet)
26. `/home/settings/Documents/pearl/machine-learning/reference/pytorch_cheat_sheet.md` (PyTorch operations reference sheet)
27. `/home/settings/Documents/pearl/machine-learning/solutions/ml_fundamentals_solutions.py` (Module 1 reference solutions)
28. `/home/settings/Documents/pearl/machine-learning/solutions/sklearn_regression_clustering_solutions.py` (Consolidated solutions for Mod 2, 3, 5, 6)
29. `/home/settings/Documents/pearl/machine-learning/solutions/pytorch_neural_net_solutions.py` (Consolidated solutions for Mod 7, 8, 9, 11)
30. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/exercises.py` (Module 1 4-tier exercises)
31. `/home/settings/Documents/pearl/machine-learning/02_scikit_learn/exercises.py` (Module 2 4-tier exercises)
32. `/home/settings/Documents/pearl/machine-learning/03_regression/exercises.py` (Module 3 4-tier exercises)
33. `/home/settings/Documents/pearl/machine-learning/04_classification/exercises.py` (Module 4 4-tier exercises)
34. `/home/settings/Documents/pearl/machine-learning/05_clustering/exercises.py` (Module 5 4-tier exercises)
35. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/exercises.py` (Module 6 4-tier exercises)
36. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/exercises.py` (Module 7 4-tier exercises)
37. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/exercises.py` (Module 8 4-tier exercises)
38. `/home/settings/Documents/pearl/machine-learning/09_neural_networks/exercises.py` (Module 9 4-tier exercises)
39. `/home/settings/Documents/pearl/machine-learning/10_cnns/exercises.py` (Module 10 4-tier exercises)
40. `/home/settings/Documents/pearl/machine-learning/11_transformers/exercises.py` (Module 11 4-tier exercises)
41. `/home/settings/Documents/pearl/machine-learning/12_capstone/generate_capstone_data.py` (Synthetic dataset generator)
42. `/home/settings/Documents/pearl/machine-learning/12_capstone/starter_template.py` (Capstone starter template)
43. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/01_what_is_ml.py` (Lesson on rules vs ML)
44. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/02_ml_workflow.py` (Lesson on 8-step ML workflow)
45. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/03_data_and_features.py` (Lesson on data representation & encoding)
46. `/home/settings/Documents/pearl/machine-learning/01_ml_fundamentals/04_train_test_split.py` (Lesson on evaluation & overfitting)
47. `/home/settings/Documents/pearl/machine-learning/02_scikit_learn/01_sklearn_api.py` (Lesson on Estimator interface)
48. `/home/settings/Documents/pearl/machine-learning/02_scikit_learn/02_preprocessing.py` (Lesson on scalers, imputers, ColumnTransformer)
49. `/home/settings/Documents/pearl/machine-learning/02_scikit_learn/03_pipelines.py` (Lesson on Pipelines & GridSearchCV)
50. `/home/settings/Documents/pearl/machine-learning/03_regression/01_linear_regression.py` (Lesson on simple/multiple linear regression & Normal Equation)
51. `/home/settings/Documents/pearl/machine-learning/03_regression/02_polynomial_regression.py` (Lesson on nonlinear polynomial modeling)
52. `/home/settings/Documents/pearl/machine-learning/03_regression/03_regularization.py` (Lesson on Ridge, Lasso, ElasticNet)
53. `/home/settings/Documents/pearl/machine-learning/04_classification/01_logistic_regression.py` (Lesson on sigmoid & binary classification)
54. `/home/settings/Documents/pearl/machine-learning/04_classification/02_decision_trees.py` (Lesson on Gini impurity & tree structure)
55. `/home/settings/Documents/pearl/machine-learning/04_classification/03_random_forests.py` (Lesson on bagging & ensembles)
56. `/home/settings/Documents/pearl/machine-learning/04_classification/04_svm.py` (Lesson on margins & kernel trick)
57. `/home/settings/Documents/pearl/machine-learning/04_classification/05_knn.py` (Lesson on instance-based learning & distance)
58. `/home/settings/Documents/pearl/machine-learning/05_clustering/01_kmeans.py` (Lesson on K-Means & silhouette score)
59. `/home/settings/Documents/pearl/machine-learning/05_clustering/02_hierarchical_clustering.py` (Lesson on agglomerative clustering & dendrograms)
60. `/home/settings/Documents/pearl/machine-learning/05_clustering/03_dbscan.py` (Lesson on density clustering & noise handling)
61. `/home/settings/Documents/pearl/machine-learning/05_clustering/04_dimensionality_reduction.py` (Lesson on PCA & variance preservation)
62. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/01_metrics.py` (Lesson on precision, recall, F1, ROC/PR curves)
63. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/02_cross_validation.py` (Lesson on K-Fold & Stratified CV)
64. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/03_hyperparameter_tuning.py` (Lesson on GridSearchCV & validation curves)
65. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/04_bias_variance_tradeoff.py` (Lesson on bias-variance decomposition)
66. `/home/settings/Documents/pearl/machine-learning/06_model_evaluation/05_imbalanced_data.py` (Lesson on severe class imbalance techniques)
67. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/01_tensors.py` (Lesson on PyTorch tensors & operations)
68. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/02_autograd.py` (Lesson on computational graphs & autodiff)
69. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/03_linear_model_in_pytorch.py` (Lesson on nn.Linear & 5-step loop)
70. `/home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/04_datasets_and_dataloaders.py` (Lesson on Dataset & DataLoader)
71. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/01_nn_module.py` (Lesson on custom nn.Module building)
72. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/02_loss_functions.py` (Lesson on regression & classification losses)
73. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/03_optimizers.py` (Lesson on SGD, Momentum, Adam)
74. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/04_training_loop.py` (Lesson on complete training loop with validation)
75. `/home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/05_mlp_classification.py` (Lesson on full MLP classification pipeline)
76. `/home/settings/Documents/pearl/machine-learning/09_neural_networks/01_activation_functions.py` (Lesson on non-linearities & gradients)
77. `/home/settings/Documents/pearl/machine-learning/09_neural_networks/02_backpropagation_and_deep_mlp.py` (Lesson on manual backprop vs autograd)
78. `/home/settings/Documents/pearl/machine-learning/10_cnns/01_convolution.py` (Lesson on manual numpy convolution & Sobel filters)
79. `/home/settings/Documents/pearl/machine-learning/10_cnns/02_pooling_and_architecture.py` (Lesson on pooling & CNN building blocks)
80. `/home/settings/Documents/pearl/machine-learning/10_cnns/03_cnn_for_images.py` (Lesson on end-to-end CNN image classification)
81. `/home/settings/Documents/pearl/machine-learning/10_cnns/04_transfer_learning.py` (Lesson on simulated pretrained CNN fine-tuning)
82. `/home/settings/Documents/pearl/machine-learning/11_transformers/01_attention_and_transformers.py` (Lesson on manual self-attention & transformer blocks)
