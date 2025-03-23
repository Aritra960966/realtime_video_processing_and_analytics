import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def parse_text_file_for_clustering(text_file_path):
    all_objects = set()
    data = []

    with open(text_file_path, 'r') as f:
        for line in f:
            _, objects = line.split(":", 1) if ":" in line else (None, "")
            objects = [obj.strip() for obj in objects.split(",") if obj.strip()]
            all_objects.update(objects)
            data.append(objects)

   
    all_objects = sorted(all_objects)  
    df = pd.DataFrame(0, index=range(len(data)), columns=all_objects)

    for i, objects in enumerate(data):
        for obj in objects:
            df.at[i, obj] = 1

    return df



def cluster_data(df, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df)

    
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(df)

    return cluster_labels, reduced_data

def plot_clusters(reduced_data, cluster_labels, output_path):
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        reduced_data[:, 0], reduced_data[:, 1],
        c=cluster_labels, cmap='viridis', s=50, alpha=0.7
    )
    plt.colorbar(scatter, label="Cluster")
    plt.xlabel("PCA Dimension 1")
    plt.ylabel("PCA Dimension 2")
    plt.title("Clustering Visualization")
    plt.tight_layout()

    
    plt.savefig(output_path)
    plt.close()
