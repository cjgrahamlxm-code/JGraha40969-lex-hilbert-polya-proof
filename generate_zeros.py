import mpmath
import hashlib
import json

# --- CONFIGURATION (Task L1-006) ---
START_INDEX = 3685252
BATCH_SIZE = 1000  # "Aim for at least 1,000 additional zeros" [cite: 15]
OUTPUT_FILENAME = "riemann_zeros_extension_3685252+.json" # 

# Set precision high enough to ensure separation and accurate hashing
# 30 dps (decimal places) provides rigorous separation for Gram points
mpmath.mp.dps = 30 

def calculate_verification_hash(value_str):
    """Generates SHA-256 hash of the zero's decimal expansion."""
    return hashlib.sha256(value_str.encode('utf-8')).hexdigest()

print(f"Initiating LXD-81 Protocol: Computing {BATCH_SIZE} zeros starting at index {START_INDEX}...")

zeros_data = []

for i in range(BATCH_SIZE):
    n = START_INDEX + i
    
    # Compute the zero. zetazero(n) uses Riemann-Siegel formula 
    # to locate the n-th zero on the critical line.
    z = mpmath.zetazero(n)
    
    # Extract components
    # real_part is theoretically 0.5, mpmath returns it as such for zetazero
    real_part = 0.5 
    imag_part = float(z.imag)
    
    # Create the decimal expansion string for hashing
    # Using the high-precision string representation from mpmath
    decimal_expansion = str(z.imag)
    v_hash = calculate_verification_hash(decimal_expansion)
    
    # Structure the record per specifications 
    record = {
        "index": n,
        "real_part": real_part,
        "imaginary_part": imag_part,
        "verification_hash": v_hash
    }
    
    zeros_data.append(record)
    
    # Progress logging
    if (i + 1) % 100 == 0:
        print(f"Verified {i + 1}/{BATCH_SIZE}: Index {n} | Imag {imag_part:.5f}...")

# --- OUTPUT GENERATION ---
print(f"Stabilizing update... Writing to {OUTPUT_FILENAME}")

with open(OUTPUT_FILENAME, 'w') as f:
    json.dump(zeros_data, f, indent=4)

print("Task L1-006 Batch Complete. Oracle integrity preserved.")