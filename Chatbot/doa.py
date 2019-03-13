import time
import serial
import struct
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_6p1_mic_array import DOA


def main():
    ard = serial.Serial('/dev/ttyACM0', 9600)
    src = Source(rate=16000, channels=8)
    ch1 = ChannelPicker(channels=8, pick=1)
    kws = KWS()
    doa = DOA(rate=16000)
    time.sleep(1)

    src.link(ch1)
    ch1.link(kws)
    src.link(doa)

    while True:
        def on_detected(keyword):
            direction = doa.get_direction()
            print('detected {} at direction {}'.format(keyword, ))
            if (direction >= 0) and (direction <= 180):
                ard.write(struct.pack('>B', direction))

    kws.set_callback(on_detected)

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
