import random
import copy

# Constants
NUM_POINTS = 100
NUM_CLUSTERS = 10
GRID_SIZE = 50  # Assuming (x, y) between 0 and 49

# Generate data
points = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(NUM_POINTS)]
centers = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(NUM_CLUSTERS)]

# Save data
with open("data.txt", "w") as f:
    for p in points:
        f.write(f"P {p[0]} {p[1]}\n")
    for c in centers:
        f.write(f"C {c[0]} {c[1]}\n")

# Manhattan Distance
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# K-Means Clustering
def kmeans(points, centers):
    iteration = 0
    while True:
        iteration += 1
        clusters = {i: [] for i in range(len(centers))}

        # Assignment step
        for p in points:
            distances = [manhattan(p, c) for c in centers]
            cluster_idx = distances.index(min(distances))
            clusters[cluster_idx].append(p)

        # Update step
        new_centers = []
        for idx in range(len(centers)):
            if clusters[idx]:  # Avoid division by zero
                xs, ys = zip(*clusters[idx])
                new_x = round(sum(xs) / len(xs))
                new_y = round(sum(ys) / len(ys))
                new_centers.append((new_x, new_y))
            else:
                new_centers.append(centers[idx])  # If no points assigned

        if new_centers == centers:
            print(f"Converged after {iteration} iterations.")
            break
        centers = new_centers
    return clusters, centers

# Perform clustering
clusters, centers = kmeans(points, centers)

# Create visualization matrix
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Mark points
for cluster_idx, pts in clusters.items():
    for x, y in pts:
        grid[y][x] = "*"

# Mark centers
for x, y in centers:
    grid[y][x] = "C"

# Print the grid
for row in reversed(grid):  # Flip vertically so (0,0) is at bottom-left
    print("".join(row))
