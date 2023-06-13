
$(function () {
    function MagneticFieldScannerViewModel(parameters) {
        this.allSettings = parameters[0]


        this.loginState = parameters[1];
        this.printerState = parameters[2];
        this.confirmation = undefined;
        this.connected = ko.observable(false)
        this.points = ko.observable(0)

        this.onAfterBinding = function () { };
        this.onBeforeBinding = function () {
            this.confirmation = $("#confirmation");
            this.settings = this.allSettings.settings

            // plot();
        };

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
            // this.confirmation.modal("hide");

        };

        this.sendGetCommand = function (command) {
            $.ajax({
                url: API_BASEURL + "plugin/magneticfieldscanner",
                type: "GET",
                dataType: "json",
                data: JSON.stringify({
                    command: command
                }),
                contentType: "application/json; charset=UTF-8",
                success: function (data, status) { refreshPlot(data) }
            });
            // this.confirmation.modal("hide");

        };

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
