// Class to represent each character
dndObjects.Character = function(name, cls, race, details) {
    var self = this;
    self.name = name;
    self.cls = cls;
    self.race = race;
    self.details = details;

    self.viewDetails = function() {
        // do shit to view details
    };
}

// Overall viewmodel for this screen
dndViewModels.CharactersVM = function() {
    var self = this;

    self.characters = ko.observableArray([
        new Character("boneCrusher", "Warrior", "Human", {}),
        new Character("ladyElf", "Mage", "Elf", {}),
        new Character("sir_hits_alot", "Brute", "Dwarf", {})
    ]);
}

ko.applyBindings(new dndViewModels.CharactersVM());
