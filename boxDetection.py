import cv2
import numpy as np
import os
import tempfile
# to activate virtual environment in windows & f:/allora/venv/Scripts/Activate.ps1


def detect_characters(sheet_image, threshold_value, cols=8, rows=10):

    # Read the image and convert to grayscale
    image = cv2.imread(sheet_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold and filter the image for better contour detection
    _, thresh = cv2.threshold(gray, threshold_value, 255, 1)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(
        thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)

    # Search for contours.
    contours, h = cv2.findContours(
        close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter contours based on number of sides and then reverse sort by area.
    contours = sorted(
        filter(
            lambda cnt: len(
                cv2.approxPolyDP(
                    cnt, 0.01 * cv2.arcLength(cnt, True), True)
            )
            == 4,
            contours,
        ),
        key=cv2.contourArea,
        reverse=True,
    )

    # Calculate the bounding of the first contour and approximate the height
    # and width for final cropping.
    x, y, w, h = cv2.boundingRect(contours[0])
    space_h, space_w = 7 * h // 16, 7 * w // 16

    # Since amongst all the contours, the expected case is that the 4 sided contours
    # containing the characters should have the maximum area, so we loop through the first
    # rows*colums contours and add them to final list after cropping.
    characters = []
    for i in range(rows * cols):
        x, y, w, h = cv2.boundingRect(contours[i])
        cx, cy = x + w // 2, y + h // 2

        roi = image[cy - space_h+3: cy + space_h -
                    3, cx - space_w+3: cx + space_w-3]
        characters.append([roi, cx, cy])

    # Now we have the characters but since they are all mixed up we need to position them.
    # Sort characters based on 'y' coordinate and group them by number of rows at a time. Then
    # sort each group based on the 'x' coordinate.
    characters.sort(key=lambda x: x[2])
    sorted_characters = []
    for k in range(rows):
        sorted_characters.extend(
            sorted(characters[cols * k: cols * (k + 1)],
                   key=lambda x: x[1])
        )

    return sorted_characters


def save_images(characters, characters_dir_name):
    temPath = os.path.join(tempfile.gettempdir(), characters_dir_name)
    if not os.path.isdir(temPath):
        os.mkdir(temPath)
    # dictionary to rename the values
    dic = {
        1: "aupper",
        2: "bupper",
        3: "cupper",
        4: "dupper",
        5: "eupper",
        6: "fupper",
        7: "gupper",
        8: "hupper",
        9: "iupper",
        10: "jupper",
        11: "kupper",
        12: "lupper",
        13: "mupper",
        14: "nupper",
        15: "oupper",
        16: "pupper",
        17: "qupper",
        18: "rupper",
        19: "supper",
        20: "tupper",
        21: "uupper",
        22: "vupper",
        23: "wupper",
        24: "xupper",
        25: "yupper",
        26: "zupper",
        27: "a",
        28: "b",
        29: "c",
        30: "d",
        31: "e",
        32: "f",
        33: "g",
        34: "h",
        35: "i",
        36: "j",
        37: "k",
        38: "l",
        39: "m",
        40: "n",
        41: "o",
        42: "p",
        43: "q",
        44: "r",
        45: "s",
        46: "t",
        47: "u",
        48: "v",
        49: "w",
        50: "x",
        51: "y",
        52: "z",
        53: "0",
        54: "1",
        55: "2",
        56: "3",
        57: "4",
        58: "5",
        59: "6",
        60: "7",
        61: "8",
        62: "9",
        63: "fullstop",
        64: "comma",
        65: "semicolon",
        66: "colon",
        67: "exclamation",
        68: "question",
        69: "doubleinvertedcomma",
        70: "singleinvertedcomma",
        71: "minus",
        72: "plus",
        73: "equal",
        74: "slash",
        75: "percentage",
        76: "ampersand",
        77: "leftparenthesis",
        78: "rightparenthesis",
        79: "leftsquarebracket",
        80: "rightsquarebracket"
    }

    for k, images in enumerate(characters):
        cv2.imwrite(os.path.join(os.path.join(tempfile.gettempdir(),
                    characters_dir_name), dic[k+1] + ".png"), images[0])

# Function 1 to crop images


def purpleCrop():
    for imgs in os.listdir(os.path.join(tempfile.gettempdir(), "tempfont")):
        img = cv2.imread(os.path.join(os.path.join(
            tempfile.gettempdir(), "tempfont"), imgs))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255*(gray < 128).astype(np.uint8)  # To invert the text to white
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords)
        rect = img[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(os.path.join(tempfile.gettempdir(),
                    "tempfont"), imgs), rect)  # Save the image

# Function 2 to crop images


def blueCrop():
    for imgs in os.listdir(os.path.join(tempfile.gettempdir(), "tempfont")):
        img = cv2.imread(os.path.join(os.path.join(
            tempfile.gettempdir(), "tempfont"), imgs))
        # Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        # perform edge detection,
        edged = cv2.Canny(blurred, 30, 150)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(edged, rect_kernel, iterations=1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        idx = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Drawing a rectangle on copied image
            # rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.imwrite("rect.png", im2)
            nImg = img[y:y+h, x:x+w]
            idx += 1
            cv2.imwrite(os.path.join(os.path.join(
                tempfile.gettempdir(), "tempfont"), imgs), nImg)
            if idx >= 1:
                break


# Function to add padding
def padder(tempfontPath):
    lower_list = ["a",  "c",  "e",  "g",   "j",
                  "m", "n", "o", "p", "q", "r", "s", "u", "v", "w", "x", "y", "z"]
    upper_list = ["aupper", "bupper", "cupper", "dupper", "eupper", "fupper", "gupper", "hupper", "iupper", "jupper", "kupper", "lupper",
                  "mupper", "nupper", "oupper", "pupper", "qupper", "rupper", "supper", "tupper", "uupper", "vupper", "wupper", "xupper", "yupper",
                  "zupper", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "exclamation", "question", "percentage", "slash", "ampersand", "leftparenthesis",
                  "rightparenthesis", "leftsquarebracket", "rightsquarebracket", "singleinvertedcomma", "doubleinvertedcomma"]
    lower_spc = ["b", "d", "f", "h", "k", "l", "t", "i"]
    special_char_1 = ["fullstop", "comma"]
    special_char_2 = ["colon", "minus", "plus", "equal", "semicolon"]
    for imgs in os.listdir(tempfontPath):
        img = cv2.imread(os.path.join(tempfontPath, imgs))
        imgName = os.path.splitext(imgs)[0]
        if imgName in lower_list:
            new_img = cv2.copyMakeBorder(
                img, 18, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(os.path.join(tempfontPath, imgs), new_img)
        elif imgName in lower_spc:
            new_img = cv2.copyMakeBorder(
                img, 10, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(os.path.join(tempfontPath, imgs), new_img)
        elif imgName in upper_list:
            new_img = cv2.copyMakeBorder(
                img, 9, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(os.path.join(tempfontPath, imgs), new_img)
        elif imgName in special_char_1:
            new_img = cv2.copyMakeBorder(
                img, 28, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(os.path.join(tempfontPath, imgs), new_img)
        elif imgName in special_char_2:
            new_img = cv2.copyMakeBorder(
                img, 25, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(os.path.join(tempfontPath, imgs), new_img)
        else:
            continue


def box_activator(fontimagePath):
    # Input image path and out folder and is fed to box detection algorithm
    charac = detect_characters(
        sheet_image=fontimagePath, threshold_value=127, cols=8, rows=10)
    save_images(characters=charac, characters_dir_name="tempfont")

    tempPathdir2 = os.path.join(tempfile.gettempdir(), "tempfont")
    purpleCrop()
    padder(tempPathdir2)
    # os.rmdir(os.path.join(tempfile.gettempdir(),"tempfont"))


# box_activator("inpT.jpg")
