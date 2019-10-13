import time

import cv2
import requests
import json

img = cv2.imread("resources/images/world_map_grid.png")
height, width, channels = img.shape


def getLongitudeAndLatitude():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    position = json.loads(response.text)

    longitude = position["iss_position"]["longitude"]
    latitude = position["iss_position"]["latitude"]

    return float(longitude), float(latitude)


def convertToPosition():
    longitude, latitude = getLongitudeAndLatitude()

    if longitude < 0:
        normalised_longitude = int(180 - longitude)
    else:
        normalised_longitude = int(180 + longitude)

    x_ratio = normalised_longitude / 360
    x_position = x_ratio * width

    if latitude < 0:
        normalised_latitude = int(90 - latitude)
    else:
        normalised_latitude = int(90 + latitude)

    y_ratio = normalised_latitude / 180
    y_position = y_ratio * height

    return int(x_position), int(y_position)


while True:
    x_pos, y_pos = convertToPosition()
    cv2.circle(img, (x_pos, y_pos), 3, (0, 255, 0), -1)
    cv2.imshow("ISS Tracker", img)
    k = cv2.waitKey(2) & 0XFF
    if k == 27:
        break

cv2.destroyAllWindows()
