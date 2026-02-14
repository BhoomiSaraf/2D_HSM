import math
import secrets


def real_mod(x, m):
    return x - math.floor(x / m) * m


def split_key_256(key_hex):
    key_hex = key_hex.replace("0x", "")
    assert len(key_hex) == 64, "Key must be 256-bit (64 hex characters)"
    return [int(key_hex[i:i+8], 16) for i in range(0, 64, 8)]


def initialize_from_key(key_hex):

    k = split_key_256(key_hex)
    k1, k2, k3, k4, k5, k6, k7, k8 = k

    # XOR stage (Algorithm 1)
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

    # Initial conditions (paper equations)
    x10 = real_mod(((k15 * k26) + (k17 * k28)) / 2**32, 1.0)
    y10 = real_mod(((k25 * k36) + (k27 * k38)) / 2**32, 1.0)

    x20 = real_mod(((k25 * k36) + (k27 * k28)) / 2**32, 1.0)
    y20 = real_mod(((k35 * k46) + (k37 * k48)) / 2**32, 1.0)

    b11 = 4.9 + real_mod(((k35 * k46) + (k37 * k48)) / 2**32, 0.1)
    b21 = 4.9 + real_mod(((k45 * k16) + (k47 * k18)) / 2**32, 0.1)

    return x10, y10, x20, y20, b11, b21


if __name__ == "__main__":

    # Generate fresh 256-bit key
    key = secrets.token_hex(32)

    x10, y10, x20, y20, b11, b21 = initialize_from_key(key)

    print("Random 256-bit Key:")
    print(key)
    print("\nInitial Conditions & Parameters:")
    print("x10 =", x10)
    print("y10 =", y10)
    print("x20 =", x20)
    print("y20 =", y20)
    print("b11 =", b11)
    print("b21 =", b21)
