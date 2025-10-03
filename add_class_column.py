import pandas as pd
import os

def get_class(rating):
    if -2 <= rating <= 1:
        return 0
    elif 1 < rating <= 2:
        return 1
    # elif 1.5 <= rating <= 2:
    #     return 2
    # elif 1 < rating <= 2:
    #     return 3
    else:
        return None

def process_file(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'Rating' in df.columns:
            df['class'] = df['Rating'].apply(get_class)
            df.to_csv(file_path, index=False)
            return True, file_path
        return False, f"No 'Rating' column in {file_path}"
    except Exception as e:
        return False, f"Error processing {file_path}: {str(e)}"

def main():
    directory = '/home/lucas/Desktop/Student_engagement/output_aggregated/'
    processed = 0
    errors = []
    
    print("Processing files...")
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            success, message = process_file(file_path)
            if success:
                print(f" Processed: {filename}")
                processed += 1
            else:
                print(f" {message}")
                errors.append(message)
    
    print(f"\nSummary:")
    print(f"Successfully processed: {processed} files")
    if errors:
        print(f"Errors occurred in {len(errors)} files:")
        for error in errors:
            print(f"  - {error}")
    
    print("\nClass mapping:")
    print("  -2 ≤ rating ≤ -1: class 0")
    print("  -1 < rating ≤  0: class 1")
    print("   0 < rating ≤  1: class 2")
    print("   1 < rating ≤  2: class 3")

if __name__ == "__main__":
    main()