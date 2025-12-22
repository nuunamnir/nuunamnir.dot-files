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
    def __init__(self, r, num_bars=16, warning_color="#ff0000", **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, **config)
        self.r = r

        self.warning_color = warning_color

        self.NUM_BARS = num_bars
        self.stream = sounddevice.InputStream(channels=2, samplerate=44100, callback=self.callback_spectrum)
        self.stream.start()
        self.visualization = ' ' * self.NUM_BARS
        self.past_values = numpy.zeros(self.NUM_BARS, dtype=float)

    def compress_array(self, arr, m):
        n = len(arr)
        if m > n:
            raise ValueError("m must be less than or equal to n")
        # Calculate the size of each bin
        bins = numpy.linspace(0, n, m+1, dtype=int)
        compressed = numpy.array([arr[bins[i]:bins[i+1]].sum() for i in range(m)])
        return compressed

    def callback_spectrum(self, in_data, frame_count, time_info, status):
        fft_data = numpy.abs(numpy.fft.fft(in_data - numpy.mean(in_data, axis=0), axis=0))
        spectrum = fft_data[:len(fft_data)//8, :]
        spectrum_left = spectrum[:, 0]
        spectrum_right = spectrum[:, 1]
        try:
            compressed_spectrum_left = self.compress_array(spectrum_left, self.NUM_BARS // 2)
            compressed_spectrum_right = self.compress_array(spectrum_right, self.NUM_BARS // 2)
            compressed_spectrum = numpy.concatenate((compressed_spectrum_left[::-1], compressed_spectrum_right))
            compressed_spectrum /= numpy.max([numpy.max(compressed_spectrum), 6])
            compressed_spectrum = 0.8 * self.past_values + 0.2 * compressed_spectrum
            self.past_values = compressed_spectrum
            discretized_spectrum = numpy.round(compressed_spectrum * 8).astype(int)
            unicode_blocks = [chr(0x2581 + h) if h > 0 else ' ' for h in discretized_spectrum]
            self.visualization = ''.join(unicode_blocks)
        except ValueError as e:
            pass

    def poll(self):
        if self.r is None:
            return ""
        data = self.r.xrevrange("audio", count=1)
        try:
            eid, payload = data[-1]
        except IndexError:
            return ""
        measurement = json.loads(payload.get(b"measurement").decode("utf-8"))


        output = f"<span letter_spacing='1024'>|{self.visualization}|</span>"

        if measurement["muted"] or measurement.get("volume", 0) <= 1:
            output = f"<span color='{self.warning_color}'>{output}</span>"
        alpha = numpy.clip(int(round(measurement.get("volume", 0) / 100 * 65536)), 6554, 65535)
        return f"<span fgalpha='{alpha}'>{output}</span>"
    
    
    def __del__(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
