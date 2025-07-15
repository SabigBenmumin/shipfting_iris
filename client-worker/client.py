from multiprocessing.connection import Client
import numpy as np
import time
import csv
import os

def send_task(input_template ,array, address=('localhost', 6000), authkey=b'sabig'):
    conn = Client(address, authkey=authkey)
    print("[Client] Sending array...")
    conn.send((input_template ,array))

    result = conn.recv()
    print(f"[Client] Got result with shape: {result.shape}")
    conn.close()
    return result

if __name__ == '__main__':
    # เตรียม input (ในระบบจริงเปลี่ยนตรงนี้ได้ เช่นจากภาพ, ไฟล์, socket ฯลฯ)
    # arr = np.random.rand(100000, 6400).astype(np.uint8)
    # arr = np.asarray([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1],])
    template1 = np.load(r'C:\Users\Sabig\Iris\shifting example\input_template.npy')
    arr = np.load(r'C:\Users\Sabig\Iris\shifting example\duplicate_templates_100k.npy')
    
    # print("what I send to worker:")
    # print(arr)
    
    start = time.perf_counter()
    result = send_task(template1, arr)
    duration = time.perf_counter() - start
    print(f"duration time {duration} sec for {arr.shape[0]:,.0f} templates")
    print(result)
    print(result.shape)
    print(type(result[0]))

    # csv_path = "optimize_result_statistics/worker-client.csv"
    # write_header = not os.path.exists(csv_path)
    # with open(csv_path, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     if write_header:
    #         writer.writerow(["multiprocessing_by_client-worker"])
    #     writer.writerow([(duration/arr.shape[0])*1000])