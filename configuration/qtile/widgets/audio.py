import json

import libqtile.widget.base
import libqtile.log_utils

try:
    import sounddevice
except ImportError:
    pass

import numpy
import pyaudio


class WidgetAudio(libqtile.widget.base.ThreadPoolText):
    def __init__(self, r, warning_color="#ff0000", **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, **config)
        self.r = r

        self.warning_color = warning_color

        self.NUM_BARS = 16

        self.p = pyaudio.PyAudio()
        self.info = self.p.get_default_input_device_info()
        device_index = self.info.get("index", None)
        self.stream = None
        if self.info["maxInputChannels"] > 0:
            self.RATE = int(self.info["defaultSampleRate"])
            self.stream = self.p.open(format=pyaudio.paInt16,
                input_device_index=device_index,
                channels=1,
                rate=self.RATE,
                input=True,
                output=False,
                stream_callback=self.callback)
            
            self.stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        in_data_ = numpy.frombuffer(in_data, dtype=numpy.int16)

        fft_data = numpy.abs(numpy.fft.fft(in_data_ - numpy.mean(in_data_)))
        freqs = numpy.fft.fftfreq(len(fft_data), 1/self.RATE)
        self.spectrum = fft_data[:len(fft_data)//2]
        self.freq = freqs[:len(fft_data)]
        return (in_data, pyaudio.paContinue)

    def poll(self):
        if self.r is None:
            return ""
        data = self.r.xrevrange("audio", count=1)
        try:
            eid, payload = data[-1]
        except IndexError:
            return ""
        measurement = json.loads(payload.get(b"measurement").decode("utf-8"))
        output = ""

        if self.stream is not None:
            if self.stream.is_active():
                nyquist = self.RATE // 2
                min_freq = 20  # lowest frequency of interest
                min_mel = self.hz_to_mel(min_freq)
                max_mel = self.hz_to_mel(nyquist)
                mel_edges = numpy.linspace(min_mel, max_mel, self.NUM_BARS + 1)
                bin_edges = self.mel_to_hz(mel_edges)

                bar_heights = numpy.zeros(self.NUM_BARS)
                for i in range(self.NUM_BARS):
                    start_freq = bin_edges[i]
                    end_freq = bin_edges[i + 1]
                    
                    indices = numpy.where((self.freq >= start_freq) & (self.freq < end_freq))[0]
                    if len(indices) > 0:
                        try:
                            bar_heights[i] = numpy.mean(self.spectrum[indices])
                        except IndexError:
                            bar_heights[i] = 0
                    else:
                        bar_heights[i] = 0

                max_height = numpy.max(bar_heights)
                if max_height > 0:
                    bar_heights = bar_heights / max_height
                discretized_heights = (bar_heights * 8).astype(int)
                discretized_heights = numpy.clip(discretized_heights, 1, 8)
                unicode_blocks = [chr(0x2581 + h) if h > 0 else ' ' for h in discretized_heights]
                output = f"<span letter_spacing='1024'>{''.join(unicode_blocks)}</span>"

        if measurement["muted"] or measurement.get("volume", 0) <= 1:
            output = f"<span color='{self.warning_color}'>{output}</span>"
        alpha = numpy.clip(int(round(measurement.get("volume", 0) / 100 * 65536)), 6554, 65535)
        return f"<span fgalpha='{alpha}'>{output}</span>"
    
    def hz_to_mel(self, hz):
        return 2595 * numpy.log10(1 + hz / 700)

    def mel_to_hz(self, mel):
        return 700 * (10**(mel / 2595) - 1)
    
    def __del__(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
