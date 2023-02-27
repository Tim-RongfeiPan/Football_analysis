import cv2
import os

import re
import numpy as np
from loguru import logger

from sklearn.cluster import KMeans

# RGB code
All_colors = {'Yellow': (195, 195, 10),
              'White': (235, 235, 235),
              'Green': (10, 235, 10),
              'Blue': (10, 10, 205),
              'Black': (0, 0, 0),
              'Red': (235, 30, 30),
              'Purple': (160, 32, 240),
              'Orange': (255, 165, 30),
              'Dark': (85, 85, 85)}

file_dict = {'frej-bp.txt': ['White-Yellow.png', 'Yellow-White.png'],
             'IF Brommapojkarna - Örebro Syrianska IF.txt': ['Yellow-RedBlack.png', 'RedBlack-Yellow.png'],
             'IF Sylvia - Team TG FF.txt': ['BlackWhite-Red.png', 'Red-BlackWhite.png'],
             'IFK Berga - IF Sylvia.txt': ['Orange-White.png', 'White-Orange.png'],
             'IFK Värnamo - FC Linköping City.txt': ['White-Blue.png', 'Blue-White.png'],
             'Nyköpings BIS - IFK Haninge.txt': ['Black-Red.png', 'Red-Black.png'],
             'Qviding FIF - Landskrona BoIS.txt': ['Dark-BlackWhite.png', 'BlackWhite-Dark.png'],
             'Qviding FIF - Lunds BK.txt': ['Red-Yellow.png', 'Yellow-Red.png'],
             'Qviding FIF - Skövde AIK.txt': ['Red-Green.png', 'Green-Red.png'],
             'Skövde AIK - FC Linköping City.txt': ['Blue-Red.png', 'Red-Blue.png'],
             'Torns IF - Motala AIF FK.txt': ['Orange-White2.png', 'White-Orange2.png'],
             'Tvååkers IF - Landskrona BoIS.txt': ['BlackWhite-Red2.png', 'Red-BlackWhite2.png'],
             'Utsikten - Lindome GIF.txt': ['Dark-White.png', 'White-Dark.png']}


def detect_color(img, colors, debug=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[1]*img.shape[0], 3))

    kmeans = KMeans(n_clusters=4, n_init=10)
    s = kmeans.fit(img)

    labels = s.labels_
    centroid = s.cluster_centers_
    labels = list(labels)
    percent = []

    for i in range(len(centroid)):
        j = labels.count(i)
        j = j/(len(labels))
        percent.append(j)

    detected_color = centroid[np.argsort(percent)[-2]]
    list_of_colors = []
    for i in colors:
        list_of_colors.append(All_colors[i])

    if debug:
        logger.info(percent)
        logger.info(centroid)
        logger.info(detected_color)

    assigned_color = closest_color(list_of_colors, detected_color)[0]
    assigned_color = (int(assigned_color[0]), int(
        assigned_color[1]), int(assigned_color[2]))

    # colorName = colors[0] if All_colors[colors[0]
    #                                         ] == assigned_color else colors[1]
    colorName = ''
    for color in colors:
        if All_colors[color] == assigned_color:
            colorName = color
            break
    return assigned_color, colorName


# Find the closest color to the detected one based on the predefined palette
def closest_color(list_of_colors, color):
    colors = np.array(list_of_colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    index_of_shortest = np.where(distances == np.amin(distances))
    shortest_distance = colors[index_of_shortest]
    return shortest_distance


def team_assignment(crop, infoFile, debug=False):
    # detect the crop image to find the corresponding team from infoFile
    with open(infoFile, 'r') as f:
        data = f.read()
        two_colors = re.findall(
            r'team, (.*?) [J,j]erseys[)]', data)
        colors = []
        for color in two_colors:
            if color.find('/') != -1:
                newcolorName = color
                if newcolorName[0].islower():
                    newcolorName = newcolorName.capitalize()
                newcolors = color.split('/')
                for index, color in enumerate(newcolors):
                    if color[0].islower():
                        newcolors[index] = color.capitalize()
                newcolor = ((All_colors[newcolors[0]][0] +
                             All_colors[newcolors[1]][0])/2, (All_colors[newcolors[0]][1] +
                                                              All_colors[newcolors[1]][1])/2, (All_colors[newcolors[0]][2] +
                                                                                               All_colors[newcolors[1]][2])/2)
                All_colors[newcolorName] = newcolor
                colors.append(newcolorName)
            else:
                colors.append(color)
        for index, color in enumerate(colors):
            if color[0].islower():
                colors[index] = color.capitalize()
    color, colorName = detect_color(
        crop, colors, debug=debug)
    return colorName


if __name__ == '__main__':

    root_path = '../datasets/test'
    file_list = os.listdir(root_path)
    test_image_list = []
    test_txt_list = []
    for file in file_list:
        if file.endswith('.png'):
            test_image_list.append(file)
        elif file.endswith('.txt'):
            test_txt_list.append(file)

    all = 0
    correct = 0

    for (txt_file, image_file) in file_dict.items():
        txt_path = root_path+'/'+txt_file

        with open(txt_path, 'r') as f:
            data = f.read()
            two_colors = re.findall(
                r'team, (.*?) [J,j]erseys[)]', data)
            colors = []
            for color in two_colors:
                if color.find('/'):
                    colors += color.split('/')
                else:
                    colors.append(color)
            for index, color in enumerate(colors):
                if color[0].islower():
                    colors[index] = color.capitalize()
        for image_path in image_file:
            crop_path = root_path+'/'+image_path
            results = image_path.split('-')[0]
            crop_path = root_path+'/'+image_path
            crop = cv2.imread(crop_path)
            colorName = team_assignment(crop, txt_path)
            if colorName in results:
                correct += 1
            else:
                logger.info(
                    f'processing file: {txt_file} and {image_path},' +
                    f'colors: {colors}, results: {results}')
                logger.info(f'prac results: {colorName}')
                colorName = team_assignment(crop, txt_path, debug=True)
            all += 1

    acc = correct/all
    logger.info(f'{all},{correct}')
    logger.info(f'Accuracy: {acc}')
