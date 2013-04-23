// Overall viewmodel for the user registration screen
dnd.vms.UserRegistrationVM = function() {
    var self = this;
    this.username = ko.observable("").extend({required: true});
    this.password = ko.observable("").extend({required: true});
    this.password_check = ko.observable("").extend({required: true, equal: self.password});
    this.account_type = ko.observable("player").extend({required: true});

    this.register = function() {
        if (this.isValid()) {
            $.post('/gateway?file=global&method=register', ko.toJSON(this), function(data) {
                if (data.success === "true") {
                    alert('Registration Successful');

                    if (self.account_type() === "master") {
                        window.location.href = "/master/dungeons?username=" + self.username();
                    }
                    else {
                        window.location.href = "/player/dungeons?username=" + self.username();
                    }
                }
                else {
                    alert(data.message);
                }
            });
        }
    };
};

dnd.instances.registration = ko.validatedObservable(new dnd.vms.UserRegistrationVM())();
ko.applyBindings(dnd.instances.registration, $('#registration_info')[0]);
