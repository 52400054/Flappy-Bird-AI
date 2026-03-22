# 🐦 Flappy Bird AI - NeuroEvolution (NEAT)

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5+-green?style=for-the-badge&logo=python&logoColor=white)
![NEAT](https://img.shields.io/badge/NEAT--Python-AI-FF6F00?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

An advanced recreation of the Flappy Bird game featuring an AI system that learns to play using **NeuroEvolution of Augmenting Topologies (NEAT)**. Watch a population of AI birds mutate, evolve, and learn to navigate through pipes via genetic algorithms!

---

## ✨ Features

*   🧬 **Genetic Algorithm (NEAT):** Simulates natural selection. A population of 100 birds flies simultaneously. The best performers are selected to breed and mutate the next generation of neural networks.
*   🎮 **Manual Mode:** Standard player-controlled mode to test your own skills.
*   🌟 **Ultra-Smooth Interpolation:** Features a decoupled game loop (Fixed Update + Variable Rendering) utilizing **Linear Interpolation (Lerp)** to ensure butter-smooth scrolling for pipes and background regardless of game logic ticks.
*   📊 **Real-time Stats:** Displays current Generation, alive birds count, and fitness scores in real-time.

---

## 🛠️ Tech Stack & Architecture

*   **Language:** Python
*   **Engine:** `pygame-ce` (Graphics & Event loops)
*   **AI/Machine Learning:** `neat-python` (Neural Networks & Genetic Algorithms)
*   **Architecture:** Object-Oriented Programming (OOP) with clear separation between game logic, rendering, and AI population management.

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/flappy-bird-ai.git
   cd flappy-bird-ai
   ```