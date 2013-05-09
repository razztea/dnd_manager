// viewmodel for any screen that has the Sign In form
dnd.vms.SignInVM = function() {
    this.username = ko.observable("").extend({required: true});
    this.password = ko.observable("").extend({required: true});

    this.signIn = function() {
        if (this.isValid()) {
            $.post('/gateway?file=global&method=sign_in', ko.toJSON(this), function(data) {
                if (data.success === "true") {
                    if (data.account_type === "master") {
                        window.location.href = "/master/worlds?username=" + data.username;
                    }
                    else {
                        window.location.href = "/player/worlds?username=" + data.username;
                    }
                }
                else {
                    alert(data.message);
                }
            });
        }
        else {
            alert("Please provide a username and password to sign in.");
        }
    };
};

dnd.instances.signIn = ko.validatedObservable(new dnd.vms.SignInVM())();

ko.applyBindings(dnd.instances.signIn, $('#signIn')[0]);
