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
        self.chartGCODE = ""
        self.scanner = None
        self.position_x = None
        self.position_y = None
        self.position_z = None
        self.data = []

    def get_settings_defaults(self):
        return dict(
            chart="google.com",
            chartGCODE="M300",
            confirmationDialog=False,
            big_button=True,
        )

    def on_event(self, event, payload):
        if event == octoprint.events.Events.ALERT:
            thread = threading.Thread(target=Plot_3D().start())
            thread.start()

    def on_after_startup(self):
        self.chartGCODE = self._settings.get(["chartGCODE"])
        self.scanner = Scanner(13.56, 10)

    def get_template_vars(self):
        return dict(chart="google.com")

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False),
        ]

    def get_api_commands(self):
        return dict(emergencyStop=[])

    def on_api_command(self, command, data):
        # check if there is a : in line
        find_this = ":"
        if find_this in str(self.chartGCODE):
            # if : found then, split, then for each:
            gcode_list = str(self.chartGCODE).split(":")
            for gcode in gcode_list:
                self._printer.commands(gcode)
        else:
            self._printer.commands(self.chartGCODE)

    def get_assets(self):
        return dict(
            js=["js/chartshow.js"],
            css=["css/chartshow.css", "css/fontawesome.all.min.css"],
        )

    # Softwareupdate hook

    def get_update_information(self):
        return dict(
            simpleschoemergencystop=dict(
                displayName="Show Chart",
                displayVersion=self._plugin_version,
                current=self._plugin_version,
            )
        )

    def hook(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
        logging.warning("------------")
        return_cmd = cmd
        if self.position_x is not None and self.position_y is not None and self.position_z is not None:
            freq, value = self.scanner.measure()
            self.data.append({'x': self.position_x, 'y': self.position_y,'Z':self.position_z, 'freq': freq, 'value': value})
            logging.warning(self.data)
            return_cmd += f" ; x: {self.position_x} y: {self.position_y} Z: {self.position_z} freq: {freq} value: {value}"

        if gcode == "G0" or gcode == "G1" or gcode == "G2":
            for word in cmd.split():
                if word.startswith('X'):
                    self.position_x = float(word[1:])
                elif word.startswith('Y'):
                    self.position_y = float(word[1:])
                elif word.startswith('Z'):
                    self.position_z = float(word[1:])
        
        return [return_cmd]

        


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Chart Show"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MagneticFieldScannerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.hook,
    }
