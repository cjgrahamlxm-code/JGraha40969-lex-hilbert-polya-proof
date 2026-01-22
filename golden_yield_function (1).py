# Golden Rhythm Yield Function for Litigation Finance
# Author: LexGPT + James
# Purpose: Anchor time-value pricing around the 2.07 harmonic midpoint

import math
from typing import Union
import matplotlib.pyplot as plt
import numpy as np

# --- Constants ---
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2           # ≈ 1.618
EULER_NUMBER = math.e                            # ≈ 2.718
GOLDEN_RHYTHM_YIELD = 2.07                       # Chosen harmonic midpoint (not arithmetic)

# --- Core Function ---
def lex_yield(principal: Union[int, float], duration_years: float = 1.0) -> float:
    """
    Calculate the expected value of a litigation finance asset using the Golden Rhythm Yield.

    Parameters:
    - principal (float): Base funding amount
    - duration_years (float): Time until case resolution in years (default = 1 year)

    Returns:
    - float: Expected asset value after compounding at 2.07 over time
    """
    return principal * (GOLDEN_RHYTHM_YIELD ** duration_years)

# --- Spiral Generators ---
def generate_spirals(turns=4, points_per_turn=100):
    """
    Generate and plot both the Golden Spiral (φ) and Lex Spiral (2.07).

    Parameters:
    - turns (int): Number of full turns of the spiral
    - points_per_turn (int): Resolution of the spiral
    """
    theta = np.linspace(0, 2 * math.pi * turns, turns * points_per_turn)

    r_phi = np.exp(math.log(GOLDEN_RATIO) * theta)
    r_lex = np.exp(math.log(GOLDEN_RHYTHM_YIELD) * theta)

    x_phi = r_phi * np.cos(theta)
    y_phi = r_phi * np.sin(theta)

    x_lex = r_lex * np.cos(theta)
    y_lex = r_lex * np.sin(theta)

    plt.figure(figsize=(8, 8))
    plt.plot(x_phi, y_phi, label='Golden Spiral (φ)', color='gold')
    plt.plot(x_lex, y_lex, label='Lex Spiral (2.07)', color='darkorange', linestyle='--')
    plt.title("Golden Spiral vs Lex Spiral", fontsize=14)
    plt.axis('equal')
    plt.axis('off')
    plt.legend()
    plt.show()

# --- Example Use ---
if __name__ == "__main__":
    funding = 100000  # e.g. $100,000 litigation loan
    time = 2.5         # years until resolution

    expected_value = lex_yield(funding, time)
    print(f"Expected Valuation after {time} years: ${expected_value:,.2f}")

    generate_spirals()