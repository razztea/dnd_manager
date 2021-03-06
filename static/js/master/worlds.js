// Class to represent each character
dnd.structs.World = function(id, name, master_name, description) {
    var self = this;
    self.id = id;
    self.name = name;
    self.master_name = master_name;
    self.description = description;
}

// Overall viewmodel for this screen
dnd.vms.WorldsVM = function() {
    var self = this;

    self.username = Get.username;
    self.worldList = ko.observableArray([]);
    self.goToWorld = function(world) {
        window.location.href = "/master/edit_world?world="+world.id+"&username="+self.username;
    };
    self.newWorld = function() {
        window.location.href = "/master/edit_world?world=new&username="+self.username;
    };

    $.post('/gateway?file=master&method=retrieve_world_list', ko.toJSON(this), function(data) {
        if (data.success === "true") {
            $.each(data.worlds, function(idx, world) {
                self.worldList.push(new dnd.structs.World(world.id, world.name, world.username, world.description));
            });
        }
        else {
            alert(data.message);
        }
    });
}

dnd.instances.worlds = new dnd.vms.WorldsVM();

ko.applyBindings(dnd.instances.worlds);
