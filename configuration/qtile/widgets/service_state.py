import subprocess

import libqtile.log_utils
import libqtile.widget.base


class WidgetServiceState(libqtile.widget.base.ThreadPoolText):
    def __init__(self, service, warning_color="#ff0000", **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, **config)
        self.service = service
        self.warning_color = warning_color

        self.tick = False

    def poll(self):
        p = subprocess.Popen(
            f"systemctl --user is-active --quiet {self.service}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate()

        output = ""
        if p.returncode == 0:
            if self.tick:
                output = "·"
            else:
                output = " "
            self.tick = not self.tick
        else:
            output = f"<span color='{self.warning_color}'>💤</span>"

        return f"{output}"
