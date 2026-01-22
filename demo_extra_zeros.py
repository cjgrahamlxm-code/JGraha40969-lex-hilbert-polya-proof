"""
Demonstration of loading extra_zeros.txt with the enhanced oracle.

This script shows how the implementation automatically detects and loads
additional zero files when they are present.
"""

from zero_verification_loop import ZeroVerificationOracle

print("=" * 70)
print("Demonstration: Loading Multiple Zero Files")
print("=" * 70)

# Example 1: Load only the main file (when extra_zeros.txt doesn't exist)
print("\nExample 1: Loading only Zeta_Zeroes.txt")
print("-" * 70)
oracle1 = ZeroVerificationOracle('Zeta_Zeroes.txt')
zeros1 = oracle1.load_verified_zeros()

# Example 2: Try to load with extra_zeros.txt (will skip if not present)
print("\n\nExample 2: Attempting to load with extra_zeros.txt")
print("-" * 70)
oracle2 = ZeroVerificationOracle(
    zeros_filepath='Zeta_Zeroes.txt',
    extra_zeros_files=['extra_zeros.txt']
)
zeros2 = oracle2.load_verified_zeros()

# Summary
print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print(f"Oracle 1 (main file only): {len(zeros1):,} zeros")
print(f"Oracle 2 (with extra_zeros): {len(zeros2):,} zeros")

if len(zeros2) > len(zeros1):
    print(f"\n✓ Successfully loaded {len(zeros2) - len(zeros1):,} additional zeros!")
    print(f"✓ New maximum verified t: {oracle2.max_verified:.6f}")
else:
    print(f"\n⚠️  No additional zeros loaded (extra_zeros.txt not present yet)")
    print(f"   When you add extra_zeros.txt, it will automatically be loaded!")

print("\n" + "=" * 70)
