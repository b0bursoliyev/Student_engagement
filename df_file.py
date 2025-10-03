import pandas as pd
import os
from pathlib import Path

def process_csv_file(file_path, output_dir):
    """Process a single CSV file and save the results."""
    try:
        # Get relative path for output naming
        rel_path = os.path.relpath(file_path, 'Engagement')
        output_filename = os.path.splitext(rel_path)[0].replace(os.sep, '_') + '_means.csv'
        output_path = os.path.join(output_dir, output_filename)
        
        # Skip if output already exists
        if os.path.exists(output_path):
            print(f"Skipping {file_path} - output already exists")
            return
            
        print(f"\nProcessing: {file_path}")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            # Skip the first 9 rows of metadata
            for _ in range(9):
                next(f)
            # Read the rest of the file
            data = []
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[1]:
                    try:
                        rating = float(parts[1])
                        data.append(rating)
                    except ValueError:
                        continue

        if not data:
            print(f"  No valid rating data found in {file_path}")
            return

        # Create DataFrame and calculate means
        df = pd.DataFrame({'Rating': data})
        df['interval'] = df.index // 2
        rating_means = df.groupby('interval')['Rating'].mean().reset_index()
        
        # Save results
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        rating_means.to_csv(output_path, index=False)
        
        # Print summary
        print(f"  Processed {len(df)} ratings into {len(rating_means)} intervals")
        print(f"  Saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


def main():
    # Create output directory
    output_dir = 'output_aggregated'
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all CSV files in Engagement directory and subdirectories
    engagement_dir = 'Engagement'
    csv_files = []
    
    for root, _, files in os.walk(engagement_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    if not csv_files:
        print("No CSV files found in the Engagement directory")
        return
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Process each file
    for csv_file in csv_files:
        process_csv_file(csv_file, output_dir)
    
    print("\nAll files processed!")

if __name__ == "__main__":
    main()