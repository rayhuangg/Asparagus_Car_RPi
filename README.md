## 檔案說明

```
i2c_responder.py                 // ADAM留下，應該是用來測試UART功能
keyboard_remote_control.py       // 用鍵盤從rpi直接遙控前進、左右轉 (目前無拍照功能)
rpi4motor_left.py                // left rpi主程式
asparagus_car.py                 // AsparagusCar class，用來做import
imageUpload.py                   // 通用的上傳蘆筍網站程式(含前視影像與pi camera上傳)
keyboard_upload.py               // 用鍵盤遙控拍攝取相
rpi4motor_right.py               // right rpi主程式
```


# 使用方法
## Rpi1_left
Fullname: raspberrypi-1dinci

用途: 連接兩邊馬達驅動器，接收從AGX下達的馬達控制指令，並負責左邊pi camera拍照上傳

### 連接agx進行巡園拍照上傳
```bash
# 接收馬達控制訊號，，並傳送拍照訊號給右邊
python3 rpi4motor_left.py
```

### 單純鍵盤遙控車輛
```bash
python3 keyboard_remote_control.py
```

### 鍵盤遙控拍照上傳
```bash
python3 keyboard_upload.py
```


## Rpi2_right
Fullname: raspberrypi-2dinci

用途: 僅負責右邊pi camera拍照上傳

### 連接agx進行巡園拍照上傳
```bash
# 僅接收左邊rpi傳送拍照訊號
python3 rpi4motor_right.py
```

### 鍵盤遙控拍照上傳
```bash
python3 keyboard_upload.py
```