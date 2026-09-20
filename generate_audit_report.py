import os
import re

def analyze_directory(base_path):
    report = {}
    for root, dirs, files in os.walk(base_path):
        if any(ignored in root for ignored in ['.venv', '.git', '__pycache__', '.pytest_cache', '.idea', 'hshs']):
            continue
        rel_root = os.path.relpath(root, base_path)
        if rel_root == '.':
            rel_root = ''
        
        md_files = [f for f in files if f.endswith('.md')]
        py_files = [f for f in files if f.endswith('.py') or f.endswith('.m')]
        
        report[rel_root] = {
            'md_count': len(md_files),
            'py_count': len(py_files),
            'files': files
        }
    return report

base_dir = '/home/settings/Documents/pearl'
data = analyze_directory(base_dir)

# Logic to map curriculum to actual folders
curriculum = {
    "Level 1: Python Data Tools": {
        "NumPy": "python-data-tools/lessons/01_numpy",
        "Pandas": "python-data-tools/lessons/02_pandas",
        "Matplotlib": "python-data-tools/lessons/03_matplotlib",
    },
    "Level 2: Engineering Math": {
        "MATLAB": "engineering-mathematics/matlab",
        "Linear Algebra": "engineering-mathematics/linear_algebra",
        "Calculus": "engineering-mathematics/calculus",
        "Probability": "engineering-mathematics/probability",
        "Simulink": "engineering-mathematics/simulink"
    },
    "Level 3: Machine Learning": {
        "ML Foundations": "machine-learning/01_ml_fundamentals",
        "Linear Regression": "machine-learning/03_regression",
        "Logistic Regression": "machine-learning/04_classification",
        "KNN": "machine-learning/04_classification",
        "Decision Trees": "machine-learning/04_classification",
        "Random Forest": "machine-learning/04_classification",
        "SVM": "machine-learning/04_classification",
        "K-Means": "machine-learning/05_clustering",
        "PCA": "machine-learning/05_clustering",
        "Perceptron": "machine-learning/07_deep_learning_intro",
        "Forward Propagation": "machine-learning/09_neural_networks",
        "Activation Functions": "machine-learning/09_neural_networks",
        "Loss Functions": "machine-learning/08_pytorch_fundamentals",
        "Gradient Descent": "machine-learning/08_pytorch_fundamentals",
        "Backpropagation": "machine-learning/09_neural_networks",
        "Model Evaluation": "machine-learning/06_model_evaluation"
    },
    "Level 3.5: Math-First ML (ml-course)": {
        "ALL": "ml-course"
    },
    "Level 4: NEAT": {
        "NEAT": "neat"
    },
    "Level 5: Deep Learning": {
        "Tensors": "machine-learning/07_deep_learning_intro",
        "PyTorch": "machine-learning/08_pytorch_fundamentals",
        "TensorFlow": "MISSING",
        "Neural Networks": "machine-learning/09_neural_networks",
        "CNNs": "machine-learning/10_cnns",
        "Transformers": "machine-learning/11_transformers"
    },
    "Level 6: Networking": {
        "TCP/IP": "MISSING",
        "HTTP/HTTPS": "MISSING",
        "REST APIs": "MISSING"
    },
    "Level 7: Game AI": {
        "Pygame": "game-ai/01_pygame",
        "Game State": "game-ai/02_game_state",
        "Tic-Tac-Toe": "game-ai/03_tic_tac_toe",
        "Minimax": "game-ai/04_minimax",
        "Alpha-Beta": "game-ai/05_alpha_beta",
        "Heuristics": "game-ai/06_heuristics",
        "Connect Four": "game-ai/07_connect_four",
        "Checkers": "game-ai/08_checkers",
        "Chess": "game-ai/09_chess",
        "MCTS": "game-ai/10_mcts",
        "Reinforcement Learning": "game-ai/11_reinforcement_learning"
    }
}

print("=== Curriculum Check ===")
for level, topics in curriculum.items():
    for topic, path in topics.items():
        if path == "MISSING":
            status = "MISSING"
        elif path in data and (data[path]['py_count'] > 0 or data[path]['md_count'] > 0):
            # Check depth for Math-first ML
            if path == 'ml-course' and data[path]['py_count'] == 0:
                status = "PLACEHOLDER"
            elif 'machine-learning' in path:
                status = "PARTIAL (Missing From-Scratch Math/NumPy Implementations)"
            elif 'game-ai/08_checkers' in path:
                 # Checkers has a README but no code
                 status = "PARTIAL"
            elif 'game-ai/10_mcts' in path or 'game-ai/11_reinforcement_learning' in path or 'game-ai/12_neural_game_ai' in path:
                 status = "MINIMAL (README only, no code)"
            else:
                status = "COMPLETE"
        else:
            status = "MISSING"
        print(f"{topic}: {status}")

