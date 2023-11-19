import subprocess

import libqtile.widget.base


class Audio(libqtile.widget.base.ThreadPoolText):
    defaults = [
        (
            "update_interval",
            0.5,
            "time between updating the state of the audio sink",
        )
    ]

    def __init__(
        self,
        **config,
    ):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Audio.defaults)

    def poll(self):
        label = "nuunamnir.widgets.audio.Audio"
        command = ['pactl', 'list', 'short', 'sinks']
        command = ['pactl', 'get-default-sink']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        default_sink = result.stdout.strip()
        command = ['pactl', 'get-sink-mute', '@DEFAULT_SINK@']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        muted = result.stdout.strip().split(': ')[-1]
        command = ['pactl', 'get-sink-volume', '@DEFAULT_SINK@']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        muted_str = ''
        if muted == 'yes':
            muted_str = ''
        return muted_str


if __name__ == "__main__":
    widget = Audio()
    print(widget.poll())
