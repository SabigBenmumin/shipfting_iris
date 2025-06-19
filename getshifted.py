import cv2
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool, cpu_count
from iris_module import HammingDistance, jaccard_distance_shifted, pearson_correlation_shifted

def read_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

dataset_path = r"C:\Users\Sabig\Iris\shifting example\Iris-Dataset\CASIA-IrisV2\device2"
tem1_path = 'C:\\Users\\Sabig\\Iris\\shifting example\\Iris-Dataset\\CASIA-IrisV2\\device2\\0023_template\\0023_000.bmp'
tem1 = cv2.imread(tem1_path, cv2.IMREAD_GRAYSCALE)

def get_flattened_mp(batch):
    results = []
    for folder, filename in batch:
        tem2 = cv2.imread(os.path.join(dataset_path, folder, filename), cv2.IMREAD_GRAYSCALE)
        hd_df = HammingDistance(template1=tem1, template2=tem2)
        jc_df = jaccard_distance_shifted(template1=tem1, template2=tem2)
        ps_df = pearson_correlation_shifted(template1=tem1, template2=tem2)
        flatten = [item for sublist in [hd_df[1], jc_df, ps_df] for item in sublist]
        results.append(flatten)
    return results

all_template_index = list()
for folder in os.listdir(dataset_path):
    for template in os.listdir(os.path.join(dataset_path, folder)):
        all_template_index.append([folder, template])
        last = (folder, template)

if __name__ == "__main__":
    total_time_using = 0
    num_threads = 4
    batch_size = len(all_template_index)//num_threads
    print("batching")
    batches = [all_template_index[i:i + batch_size] for i in range(0, len(all_template_index), batch_size)]

    start_t = time.time()
    with Pool(processes=num_threads) as pool:
        print("in pool")
        all_results = pool.map(get_flattened_mp, batches)
    flattened_data = pd.DataFrame([row for batch in all_results for row in batch])
    total_time_using= time.time() - start_t

    print(flattened_data)
    print("total time using:", total_time_using,"sec")
    print(f"average: {(total_time_using/len(all_template_index))*1000} ms/compare")
    print(f"total data compare {len(all_template_index)} times")