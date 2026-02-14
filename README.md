# Secure Image Encryption using Dual 2D-HSM Chaotic Maps

## Overview

This project implements a chaos-based grayscale image encryption scheme using two independent Two-Dimensional Hyperchaotic Sine Maps (2D-HSM). The system follows a 256-bit key-dependent initialization mechanism to generate secure chaotic parameters and construct two chaotic matrices (S₁ and S₂) of size 256×256.

The objective of this research is to design a secure and statistically robust image encryption framework with strong key sensitivity and resistance against differential and statistical attacks.

---

## Mathematical Model

The 2D-HSM system is defined as:

xₙ₊₁ = 0.5 × [1 − sin(1 − ωb₁xₙ² − ωb₂yₙ)]

yₙ₊₁ = sin(ωb₂xₙ)

Where:
- ω is a system constant
- b₁ and b₂ are control parameters
- (x₀, y₀) are key-dependent initial conditions

The 256-bit secret key is divided into eight 32-bit subkeys. XOR-based mixing and modular arithmetic are used to compute:

- (x₁₀, y₁₀, b₁₁)
- (x₂₀, y₂₀, b₂₁)

These parameters initialize two independent chaotic systems.

---

## Features

- 256-bit key-dependent initialization (Algorithm 1)
- Dual 2D-HSM chaotic systems
- Generation of S₁ and S₂ matrices (256×256)
- Burn-in phase for stable chaotic behavior
- 8-bit quantization of chaotic outputs
- Structured research-aligned implementation

---

## Current Implementation Status

- Key initialization completed
- Chaotic parameter generation verified
- S₁ and S₂ matrix generation implemented
- Value range validation (0–255)
  

Encryption rounds (confusion–diffusion) are under development.



