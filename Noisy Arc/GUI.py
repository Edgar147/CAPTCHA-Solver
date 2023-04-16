import heapq
import os
import shutil
from tkinter import *

import cv2
from PIL import ImageTk,Image
from tkinter import filedialog
from solve_captcha import solve
root = Tk()
root.title("CAPTCHA_SOLVER")
root.geometry("500x500")
frame = Frame(root)
frame.pack()
path = ""
def details():

    root.filename = filedialog.askopenfilename(initialdir="C:\\Users\\karap\\Desktop\\M1\\IR\\CAPTCHA-Solver-master\\Noisy Arc\\samples", title="Select a file")
    #my_label = Label(root, text=root.filename).pack()
    path = root.filename
    
    img = ImageTk.PhotoImage(Image.open(root.filename))
    panel = Label(root, image = img)
    panel.image = img
    panel.configure(image=img)
    panel.pack(side = "top", fill = "both", expand = "no")
    L1 = Label(frame, text = "Input image", font = 14)
    L1.pack( side = BOTTOM)
    
    solvec(path)

def solvec(path):

    print(path)
    print(path)

    filename=path[-9:]
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Apply adaptive thresholding to binarize the image
    threshold_value = 127
    max_value = 255
    _, thresh = cv2.threshold(img, threshold_value, max_value, cv2.THRESH_BINARY)
    # img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # print(img)
    # Save the binarized image in the 'bins' folder
    cv2.imwrite(os.path.join('essai_GUI/', filename), thresh)

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    # Define a function to get the neighbors of a pixel
    def get_neighbors(x, y):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < width and 0 <= y + j < height:
                    pixel = img.getpixel((x + i, y + j))
                    if pixel < 255:
                        neighbors.append((x + i, y + j))
        return neighbors

    folder_path = 'essai_GUI'

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
    # img = Image.open('b.png').convert('L')
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
                        distance = manhattan_distance(node, neighbor)  # Manhattan distance
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
                        heapq.heappush(queue, (distance + weight, neighbor))

            if right not in distances:
                img.putpixel(left, 255)
                left = findLeftPixelNonWith(width, height, img)
                continue
        # Draw the shortest path on the image
        x, y = right
        # img = img.convert('RGB')

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

                if y > 0:
                    img.putpixel((x, y - 1), 255)
                if y > 1:
                    img.putpixel((x, y - 2), 255)
                if y < img.height - 1:
                    img.putpixel((x, y + 1), 255)
                if y < img.height - 2:
                    img.putpixel((x, y + 2), 255)

            for edge in graph[(x, y)]:
                weight, neighbor = edge
                print(file_path)
                if distances[neighbor] == distances[(x, y)] - weight:
                    x, y = neighbor
                    break

        x = 0
        while x <= 29:
            y = 0
            while y <= img.height - 1:
                img.putpixel((x, y), 255)
                y = y + 1
            x = x + 1

        # Save the image
        # new_file_path = file_path.replace('binaire_start\\', '')

        # img.save(os.path.join('image_binary', new_file_path))

        img.save(os.path.join('essai_GUI/',filename))

        new_path = path.replace("samples", "essai_GUI")
















    text1 = solve(new_path)

    # Get a list of all files and directories within 'essai_GUI'
    contents = os.listdir('essai_GUI')

    # Loop over the contents and delete each file or directory
    for item in contents:
        item_path = os.path.join('essai_GUI', item)
        if os.path.isfile(item_path):            os.remove(item_path)
        else:
            os.rmdir(item_path)

    L4 = Label(frame, text = "Output: {}".format(text1), font = 14)
    L4.pack( side = BOTTOM)

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM)

L2 = Label(frame, text="CAPTCHA SOLVER", font = 18)
L2.pack(side = TOP)
L5 = Label(frame, text=" ", font = 18)
L5.pack(side = TOP)

L3 = Label(frame, text="Select a CAPTCHA image", font = 14)
L3.pack (side = TOP)
L6 = Label(frame, text=" ", font = 18)
L6.pack(side = TOP)
L8 = Label(frame, text=" ", font = 18)
L8.pack(side = TOP)
B1 = Button(bottomframe, text ="Select", command = details)

B1.pack()

root.mainloop()
