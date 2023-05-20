
$(function () {
    function SchowchartViewModel(parameters) {
        this.settings = undefined;
        this.allSettings = parameters[0];
        this.loginState = parameters[1];
        this.printerState = parameters[2];
        this.confirmation = undefined;

        this.onAfterBinding = function () { };
        this.onBeforeBinding = function () {
            this.confirmation = $("#confirmation");
            this.settings = this.allSettings.settings.plugins.magneticfieldscanner;
        };

        this.click = function () {
            if (!this.can_send_command())
                return;
            if (this.settings.confirmationDialog())
                this.confirmation.modal("show");
            else
                this.sendCommand();

        };

        this.sendCommand = function () {
            $.ajax({
                url: API_BASEURL + "plugin/magneticfieldscanner",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "emergencyStop"
                }),
                contentType: "application/json; charset=UTF-8",
                success: function (data, status) { }
            });
            this.confirmation.modal("hide");

        };

        this.hasControlPermition = function () {
            let user = this.loginState.currentUser();
            if (user.permissions !== undefined) {
                return user.permissions.includes("control") || user.needs.role.includes("control");
            }
            else return true;

        }


        this.little_button_visible = function () {
            return this.loginState.isUser() && this.hasControlPermition();
        };

        this.can_send_command = function () {
            return this.loginState.isUser() && this.hasControlPermition() && this.printerState.isOperational();
        };

        this.little_button_css = function () {
            return (this.printerState.isOperational() ? "ses_small" : "ses_small_disabled");
        };



    };

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        SchowchartViewModel,

        ["settingsViewModel", "loginStateViewModel", "printerStateViewModel"],

        ["#navbar_plugin_magneticfieldscanner"]
    ]);
});
