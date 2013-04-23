dndObjects.Stat = function(name, min, max) {
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
dndViewModels.CharacterGenerationVM = function() {
    var self = this;
    // These will come from the server later
    self.availableClasses = [];
    self.availableRaces = [];

    self.username = Get.username;
    self.char_name = ko.observable("");
    self.char_class = ko.observable("");
    self.char_race = ko.observable("");

    self.stats = ko.observableArray([]);

    self.generateStats = function() {
        for(var i = 0; i < this.stats().length; i++) {
            var oldStat = this.stats().splice(0, 1)[0];
            this.stats.push(new dndObjects.Stat(oldStat.name, oldStat.min, oldStat.max));
        }
    };
}

ko.applyBindings(new dndViewModels.CharacterGenerationVM());
