// Class to represent each character
dnd.structs.World = function(id, name, master_name, details) {
    var self = this;
    self.id = id;
    self.name = name;
    self.master_name = master_name;
    self.details = details;

    self.viewDetails = function() {
        // do shit to view details
    };
}

// Overall viewmodel for this screen
dnd.structs.DungeonsVM = function() {
    var self = this;

    self.username = Get.username;
    self.dungeons = ko.observableArray([]);
    self.goToDungeon = function(world) {
        window.location.href = "/player/character_generation?world="+world.id+"&username="+self.username;
    };
}

ko.applyBindings(new dnd.vms.DungeonsVM());
