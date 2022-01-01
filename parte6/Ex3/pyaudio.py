#!/usr/bin/env python
import cv2
import pyaudio
import wave


def main():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 0.5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    while True:
    #frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            #frames.append(data)

        #print("* done recording")
        #print(data)

        rms = audioloop.rms(data, 2) # width=2 for format=paInt16
        print(rms)

        if rms > 1000:
            print('something is making noise.')
        else:
            print('Its so quite around here ...')
    stream.stop_stream()
    stream.close()
    p.terminate()

    #wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #wf.setnchannels(CHANNELS)
    #wf.setsampwidth(p.get_sample_size(FORMAT))
    #wf.setframerate(RATE)
    #wf.writeframes(b''.join(frames))
    #wf.close()

if __name__ == '__main__':
    main()