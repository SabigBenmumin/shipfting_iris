# step 1: เปลี่ยนจาก `BGR` เป็น `Grayscale`  
โดยการเปลี่ยนการ input และ convert BGR2RGB -> input เป็น grayscale
**จาก:**
```python
def read_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
```
**เป็น:**
```python
def read_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return img
```

>[!Warning]
>ในโปรแกรมที่ใช้ทดสอบต้องเปลี่ยน shape ที่ใช้ duplicate template จาก `shape(len(files), 64, 800, 3)` => `shape(len(files), 64, 800)`
## ปัจจัยควบคุม
file templates ของจริงใช้: 1,200 file
target (duplicate templates) เป็น: 100,000 template
จำนวน loop ต่อการรัน โปรแกรม = target
ทดลองรันโปรแกรมละ 10 ครั้งต่อโปรแกรม
## ผล
**ก่อน :**
```powershell
Total records: 20
Path: C:/Users/Sabig/Iris/shifting example/before_optimize_results.csv
Performance Statistics (in milliseconds/compare):

before_optimize:
  Min:  0.751278 ms
  Max:  0.825900 ms
  Avg:  0.780630 ms
```
**หลัง :**
```powershell
Total records: 20
Path: C:/Users/Sabig/Iris/shifting example/grayscale_results.csv
Performance Statistics (in milliseconds/compare):

input as grayscale:
  Min:  0.126350 ms
  Max:  0.159186 ms
  Avg:  0.134396 ms
```
## สรุป:
| Step                  | Min (ms/compare) | Max (ms/compare) | Avg (ms/compare) |
| --------------------- | ---------------- | ---------------- | ---------------- |
| BGR (20 record)       | 0.751278         | 0.825900         | 0.780630         |
| Grayscale (20 record) | 0.126350         | 0.159186         | 0.134396         |
- ลดเวลาไป 82.78% หรือเหลือแค่ 17.22% จากของเดิม
- เร็วขึ้น 5.8 เท่า
# step 2: flatten and bitwise XOR
ขั้นตอนนี้ทำโดยการเปลี่ยนจาก `numpy array` shape (64, 800) เป็น (51200, )
และเปลี่ยนจากการ *XOR* ด้วย `logical_xor` เป็น `bitwise_xor`
## code
### templates data shape
**ก่อน**
```python
template2 = np.ndarray(shape=(len(files),64,800), dtype=np.uint8)
# template2 = []
print("Number of files:", len(files))
# -----------------------------------------------------------
print()

start_time = datetime.now()
print("Start Time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

for i,file in enumerate(files):
    template1 = read_image(file)
    template2[i,:,:] = template1
    #print(template1.shape) #64,800,3

target = 100000
duplicate_templates = np.ndarray(shape=(target, 64, 800), dtype=np.uint8) #153600
```
**หลัง**
```python
template2 = np.ndarray(shape=(len(files),51200,), dtype=np.uint8)
# template2 = []
print("Number of files:", len(files))
# -----------------------------------------------------------
print()

start_time = datetime.now()
print("Start Time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

for i,file in enumerate(files):
    template1 = read_image(file).flatten()
    template2[i,:] = template1
# print(template2[0].shape) #(51200, )
# print(template2[0]) #

target = 100000
duplicate_templates = np.ndarray(shape=(target, 51200,), dtype=np.uint8) #153600
```
### convert to flatten data
**ก่อน**
```python
for i,file in enumerate(files):
    template1 = read_image(file)
    template2[i,:,:] = template1
```
**หลัง**
```python
for i,file in enumerate(files):
    template1 = read_image(file).flatten()
    template2[i,:] = template1
```
---
>[!note]
>การทดสอบในตารางต่อไปนี้จะเป็นการทดสอบโดย labtop เครื่องเดียวกัน โดยควบคุมปัจจัยเรื่องการเสียบสายชาจขณะทดสอบทุกครั้ง
>โดยทดสอบบนเครื่องที่มีสเปคดังนี้
>**Processor**: AMD Ryzen 5 5600H with Radeon Graphics 3.30GHz
>**Installed Ram**: 16.0GB (15.4GB usable)
>**OS**: Windows 11

## เทียบเวลา
| Step                            | Min (ms/compare) | Max (ms/compare) | Avg (ms/compare) |
| ------------------------------- | ---------------- | ---------------- | ---------------- |
| BGR (20 record)                 | 0.751278         | 0.825900         | 0.780630         |
| Grayscale (20 record)           | 0.126350         | 0.159186         | 0.134396         |
| Flatten + bitwise XOR           | 0.065160         | 0.073099         | 0.067009         |
| sum(C == 1) -> sum(C)           | 0.048676         | 0.052370         | 0.050145         |
| packbits                        | 0.031929         | 0.043906         | 0.034713         |
| bitcount lookup                 | 0.025092         | 0.027408         | 0.025945         |
| multiprocessing (worker-client) | 0.021683         | 0.027497         | 0.023487         |
| *no send duplicate templates*   | 0.015970         | 0.017147         | 0.016397         |
# เปรียบเทียบผล 
>จากการรันโดยให้ duplicate template = 100,000

| วิธี                                                                            | Avg เวลา (ms) | % ลดลงจากก่อนหน้า | % ลดลงจากก่อน Optimize | ความเร็วเพิ่มจากก่อนหน้า | ความเร็วเพิ่มจากก่อน Optimize | ค่า sum ที่ได้จากการ compare ครั้งสุดท้าย(loop สุดท้าย) | แก้อะไร?                            |
| ------------------------------------------------------------------------------- | ------------- | ----------------- | ---------------------- | ------------------------ | ----------------------------- | ------------------------------------------------------- | ----------------------------------- |
| ก่อน Optimize                                                                   | 0.780630      | -                 | -                      | -                        | -                             | 76128                                                   | -                                   |
| Grayscale                                                                       | 0.134396      | 82.78%            | 82.78%                 | 5.80 เท่า                | 5.80 เท่า                     | 25376                                                   | 3byte/cell -> 1byte/cell            |
| Flatten + bitwise XOR                                                           | 0.067009      | 50.15%            | 91.42%                 | 2.00 เท่า                | 11.64 เท่า                    | 25376                                                   | (64, 800)->(51200, )                |
| sum(C == 1) -> sum(C)                                                           | 0.050145      | 25.16%            | 93.57%                 | 1.33 เท่า                | 15.56 เท่า                    | 25376                                                   |                                     |
| packbits                                                                        | 0.034713      | 30.71%            | 95.55%                 |                          |                               | 25376                                                   | pack 8 byte to 1 byte (byte to bit) |
| bit count lookup                                                                | 0.025945      | 25.26%            | 96.68%                 |                          |                               | 25376                                                   | unpack for sum -> bit count for sum |
| multiprocessing (worker-client solution)                                        | 0.023487      | 9.47%             | 96.99%                 |                          |                               | 25376                                                   |                                     |
| no send duplicate templates *เทียบกับก่อนทำ multiprocessing (bit count lookup)* | 0.016397      | 36.80%            | 97.899%                |                          |                               | 25376                                                   |                                     |

>[!note]
>ผลเป็นหน่วย milliseconds / compare
>โดยการนำเวลาที่ใช้ท้งหมดหารด้วยจำนวน template ที่นำมาเปรียบเทียบ

$(\frac{เวลาในหน่วยวินาที}{จำนวน template หลัง duplicate})\times 1000 = milliseconds/compare$
