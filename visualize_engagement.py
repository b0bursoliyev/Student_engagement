import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def plot_overall_class_counts(directory, output_path="overall_class_counts_original.png"):
    """Plot overall count of all engagement classes in one plot."""
    all_classes = []

    # Collect 'class' values from all CSVs
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_csv(file_path)
                if 'class' in df.columns:
                    all_classes.extend(df['class'].dropna().tolist())
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    if not all_classes:
        print("No class data found.")
        return

    # Plot countplot
    plt.figure(figsize=(8, 6))
    sns.countplot(x=all_classes, palette='Set2')
    plt.title("Overall Engagement Class Counts")
    plt.xlabel("Class")
    plt.ylabel("Count")

    # Add labels above bars
    counts = pd.Series(all_classes).value_counts().sort_index()
    for i, v in enumerate(counts):
        plt.text(i, v + 10, str(v), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Saved overall class count plot as {output_path}")


directory = '/home/lucas/Desktop/Student_engagement/output_aggregated/'
plot_overall_class_counts(directory)
