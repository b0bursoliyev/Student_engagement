import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def plot_engagement_data(csv_path, output_dir='engagement_plots'):
    """
    Generate multiple visualizations for engagement data.
    
    Args:
        csv_path (str): Path to the CSV file with engagement data
        output_dir (str): Directory to save the plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the data
    df = pd.read_csv(csv_path)
    filename = Path(csv_path).stem  # Get filename without extension
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')  # Updated style for newer matplotlib
    sns.set_theme(style="whitegrid")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Line plot
    ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
    sns.lineplot(data=df, x='interval', y='Rating', ax=ax1, marker='o')
    ax1.set_title(f'Engagement Rating Over Time - {filename}')
    ax1.set_xlabel('Interval (7-row groups)')
    ax1.set_ylabel('Mean Rating')
    ax1.grid(True, alpha=0.3)
    
    # 2. Bar plot
    ax2 = plt.subplot2grid((3, 2), (1, 0))
    sns.barplot(data=df, x='interval', y='Rating', ax=ax2)
    ax2.set_title('Engagement by Interval')
    ax2.set_xlabel('Interval')
    ax2.set_ylabel('Mean Rating')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 3. Distribution plot
    ax3 = plt.subplot2grid((3, 2), (1, 1))
    sns.histplot(data=df, x='Rating', kde=True, ax=ax3, bins=15)
    ax3.set_title('Distribution of Engagement Ratings')
    ax3.set_xlabel('Rating')
    ax3.set_ylabel('Frequency')
    
    # 4. Box plot
    ax4 = plt.subplot2grid((3, 2), (2, 0))
    sns.boxplot(data=df, y='Rating', ax=ax4)
    ax4.set_title('Engagement Rating Distribution')
    ax4.set_ylabel('Rating')
    
    # 5. Rolling mean (smoothed line)
    ax5 = plt.subplot2grid((3, 2), (2, 1))
    rolling_mean = df['Rating'].rolling(window=3, min_periods=1).mean()
    sns.lineplot(data=df, x='interval', y='Rating', ax=ax5, alpha=0.5, label='Original')
    sns.lineplot(x=df['interval'], y=rolling_mean, ax=ax5, color='red', label='Rolling Mean (3)')
    ax5.set_title('Engagement Rating with Rolling Mean')
    ax5.set_xlabel('Interval')
    ax5.set_ylabel('Rating')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    
    # Save the combined plot
    output_path = os.path.join(output_dir, f'{filename}_combined.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualizations saved to: {output_path}")
    
    # Create and save individual plots
    plot_individual_plots(df, filename, output_dir)

def plot_individual_plots(df, filename, output_dir):
    """Create and save individual plots for each visualization."""
    # 1. Line plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='interval', y='Rating', marker='o')
    plt.title(f'Engagement Rating Over Time - {filename}')
    plt.xlabel('Interval (7-row groups)')
    plt.ylabel('Mean Rating')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{filename}_line.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Heatmap (for patterns across intervals)
    plt.figure(figsize=(12, 6))
    # Create a pivot table for heatmap (example: first 20 intervals for better visualization)
    if len(df) > 0:  # Only create heatmap if there's data
        heatmap_data = df.head(20).pivot_table(values='Rating', 
                                             columns='interval', 
                                             aggfunc='mean')
        sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.2f', cbar_kws={'label': 'Engagement Rating'})
        plt.title(f'Engagement Heatmap - {filename}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{filename}_heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    # Example usage:
    # You can modify this to process a specific file or loop through multiple files
    import sys
    
    if len(sys.argv) > 1:
        # If file path is provided as command line argument
        csv_file = sys.argv[1]
        plot_engagement_data(csv_file)
    else:
        # Otherwise, process all CSV files in the output_aggregated directory
        input_dir = 'output_aggregated'
        output_dir = 'engagement_plots'
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each CSV file
        for file in os.listdir(input_dir):
            if file.endswith('_means.csv'):
                file_path = os.path.join(input_dir, file)
                print(f"Processing: {file}")
                try:
                    plot_engagement_data(file_path, output_dir)
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
        
        print("\nAll visualizations have been generated in the 'engagement_plots' directory.")
        print("To visualize a specific file, run: python visualize_engagement.py path/to/your/file.csv")
