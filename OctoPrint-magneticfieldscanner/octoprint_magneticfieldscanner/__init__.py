# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import octoprint.plugin
import threading
from .plot_chart import Plot_3D
from .scanner import Scanner


class MagneticFieldScannerPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.EventHandlerPlugin,
):
    def __init__(self):
        self.scanner = None
        self.position_x = None
        self.position_y = None
        self.position_z = None
        self.data = []
        self.counter = 0

    def on_after_startup(self):
        self.scanner = Scanner()

    def get_settings_defaults(self):
        return {"scanner_freq": 123, "scanner_window": 13, "scanner_ip": "192.168.0.254"}

    def get_template_configs(self):
        return [{"type": "settings", "custom_bindings": False}]

    def get_api_commands(self):
        return dict(show_chart=[], connect=[])

    def on_api_command(self, command, data):
        if command == "connect":
            self.connect_scanner()
        elif command == "show_chart":
            thread = threading.Thread(target=Plot_3D().start(self.data))
            thread.start()
        elif command == "delete_data":
            self.data = []
            self._ping("points_update", len(self.data))
        elif command == "export_data":
            pass

    def get_assets(self):
        return dict(
            js=["js/magneticfieldscanner.js"],
            css=["css/magneticfieldscanner.css", "css/fontawesome.all.min.css"],
        )

    def connect_scanner(self):
        ip = self._settings.get(["scanner_ip"])
        freq = self._settings.get_float(["scanner_freq"])
        window = self._settings.get_float(["scanner_window"])
        result = self.scanner.connect(ip, freq, window)
        self._ping("connection_update", result)

    def get_update_information(self):
        return dict(
            magneticfieldscanner=dict(
                displayName="Magnetic Field Scanner",
                displayVersion=self._plugin_version,
                current=self._plugin_version,
            )
        )

    def hook(
        self,
        comm_instance,
        phase,
        cmd,
        cmd_type,
        gcode,
        subcode=None,
        tags=None,
        *args,
        **kwargs,
    ):
        if not self.scanner.connected:
            self._ping("connection_update", False)
            return [return_cmd]

        return_cmd = cmd
        if (
            self.position_x is not None
            and self.position_y is not None
            and self.position_z is not None
        ):
            freq, value = self.scanner.measure()
            self.data.append(
                {
                    "x": self.position_x,
                    "y": self.position_y,
                    "Z": self.position_z,
                    "freq": freq,
                    "value": value,
                }
            )
            self._ping("points_update", len(self.data))

        if gcode == "G0" or gcode == "G1" or gcode == "G2":
            for word in cmd.split():
                if word.startswith("X"):
                    self.position_x = float(word[1:])
                elif word.startswith("Y"):
                    self.position_y = float(word[1:])
                elif word.startswith("Z"):
                    self.position_z = float(word[1:])

    def _ping(self, command, value):
        self._plugin_manager.send_plugin_message(
            self._identifier, dict(type=command, value=value)
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Magnetic Field Scanner"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MagneticFieldScannerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.hook,
    }
