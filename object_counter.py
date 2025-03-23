import matplotlib.pyplot as plt
import json
from collections import Counter
import random
import seaborn as sns   

def count_objects(text_file_path):
    
    object_counter = Counter()
    with open(text_file_path, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            parts = line.split(":", 1)  
            if len(parts) == 2:  
                objects = parts[1].strip()  
                if objects:  
                    for obj in objects.split(","):  
                        object_counter[obj.strip()] += 1  
    return object_counter

def plot_object_distribution(object_counts, output_path):
    objects = list(object_counts.keys())
    counts = list(object_counts.values())
    plt.figure(figsize=(10, 6))
    sns.barplot(x=objects, y=counts, palette='viridis')
    plt.xlabel('Objects')
    plt.ylabel('Counts')
    plt.title('Object Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()




def plot_scatter(object_counts, output_path):
    
    objects = list(object_counts.keys())
    counts = list(object_counts.values())
    x_coords = range(1, len(objects) + 1)  
    y_coords = counts
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x_coords, y=y_coords, marker='o', label='Object Counts', color='blue')
    plt.xlabel('Objects (Sequential Index)')
    plt.ylabel('Counts')
    plt.title('Scatter Plot of Object Counts')
    plt.xticks(ticks=x_coords, labels=objects, rotation=45, ha='right')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
