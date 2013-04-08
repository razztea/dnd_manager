function Stat(name, min, max) {
    var self = this;
    self.name = name;
    self.value = ko.observable(Math.floor((Math.random()*(max-min)+min)));
    self.min = min;
    self.max = max;

    self.perc_str = ko.computed(function() {
        return String(self.value()/self.max*100) + "%";
    });
}

// Overall viewmodel for the character generation screen
function CharacterGenerationViewModel() {
    // These will come from the server later
    this.availableClasses = ['Warrior', 'Thief', 'Mage', 'Monk', 'Ranger'];
    this.availableRaces = ['Human', 'Elf', 'Dwarf'];

    this.char_name = ko.observable("");
    this.char_class = ko.observable("Warrior");
    this.char_race = ko.observable("Human");

    this.stats = ko.observableArray([
        new Stat("Strength", 3, 18),
        new Stat("Wisdom", 3, 18)]
    );

    this.generateStats = function() {
        for(var i = 0; i < this.stats().length; i++) {
            var oldStat = this.stats().splice(0, 1)[0];
            this.stats.push(new Stat(oldStat.name, oldStat.min, oldStat.max));
        }
    };
}

ko.applyBindings(new CharacterGenerationViewModel());
