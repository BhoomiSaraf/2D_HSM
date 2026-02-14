import numpy as np
import math
import secrets
import matplotlib.pyplot as plt

# =====================================================
# 2D-HSM CONSTANTS (as used in the paper)
# =====================================================
OMEGA = 10.0
B2 = 1.57


# =====================================================
# Real mod function (paper definition)
# =====================================================
def real_mod(x, m):
    return x - math.floor(x / m) * m


# =====================================================
# Split 256-bit key into 8 × 32-bit blocks
# =====================================================
def split_key_256(key_hex):
    key_hex = key_hex.replace("0x", "")
    assert len(key_hex) == 64, "Key must be 256-bit (64 hex characters)"
    return [int(key_hex[i:i+8], 16) for i in range(0, 64, 8)]


# =====================================================
# Algorithm 1 – Key Initialization (Paper-Faithful)
# =====================================================
def initialize_from_key(key_hex):

    k = split_key_256(key_hex)
    k1, k2, k3, k4, k5, k6, k7, k8 = k

    # XOR stage (kst = ks ⊕ kt)
    k15 = k1 ^ k5
    k16 = k1 ^ k6
    k17 = k1 ^ k7
    k18 = k1 ^ k8

    k25 = k2 ^ k5
    k26 = k2 ^ k6
    k27 = k2 ^ k7
    k28 = k2 ^ k8

    k35 = k3 ^ k5
    k36 = k3 ^ k6
    k37 = k3 ^ k7
    k38 = k3 ^ k8

    k45 = k4 ^ k5
    k46 = k4 ^ k6
    k47 = k4 ^ k7
    k48 = k4 ^ k8

    # Initial conditions
    x10 = real_mod(((k15 * k26) + (k17 * k28)) / 2**32, 1.0)
    y10 = real_mod(((k25 * k36) + (k27 * k38)) / 2**32, 1.0)

    x20 = real_mod(((k25 * k36) + (k27 * k28)) / 2**32, 1.0)
    y20 = real_mod(((k35 * k46) + (k37 * k48)) / 2**32, 1.0)

    b11 = 4.9 + real_mod(((k35 * k46) + (k37 * k48)) / 2**32, 0.1)
    b21 = 4.9 + real_mod(((k45 * k16) + (k47 * k18)) / 2**32, 0.1)

    return x10, y10, x20, y20, b11, b21


# =====================================================
# 2D-HSM Iteration
# =====================================================
def iterate_2dhsm(x, y, b1):
    x_next = 0.5 * (1 - math.sin(1 - OMEGA * b1 * x * x - OMEGA * B2 * y))
    y_next = math.sin(OMEGA * B2 * x)
    return x_next % 1.0, y_next % 1.0


# =====================================================
# Generate Chaotic Matrix (256×256)
# =====================================================
def generate_S_matrix(x0, y0, b1, size=256, burn_in=1000):

    x, y = x0, y0
    total = size * size
    sequence = []

    for i in range(total + burn_in):
        x, y = iterate_2dhsm(x, y, b1)

        if i >= burn_in:
            value = int(x * 256) % 256
            sequence.append(value)

    S = np.array(sequence, dtype=np.uint8).reshape(size, size)
    return S


# =====================================================
# MAIN EXECUTION
# =====================================================
if __name__ == "__main__":

    # Generate random 256-bit key
    key = secrets.token_hex(32)

    # Initialize chaotic systems
    x10, y10, x20, y20, b11, b21 = initialize_from_key(key)

    # Print parameters
    print("\n=== 256-bit Key ===")
    print(key)

    print("\n=== Initial Conditions ===")
    print("x10 =", x10)
    print("y10 =", y10)
    print("x20 =", x20)
    print("y20 =", y20)

    print("\n=== Parameters ===")
    print("b11 =", b11)
    print("b21 =", b21)

    # Generate S1 and S2 (256×256)
    S1 = generate_S_matrix(x10, y10, b11, size=256)
    S2 = generate_S_matrix(x20, y20, b21, size=256)

    print("\n=== Matrix Shapes ===")
    print("S1 shape:", S1.shape)
    print("S2 shape:", S2.shape)

    print("\n=== Value Range Check ===")
    print("S1 min/max:", S1.min(), S1.max())
    print("S2 min/max:", S2.min(), S2.max())

    print("\n=== First 4 elements of S1 ===")
print("S1[0,0] =", S1[0,0])
print("S1[0,1] =", S1[0,1])
print("S1[1,0] =", S1[1,0])
print("S1[1,1] =", S1[1,1])

print("\n=== First 4 elements of S2 ===")
print("S2[0,0] =", S2[0,0])
print("S2[0,1] =", S2[0,1])
print("S2[1,0] =", S2[1,0])
print("S2[1,1] =", S2[1,1])

print("\nS1 first 2x2 block:")
print(S1[:2, :2])

print("\nS2 first 2x2 block:")
print(S2[:2, :2])


   
