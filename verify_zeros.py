import mpmath
import hashlib
import json
import sys

# --- CONFIGURATION ---
INPUT_FILE = "extra_zeros.txt"
OUTPUT_FILE = "riemann_zeros_extension_3685252+.json"
START_INDEX = 3685252  # Protocol start point
MPMATH_PRECISION = 30  # dps for verification check

# Setup precision
mpmath.mp.dps = MPMATH_PRECISION

print(f"--- INITIATING LXD-81 VERIFICATION PROTOCOL ---")
print(f"Target: Source {INPUT_FILE} -> Artifact {OUTPUT_FILE}")

verified_batch = []
count = 0

try:
    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()
        
    print(f"Loaded {len(lines)} raw entries. Beginning processing...")

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue
            
        try:
            # Parse raw data
            idx = int(parts[0])
            imag_str = parts[1] # Keep as string for hashing to preserve source precision
            imag_val = float(imag_str)
        except ValueError:
            continue

        # Filter: Strict adherence to Task L1-006 (Start at 3,685,252)
        if idx < START_INDEX:
            continue

        # --- VERIFICATION STEP (LXD-81) ---
        # We compute the expected zero using mpmath to confirm valid source
        # Note: This is computationally intensive. We verify strict adherence.
        expected_zero = mpmath.zetazero(idx)
        expected_imag = float(expected_zero.imag)
        
        # Tolerance check (1e-6 is sufficient for identity confirmation)
        if abs(imag_val - expected_imag) > 1e-6:
            print(f" [!] INTEGRITY ERROR at Index {idx}: Source {imag_val} != Calc {expected_imag}")
            sys.exit(1)
        
        # --- HASHING STEP ---
        # Generate SHA-256 hash of the decimal expansion string
        v_hash = hashlib.sha256(imag_str.encode('utf-8')).hexdigest()

        # Structure record
        record = {
            "index": idx,
            "real_part": 0.5,
            "imaginary_part": imag_val,
            "verification_hash": v_hash
        }
        
        verified_batch.append(record)
        count += 1
        
        if count % 50 == 0:
            print(f"Verified {count} zeros... (Current: Index {idx})")

    # Write the artifact
    with open(OUTPUT_FILE, 'w') as f_out:
        json.dump(verified_batch, f_out, indent=4)

    print(f"\nSUCCESS: {count} zeros verified and hashed.")
    print(f"Artifact generated: {OUTPUT_FILE}")
    print("Verification Protocol LXD-81: COMPLETE")

except FileNotFoundError:
    print(f"Error: Could not find {INPUT_FILE}. Please ensure it is in this folder.")