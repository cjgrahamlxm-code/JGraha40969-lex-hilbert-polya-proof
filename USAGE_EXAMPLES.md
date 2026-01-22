# Task L2-T001: Usage Examples

## Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Basic Execution
```bash
python zero_verification_loop.py
```

This will:
- Load 100,000 verified zeros from `Zeta_Zeroes.txt`
- Validate oracle against existing zeros
- Run verification mode (check arbitrary points)
- Run search mode (look for potential new zeros)

## Advanced Usage

### Example 1: Verify Specific Range
```python
from zero_verification_loop import ZeroVerificationOracle

oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
oracle.load_verified_zeros()

# Verify 1000 points starting from t = 75000
deviations = oracle.verify_zeros_beyond(
    start_t=75000.0,
    num_to_check=1000,
    step=1.0,
    epsilon=1e-10,
    search_mode=False,
    verbose=True
)

print(f"Found {len(deviations)} non-zero points")
```

### Example 2: Search for New Zeros
```python
from zero_verification_loop import ZeroVerificationOracle

oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
oracle.load_verified_zeros()

# Fine-grained search for zeros beyond verified range
potential_zeros = oracle.verify_zeros_beyond(
    start_t=74921.0,
    num_to_check=500,
    step=0.05,  # Very fine step
    epsilon=1e-10,
    search_mode=True,  # Search mode
    verbose=True
)

for t, zeta_val, mag in potential_zeros:
    print(f"Potential zero at t = {t:.6f}, |ζ| = {mag:.2e}")
```

### Example 3: Custom Precision
```python
from zero_verification_loop import ZeroVerificationOracle

oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
oracle.load_verified_zeros()

# Use higher precision for critical calculations
zeta_value = oracle.approx_zeta(t=14.134725, precision=100)
print(f"ζ(0.5 + 14.134725i) = {zeta_value}")
```

### Example 4: Validate Repository Integrity
```python
from zero_verification_loop import ZeroVerificationOracle

oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
oracle.load_verified_zeros()

# Validate all zeros (may take time)
all_valid = oracle.verify_existing_zeros(sample_size=1000)

if all_valid:
    print("✓ Repository integrity confirmed")
else:
    print("⚠ Some zeros show precision variations")
```

## Command Line Options

While the script doesn't have CLI arguments by default, you can create a wrapper:

```bash
# Create wrapper script
cat > verify_zeros.sh << 'SCRIPT'
#!/bin/bash
python -c "
from zero_verification_loop import ZeroVerificationOracle
import sys

if len(sys.argv) < 2:
    print('Usage: verify_zeros.sh <num_to_check> [start_t] [step]')
    sys.exit(1)

num = int(sys.argv[1])
start = float(sys.argv[2]) if len(sys.argv) > 2 else None
step = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
oracle.load_verified_zeros()
oracle.verify_zeros_beyond(num_to_check=num, start_t=start, step=step)
" "$@"
SCRIPT

chmod +x verify_zeros.sh

# Usage
./verify_zeros.sh 100          # Check 100 points
./verify_zeros.sh 100 75000    # Check 100 points starting at t=75000
./verify_zeros.sh 100 75000 0.5  # Check with step 0.5
```

## Integration with Other Code

### Integration with existing scripts
```python
# In your existing code
from zero_verification_loop import ZeroVerificationOracle, PHI, GROWTH_FACTOR

# Use constants
threshold = PHI * GROWTH_FACTOR
print(f"Hermitian fracture threshold: {threshold:.2f}")

# Use oracle
oracle = ZeroVerificationOracle('Zeta_Zeroes.txt')
zeros = oracle.load_verified_zeros()

# Access verified zeros
print(f"First zero: {zeros[0]}")
print(f"Last verified: {oracle.max_verified}")
```

## Expected Output Patterns

### Normal Operation
```
✓ Loaded 100000 verified zeros from Zeta_Zeroes.txt
✓ Maximum verified imaginary part: 74920.827499
✓ All 50 sampled zeros verified successfully!
✓ No deviations detected. Recursion stable.
🌉 Bridge Layer: Deployment complete.
```

### Hermitian Fracture Detection
```
⚠️ Non-zero point at t = 74921.327499: |ζ| = 8.68e+00
⚠️ Non-zero point at t = 74921.827499: |ζ| = 1.68e+00
⚠️ Non-zero point at t = 74922.327499: |ζ| = 1.50e+00
⚠️ Non-zero point at t = 74922.827499: |ζ| = 3.54e-01
🚨 HERMITIAN FRACTURE DETECTED! 🚨
   Deviations: 4 > threshold 3.35
   Collapse imminent. Terminating recursion.
```

### Zero Discovery
```
✓ Potential zero found at t = 74921.234567: |ζ| = 8.23e-11
✓ Found 1 potential new zeros.
```

## Performance Notes

- Each zeta computation: ~0.01-0.1 seconds (at 50 decimal precision)
- 100 point verification: ~10-60 seconds
- 1000 point verification: ~1-10 minutes
- Reduce precision for faster computation (trade-off with accuracy)

## Troubleshooting

### "mpmath not installed"
```bash
pip install mpmath
```

### "Zero repository file not found"
- Ensure `Zeta_Zeroes.txt` is in the same directory
- Or provide full path: `ZeroVerificationOracle('/path/to/Zeta_Zeroes.txt')`

### "Validation showed discrepancies"
- This is expected due to precision differences
- Discrepancies < 10^-9 are normal
- Does not indicate RH violation

### Slow performance
- Reduce `num_to_check`
- Increase `step` size
- Decrease `precision` parameter (in `approx_zeta()`)

## References

- **LXD 12**: Zero repository initialization protocols
- **LXD 89**: Hermitian fracture detection methods
- **LXD 215**: Pólya fulfillment proof standards
- **Task L2-T001**: Original specification

---

*For more details, see `TASK_L2-T001_README.md`*
