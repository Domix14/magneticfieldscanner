
$(function () {
    function MagneticFieldScannerViewModel(parameters) {
        this.allSettings = parameters[0]


        this.loginState = parameters[1];
        this.printerState = parameters[2];
        this.confirmation = undefined;
        this.connected = ko.observable(false)
        this.points = ko.observable(0)
        this.data = []

        this.onAfterBinding = function () { };
        this.onBeforeBinding = function () {
            this.confirmation = $("#confirmation");
            this.settings = this.allSettings.settings

            this.connected(this.settings.plugins.magneticfieldscanner.connected())
            this.points(this.settings.plugins.magneticfieldscanner.points_count())

            // this.updateChart();
        };

        this.deleteData = function () {
            this.sendCommand('delete_data')
            this.data = []
            this.points(0)
            refreshPlot(this.data);
        }

        this.exportData = function () {
            // this is stupid but works
            window.location = API_BASEURL + "/plugin/magneticfieldscanner/export_data"
        }

        this.sendCommand = function (command) {
            $.ajax({
                url: API_BASEURL + "plugin/magneticfieldscanner",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: command
                }),
                contentType: "application/json; charset=UTF-8",
                success: function (data, status) { }
            });
        };

        this.updateChart = function () {
            $.ajax({
                url: API_BASEURL + "/plugin/magneticfieldscanner",
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                success: (data, status) => {
                    this.data = data
                    refreshPlot(this.data)
                }
            });
        }

        this.onDataUpdaterPluginMessage = function (plugin, data) {
            if (data.type == "connection_update") {
                this.connected(data.value)
            }
            else if (data.type == "points_update") {
                this.points(data.value)
            }
        };
    };

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        MagneticFieldScannerViewModel,

        ["settingsViewModel", "loginStateViewModel", "printerStateViewModel"],

        ["#navbar_plugin_magneticfieldscanner", "#tab_plugin_magneticfieldscanner"]
    ]);
});
