dnd.structs.Stat = function(name, min, max) {
    var self = this;
    self.name = name;
    self.value = ko.observable(0);
    self.min = min;
    self.max = max;

    self.perc_str = ko.computed(function() {
        return String(self.value()/self.max*100) + "%";
    });

}

// Overall viewmodel for the character generation screen
dnd.vms.CharacterGenerationVM = function() {
    var self = this;

    self.username = Get.username;
    self.world_id = Get.world_id;
    // These will come from the server later
    self.availableClasses = ko.observableArray([]);
    self.availableRaces = ko.observableArray([]);
    self.attributes = ko.observableArray([]);
    self.availableAlignments = ko.observableArray([]);

    self.username = Get.username;
    self.char_name = ko.observable("");
    self.char_class = ko.observable("");
    self.char_race = ko.observable("");
    self.char_alignment = ko.observable("");

    self.generateStats = function() {
        for(var i = 0; i < this.attributes().length; i++) {
            self.randomStatValue(this.attributes()[i]);
        }
    };

    self.randomStatValue = function(attr) {
        attr.value(Math.floor((Math.random()*(attr.max-attr.min)+attr.min)));
    };

    self.save = function() {
        $('#save').button('loading');
        $.post('/gateway?file=player&method=save_character', ko.toJSON(this), function(data) {
            $('#save').button('reset');
            if (data.success === "true") {
                self.reset(data);
            }
            else {
                alert(data.message);
            }
        });
    };


    $.post('/gateway?file=player&method=retrieve_world_info', ko.toJSON(this), function(data) {
        if (data.success === "true") {
            $.each(data.attributes, function(idx, attr) {
                self.attributes.push(new dnd.structs.Stat(attr.name, attr.min, attr.max));
            });
            $.each(data.alignments, function(idx, al) {
                self.availableAlignments.push(al.name);
            });
            $.each(data.classes, function(idx, cls) {
                self.availableClasses.push(cls.name);
            });
            $.each(data.races, function(idx, race) {
                self.availableRaces.push(race.name);
            });
        }
        else {
            alert(data.message);
        }
    });
}

dnd.instances.char_gen = new dnd.vms.CharacterGenerationVM();
ko.applyBindings(dnd.instances.char_gen);
