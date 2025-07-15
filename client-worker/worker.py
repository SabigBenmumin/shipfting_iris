import multiprocessing as mp
import numpy as np
from multiprocessing.connection import Listener

def worker(input_queue, output_queue, wid):
    bitcount_lookup = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)
    while True:
        task = input_queue.get()
        if task is None:
            # continue
            break
        idx, input_template, data = task
        result = np.ndarray(shape=(data.shape[0],), dtype=np.uint32)
        
        for i in range(data.shape[0]):
            C = np.bitwise_xor(input_template, data[i])
            # dist = np.sum(bitcount_lookup[C])
            result[i] = np.sum(bitcount_lookup[C])
        output_queue.put((idx, result))
    

# def worker(input_queue, output_queue, wid):
#     print(f"[Worker {wid}] started")
#     while True:
#         task = input_queue.get()
#         if task is None:
#             continue  # ignore shutdown signal
#         idx, data = task
#         print(f"[Worker {wid}] working on task {idx} with data {data}")
#         result = np.sum(data, axis=1)
#         output_queue.put((idx, result))

def start_worker_server(address=('localhost', 6000), authkey=b'sabig'):
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    num_workers = 4

    for i in range(num_workers):
        mp.Process(target=worker, args=(input_queue, output_queue, i), daemon=True).start()

    listener = Listener(address, authkey=authkey)
    task_id = 0
    print("[Server] Ready. Waiting for connection...")

    while True:
        conn = listener.accept()
        print(f"[Server] Connection accepted from {listener.last_accepted}")
        try:
            input_template ,data = conn.recv()  # รับ numpy array
            print(f"[Server] Got task shape: {data.shape}")
            chunk_size = len(data) // num_workers
            for i in range(num_workers):
                chunk = data[i*chunk_size:(i+1)*chunk_size]
                input_queue.put((i, input_template, chunk))

            results = [None] * num_workers
            for _ in range(num_workers):
                idx, result = output_queue.get()
                results[idx] = result

            final = np.concatenate(results)
            conn.send(final)  # ส่งกลับไปให้ client
            print(f"[Server] Done. Result shape: {final.shape}")
        except Exception as e:
            print(f"[Server] Error: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    mp.set_start_method("spawn")  # Windows support
    start_worker_server()
