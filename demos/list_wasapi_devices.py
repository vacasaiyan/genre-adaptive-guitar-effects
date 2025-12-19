import sounddevice as sd

devices = sd.query_devices()

print("\n=== WASAPI Audient Devices ===")
for i, d in enumerate(devices):
    if 68 <= i <= 99 and 'Audient' in d['name']:
        print(f"{i}: {d['name']}")
        print(f"   Input channels: {d['max_input_channels']}")
        print(f"   Output channels: {d['max_output_channels']}")
        print()
