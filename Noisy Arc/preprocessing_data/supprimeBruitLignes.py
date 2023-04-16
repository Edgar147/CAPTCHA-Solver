from PIL import Image
import numpy as np
import heapq
import os
print("aaaa"+os.getcwd())

no_path_list = []

# Define a function to calculate the Manhattan distance between two points
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Define a function to get the neighbors of a pixel
def get_neighbors(x, y):
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if 0 <= x+i < width and 0 <= y+j < height:
                pixel = img.getpixel((x+i, y+j))
                if pixel < 255:
                    neighbors.append((x+i, y+j))
    return neighbors
folder_path = 'binaire_start'

def findLeftPixelNonWith(width, height, img):
    # Find the first non-white pixel from the left
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel < 255:
                left = (x, y)
                break
        else:
            continue
        break
    return left

def findRightPixelNonWith(width, height, img):
    # Find the first non-white pixel from the right
    for x in range(width - 1, -1, -1):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel < 255:
                right = (x, y)
                break
        else:
            continue
        break
    return right

# Open the image
#img = Image.open('b.png').convert('L')
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    img = Image.open(file_path).convert('L')
    # Get the image size
    width, height = img.size

    left = findLeftPixelNonWith(width, height, img)
    right = findRightPixelNonWith(width, height, img)


    # Replace the pixels with red
    img.putpixel(left, 150)
    img.putpixel(right, 150)

    # Create the graph
    graph = {}
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel < 255:
                node = (x, y)
                neighbors = get_neighbors(x, y)
                edges = []
                for neighbor in neighbors:
                    distance = manhattan_distance(node, neighbor) # Manhattan distance
                    edges.append((distance, neighbor))
                graph[node] = edges

    distances = {}
    while right not in distances:
        # Apply Dijkstra's algorithm
        distances = {}
        queue = []
        print(left)
        heapq.heappush(queue, (0, left))
        while queue:
            distance, node = heapq.heappop(queue)
            if node in distances:
                continue
            distances[node] = distance
            if node == right:
                break
            for edge in graph[node]:
                weight, neighbor = edge
                if neighbor not in distances:
                    heapq.heappush(queue, (distance+weight, neighbor))

        if right not in distances:
            img.putpixel(left, 255)
            left = findLeftPixelNonWith(width, height, img)
            continue
    # Draw the shortest path on the image
    x, y = right
    #img = img.convert('RGB')

    while (x, y) != left:
        black_above = 0
        black_below = 0
        if y > 0:
            black_above = img.getpixel((x, y - 1))
        if y > 1:
            black_above += img.getpixel((x, y - 2))
        if y < img.height - 1:
            black_below = img.getpixel((x, y + 1))
        if y < img.height - 2:
            black_below += img.getpixel((x, y + 2))

        if black_above + black_below >= 256:
            img.putpixel((x, y), 255)

            if y>0:
                img.putpixel((x, y-1), 255)
            if y>1:
                img.putpixel((x, y-2), 255)
            if y < img.height-1:
                img.putpixel((x, y+1), 255)
            if y < img.height-2:
                img.putpixel((x, y+2), 255)


        for edge in graph[(x, y)]:
            weight, neighbor = edge
            print(file_path)
            if distances[neighbor] == distances[(x, y)] - weight:
                x, y = neighbor
                break

    x = 0
    while x <= 29:
        y = 0
        while y <= img.height-1:
            img.putpixel((x, y), 255)
            y = y+1
        x = x+1

    # Save the image
    new_file_path = file_path.replace('binaire_start\\', '')

    img.save(os.path.join('image_binary', new_file_path))


