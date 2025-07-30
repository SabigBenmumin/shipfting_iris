import time
import multiprocessing as mp
import numpy as np
import os
import cv2
from multiprocessing.connection import Listener

def read_image(image_path):
    """Read an image from the specified path."""
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return gray_image

def worker(wid, template_size, start_index, in_queue, out_queue):
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    
    bitcount_lookup = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)
    packed_template2 = np.ndarray(shape=(template_size,6400,), dtype=np.uint8)
    init_path = '/home/surasak'
    total_template = 0
    for f in range(start_index,60):
        for i in range(20):
            template = read_image(os.path.join(init_path, 'data', \
                    f'CASIA-IrisV2/device2/00{str(f).zfill(2)}_template/00{str(f).zfill(2)}_0{str(i).zfill(2)}.bmp'))[:, :, 0]
            packed_template2[total_template,:] = np.packbits(template.flatten())
            total_template += 1
            if total_template == template_size:
                break
        if total_template == template_size:
            break
    print(f"[Worker {wid}] loaded {total_template} templates started from f={start_index} ended with f={f}, i={i} ")

    while True:
        #print(f"[Worker {wid}] waiting for event...")
        idx, template = input_queue.get()
        print(f'[Worker {wid}] received : {template[0,0:10]}')
        ts = time.time_ns()
        hd_all = []
        for k in range(template_size):
            hd = []
            for i in range(17):
                packed_template = template[i,:]
                C = np.bitwise_xor(packed_template, packed_template2[k,:])
                HD = np.sum(bitcount_lookup[C])/51200.0
                hd.append(HD)
            hd_all.append(hd)
        te = (time.time_ns() - ts) / 1_000_000
        #print(f'Execution time {te}')
        hd_all_np = np.asarray(hd_all)
        #print(f'hd_all_np shape {hd_all_np.shape}')
        #np.copyto(shared_array_out[start_index*20,:], hd_all_np)
        out_queue.put((wid, hd_all_np))

if __name__ == "__main__":
    num_workers = 4
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    
    for i in range(num_workers):
        mp.Process(target=worker, args=(i, int(1200/num_workers), i*int(60/num_workers), \
                input_queue, output_queue), daemon=True).start()
        #p.start()
        #p.join()
    
    address=('localhost', 6000)
    authkey=b'sabig'
    listener = Listener(address, authkey=authkey)
    
    while True:
        conn = listener.accept()
        finished_processes = 0
        #print(f"[Server] Connection accepted from {listener.last_accepted}")
        input_template = conn.recv()  # accept numpy array
        #print(f'Example input: {input_template[0,0:10]}')
        #print(input_template)
        #print(input_template.shape)
        # Copy data to our shared array.
        for i in range(num_workers):
            input_queue.put((i,input_template))
            
        #time.sleep(5) # Simulate some work in the main process
        #print("Main process setting the event.")
        #Wait for all process finished
        finishedProcesses = []
        while len(finishedProcesses) < num_workers:
            idx, result = output_queue.get()
            finishedProcesses.append([idx, result])
            #print(f'Worker {idx} finished')
        conn.send(finishedProcesses)
        #print("Main process finished.")
        
