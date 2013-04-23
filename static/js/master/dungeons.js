// Class to represent each character
dndObjects.Dungeon = function(id, name, master_name, details) {
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
dndViewModels.DungeonsVM = function() {
    var self = this;

    self.username = Get.username;
    self.dungeons = ko.observableArray([]);
    self.goToDungeon = function(dungeon) {
        window.location.href = "/player/character_generation?dungeon="+dungeon.id+"&username="+self.username;
    }
}

ko.applyBindings(new dndViewModels.DungeonsVM());
