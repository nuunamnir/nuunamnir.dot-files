import libqtile.widget.base


class Bluetooth(libqtile.widget.base.ThreadPoolText):
    def __init__(self, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)

    def poll(self):
        label = "nuunamnir.widgets.bluetooth.Bluetooth"
        return label


if __name__ == "__main__":
    pass
