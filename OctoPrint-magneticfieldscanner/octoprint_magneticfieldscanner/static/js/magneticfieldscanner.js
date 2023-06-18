
$(function () {
    function MagneticFieldScannerViewModel(parameters) {
        var self = this
        self.allSettings = parameters[0]


        self.loginState = parameters[1];
        self.printerState = parameters[2];
        self.confirmation = undefined;
        self.connected = ko.observable(false)
        self.points = ko.observable(0)
        self.uploadFilename = ko.observable();
        self.data = []

        self.uploadModal = $(
            "#plugins_magneticfieldscanner_upload"
        );

        self.uploadElement = $(
            "#plugins_magneticfieldscanner_upload_text"
        );

        self.uploadButton = $(
            "#plugins_magneticfieldscanner_upload_start"
        );

        self.onAfterBinding = function () { };
        self.onBeforeBinding = function () {
            self.confirmation = $("#confirmation");
            self.settings = self.allSettings.settings

            self.connected(self.settings.plugins.magneticfieldscanner.connected())
            self.points(self.settings.plugins.magneticfieldscanner.points_count())


            // self.updateChart();
            self.uploadModal.modal("hide")
        };

        self.deleteData = function () {
            self.sendCommand('delete_data')
            self.data = []
            self.points(0)
            refreshPlot(self.data);
        }

        self.uploadElement.fileupload({
            dataType: "json",
            maxNumberOfFiles: 1,
            autoUpload: false,
            add: function (e, data) {
                if (data.files.length == 0) {
                    return false;
                }

                self.uploadFilename(data.files[0].name);

                self.uploadButton.unbind("click");
                self.uploadButton.bind("click", function () {
                    var f = data.files[0];
                    if (f) {
                        var r = new FileReader();
                        r.onload = function (e) {
                            var contents = e.target.result;
                            csv()
                                .fromString(contents)
                                .then((jsonObj) => {
                                    self.uploadData(jsonObj)
                                })
                        }
                        r.readAsText(f);

                    }
                    return false;
                });
            },
            done: function (e, data) {
                self.uploadButton.unbind("click");
                // self.uploadFilename(undefined);
                // self.fromTranslationResponse(data.result);
            },
            fail: function (e, data) {
                self.uploadButton.unbind("click");
                // self.uploadFilename(undefined);
            }
        });

        self.exportData = function () {
            // self is stupid but works
            window.location = API_BASEURL + "/plugin/magneticfieldscanner/export_data"
        }

        self.sendCommand = function (command) {
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

        self.uploadData = function (data) {
            $.ajax({
                url: API_BASEURL + "plugin/magneticfieldscanner",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "upload_data",
                    data: data
                }),
                contentType: "application/json;",
                success: function (data, status) { }
            });
        };

        self.updateChart = function () {
            $.ajax({
                url: API_BASEURL + "/plugin/magneticfieldscanner",
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                success: (data, status) => {
                    self.data = data
                    refreshPlot(self.data)
                }
            });
        }

        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (data.type == "connection_update") {
                self.connected(data.value)
            }
            else if (data.type == "points_update") {
                self.points(data.value)
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