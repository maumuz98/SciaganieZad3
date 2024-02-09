#Maurycy Muzyka 285730
#Zadanie 3

import requests
from bs4 import BeautifulSoup
import io
from pathlib import Path
from PIL import Image

import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

import cv2
import numpy as np

wielowatkowo = 1    #0 - nie; 1 - tak
gauss = 0           #0 - nie; 1 - tak

page_url = "https://"
page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')

pngs = []
pngs2 = soup.find_all('a')
for i in range(len(pngs2)):
    line = str(pngs2[i])
    if line.find(".png") > 0:
        #pngs.append(pngs2[i])
        print(line)
        start = line.find("\"") + 1
        pngs.append(line[start : line.find(".png") + 4])

n = len(pngs)
print("Znaleziono", n, "zdjec png:")

pngUrls = []
for i in range(n):
    pngUrls.append(page_url + pngs[i])

for i in range(n): 
    print(pngUrls[i])

def sciagaj(ii): #sciaga 1 obrazek
    image_content = requests.get(pngUrls[ii]).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    if gauss == 1:
        #https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
        image = np.array(image)
        image = cv2.GaussianBlur(image, (3, 3), 1/3)
        cv2.imwrite("G" + str(pngs[ii]), image)
        print("Zapisano", "G" + str(pngs[ii]))
    else:
        file_path = Path("E:/Dokumenty/Studia/Semestr IX/Programowanie Rownolegle/wdprir2023python-main/wdprir2023python-main/src/",
                         str(pngs[ii]))
        image.save(file_path, "PNG", quality=80)
        print("Zapisano", str(pngs[ii]))

start = time.time()

if wielowatkowo == 1:
    with ThreadPoolExecutor(multiprocessing.cpu_count()) as ex:
        futures = [ex.submit(sciagaj, i) for i in range(n)]
        results = [future.result() for future in futures]
else:
    for i in range(n):
        sciagaj(i)

end = time.time()
print(f'{end - start = }')

#10 obrazow png
#bez Gaussa, nierownolegle  t = 126.3 s / 122.53 s
#bez Gaussa, rownolegle     t = 63.0 s / 60.3 s
#Gauss,      nierownolegle  t = 63.3 s / 67.0 s
#Gauss,      rownolegle     t = 39.2 s / 39.3 s
