import sounddevice as sd

# Replace '1' with the index of the device you want to use
device_info = sd.query_devices(1, 'input')
print(device_info)
