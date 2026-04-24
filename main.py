import numpy as np
import argparse

# Note: Data is synthetic. No real privacy guarantees are provided.

def generate_synthetic_data(num_samples=10):
    """
    Generates synthetic data based on a hardcoded example dataset.
    Uses basic statistical methods (mean and standard deviation).
    """
    # Hardcoded example dataset (e.g., ages, salaries, and years of experience)
    # Each row is an individual, columns: [Age, Salary, Years of Experience]
    real_data = np.array([
        [25, 50000, 2],
        [30, 65000, 5],
        [35, 80000, 10],
        [40, 95000, 15],
        [45, 110000, 20],
        [28, 55000, 3],
        [32, 70000, 7],
        [38, 90000, 12]
    ])
    
    print(f"Original dataset shape: {real_data.shape}")
    print("Calculating statistics...")
    
    # Calculate mean and standard deviation for each column
    means = np.mean(real_data, axis=0)
    stds = np.std(real_data, axis=0)
    
    print(f"Means: {means}")
    print(f"Standard Deviations: {stds}")
    
    print(f"Generating {num_samples} synthetic samples...")
    # Sample from normal distribution using the calculated statistics
    synthetic_data = np.zeros((num_samples, real_data.shape[1]))
    
    for i in range(real_data.shape[1]):
        synthetic_data[:, i] = np.random.normal(loc=means[i], scale=stds[i], size=num_samples)
    
    # Post-process for realistic presentation
    # Round Age and Years of Experience to integers, Salary to 2 decimal places
    synthetic_data[:, 0] = np.maximum(18, np.round(synthetic_data[:, 0])) # Ensure age >= 18
    synthetic_data[:, 1] = np.maximum(0, np.round(synthetic_data[:, 1], 2)) # Ensure salary >= 0
    synthetic_data[:, 2] = np.maximum(0, np.round(synthetic_data[:, 2])) # Ensure experience >= 0
    
    return synthetic_data

def main():
    parser = argparse.ArgumentParser(description="Simple AI-based synthetic data generator")
    parser.add_argument("--samples", type=int, default=10, help="Number of synthetic samples to generate")
    args = parser.parse_args()
    
    print("--- Synthetic Data Generation Platform ---")
    synthetic_data = generate_synthetic_data(args.samples)
    
    print("\n--- Generated Synthetic Data ---")
    print(f"{'Age':<5} | {'Salary':<10} | {'Years of Experience':<20}")
    print("-" * 42)
    for row in synthetic_data:
        print(f"{int(row[0]):<5} | {row[1]:<10.2f} | {int(row[2]):<20}")
        
    print("\nNote: Data is synthetic. Generated using basic normal distribution sampling.")

if __name__ == "__main__":
    main()
