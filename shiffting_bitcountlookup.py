import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def read_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return img

path = 'D:\\CASIA-IrisV2-20250213T083822Z-001'

# Shift the bits of the template
def shiftbits_ham(template, noshifts):
    templatenew = np.zeros(template.shape)
    width = template.shape[1]
    s = 2 * np.abs(noshifts)
    p = width - s

    # If no shift is needed, return the original template
    if noshifts == 0:
        templatenew = template

    # If the shift is positive, shift the bits to the right
    elif noshifts < 0:
        x = np.arange(p)
        templatenew[:, x] = template[:, s + x]
        x = np.arange(p, width)
        templatenew[:, x] = template[:, x - p]

    # If the shift is negative, shift the bits to the left
    else:
        x = np.arange(s, width)
        templatenew[:, x] = template[:, x - s]
        x = np.arange(s)
        templatenew[:, x] = template[:, p + x]

    return templatenew

#load all templates into memory
import glob
import os
#/home/tpoungla/irisIdentifier/Iris-Dataset/CASIA-IrisV2/device2/0000_template/0000_000.bmp
# files = glob.glob('/home/tpoungla/irisIdentifier/ris-Dataset/CASIA-IrisV2/device2/*_template/*.bmp')
# files = glob.glob('D:\\CASIA-IrisV2-20250213T083822Z-001\\CASIA-IrisV2\\device2\\*_template\\*.bmp')

base_path = r'C:/Users/Sabig/Iris/shifting example/Iris-Dataset/CASIA-IrisV2/device2/*_template/*.bmp'
files = glob.glob(base_path)
f_data_frame = pd.DataFrame(files)

template2 = np.ndarray(shape=(len(files),6400,), dtype=np.uint8)
# template2 = []
print("Number of files:", len(files))
# -----------------------------------------------------------
print()

start_time = datetime.now()
print("Start Time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

for i,file in enumerate(files):
    template1 = np.packbits(read_image(file).flatten())
    template2[i,:] = template1
# print(template2[0].shape) #(51200, )
# print(template2[0]) #

target = 100000
duplicate_templates = np.ndarray(shape=(target, 6400,), dtype=np.uint8) #153600

for i in range(target):
    duplicate_templates[i] = template2[i % len(template2)]  # Cycle through original templates

print("Final Number of files:", len(duplicate_templates))
# for f in duplicate_templates:
#     print(f)
end_time = datetime.now()
print("End Time:", end_time.strftime("%Y-%m-%d %H:%M:%S"))

duration = end_time - start_time
print("read loop Duration:", duration)
print()
#template1 = read_image(file)
# -----------------------------------------------------------
# timeStart = xxx
bitcount_lookup = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)
start_time = datetime.now()
t0 = time.time()
print("Start Time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))
import matplotlib.pyplot as plt
for i in range(target):
    # C = np.logical_xor(template1, duplicate_templates[i,:])
    C = np.bitwise_xor(template1, duplicate_templates[i,:])
    # plt.imshow(C.astype(np.uint8) * 255, cmap='gray')  # Multiply to make visible
    # plt.title(f"Difference Mask {i}")
    # plt.axis('off')
    # plt.show()
    # a = np.sum(np.unpackbits(C))
    a = np.sum(bitcount_lookup[C])
    # a = np.sum(C)
    #print (i)

# timeStop = yyyy
t1 = time.time()
end_time = datetime.now()
print("End Time:", end_time.strftime("%Y-%m-%d %H:%M:%S"))

duration = end_time - start_time
print("XOR loop Duration:", duration)
print(f"\t-> {t1-t0} sec for {target:,.0f} templates")
print(f"\t-> avg: {((t1-t0)/target)*1000} ms/template")
print("========================================================")
print()
# plt.imshow(duplicate_templates[0,:,:],cmap="gray")
# print(type(duplicate_templates[0,:,:]))
# print(template1)
# print(duplicate_templates[0])
# plt.show()

import csv
csv_path = "optimize_result_statistics/bitcountlookup_results.csv"
write_header = not os.path.exists(csv_path)
with open(csv_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(["bitcount_lookup"])
    writer.writerow([((t1-t0)/target)*1000])

print(a)

exit()
