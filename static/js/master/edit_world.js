dnd.structs.Race = function(name, description, class_limit, special, classes, attributes, id) {
    var self = this;
    self.id = id ? id : "";
    self.name = ko.observable(name);
    self.description = ko.observable(description);
    self.class_limit = ko.observable(class_limit);
    self.special = ko.observable(special);

    self.class_requirements = ko.observableArray($.map(classes(), function(cls) { return new dnd.structs.ClassRequirement(cls)}));
    self.view_cr = ko.observable(false);
    self.attribute_requirements = ko.observableArray($.map(attributes(), function(attribute) { return new dnd.structs.AttributeRequirement(attribute)}));
    self.view_ar = ko.observable(false);

    classes.subscribe(function(classList) {
        if (classList.length > self.class_requirements().length) {
            self.class_requirements.push(new dnd.structs.ClassRequirement(classList[classList.length-1]));
        }
        else if (classList.length < self.class_requirements().length) {
            for(var j=0; j<self.class_requirements().length; j++) {
                for(var i=0; i<classList.length; i++) {
                    var match = false;
                    var class_req = self.class_requirements()[j];
                    if (classList[i].name() === class_req.cls_name) {
                        match = true;
                    }
                    if (!match) {
                        if (class_req.id != "") {
                            self.class_requirements.destroy(class_req);
                        }
                        else {
                            self.class_requirements.remove(class_req);
                        }
                        return;
                    }
                };
            };
        }
    });
    attributes.subscribe(function(attributeList) {
        if (attributeList.length > self.attribute_requirements().length) {
            self.attribute_requirements.push(new dnd.structs.AttributeRequirement(attributeList[attributeList.length-1]));
        }
        else if (attributeList.length < self.attribute_requirements().length) {
            for(var j=0; j<self.attribute_requirements().length; j++) {
                for(var i=0; i<attributeList.length; i++) {
                    var match = false;
                    var attr_req = self.attribute_requirements()[j];
                    if (attributeList[i].name() === attr_req.attr_name) {
                        match = true;
                    }
                    if (!match) {
                        if (attr_req.id != "") {
                            self.attribute_requirements.destroy(attr_req);
                        }
                        else {
                            self.attribute_requirements.remove(attr_req);
                        }
                        return;
                    }
                };
            };
        }
    });
}

dnd.structs.Class = function(name, description, special, min_hp, max_hp, attributes, alignments, id) {
    var self = this;
    self.id = id ? id : "";
    self.name = ko.observable(name);
    self.description = ko.observable(description);
    self.special = ko.observable(special);
    self.min_hp = ko.observable(min_hp);
    self.max_hp = ko.observable(max_hp);

    self.attribute_requirements = ko.observableArray($.map(attributes(), function(attribute) { return new dnd.structs.AttributeRequirement(attribute)}));
    self.view_ar = ko.observable(false);
    self.alignments = ko.observableArray($.map(alignments(), function(alignment) { return new dnd.structs.ClassAlignment(alignment)} ));
    self.view_al = ko.observable(false);

    attributes.subscribe(function(attributeList) {
        if (attributeList.length > self.attribute_requirements().length) {
            self.attribute_requirements.push(new dnd.structs.AttributeRequirement(attributeList[attributeList.length-1]));
        }
        else if (attributeList.length < self.attribute_requirements().length) {
            for(var j=0; j<self.attribute_requirements().length; j++) {
                for(var i=0; i<attributeList.length; i++) {
                    var match = false;
                    var attr_req = self.attribute_requirements()[j];
                    if (attributeList[i].name() === attr_req.attr_name) {
                        match = true;
                    }
                    if (!match) {
                        if (attr_req.id != "") {
                            self.attribute_requirements.destroy(attr_req);
                        }
                        else {
                            self.attribute_requirements.remove(attr_req);
                        }
                        return;
                    }
                };
            };
        }
    });
    alignments.subscribe(function(alignmentList) {
        if (alignmentList.length > self.alignments().length) {
            self.alignments.push(new dnd.structs.ClassAlignment(alignmentList[alignmentList.length-1]));
        }
        else if (alignmentList.length < self.alignments().length) {
            for(var j=0; j<self.alignments().length; j++) {
                for(var i=0; i<alignmentList.length; i++) {
                    var match = false;
                    var al_req = self.alignments()[j];
                    if (alignmentList[i].name() === al_req.ali_name) {
                        match = true;
                    }
                    if (!match) {
                        if (al_req.id != "") {
                            self.alignments.destroy(al_req);
                        }
                        else {
                            self.alignments.remove(al_req);
                        }
                        return;
                    }
                };
            };
        }
    });
}

dnd.structs.ClassRequirement = function(cls, id) {
    var self = this;
    self.id = id ? id : "";
    self.cls_id = cls.id;
    self.cls_name = cls.name;
    self.max_level = ko.observable(0);
    self.allowed = ko.observable(true);
}

dnd.structs.ClassAlignment = function(alignment, id) {
    var self = this;
    self.id = id ? id : "";
    self.ali_id = alignment.id;
    self.ali_name = alignment.name;
    self.allowed = ko.observable(true);
}

dnd.structs.AttributeRequirement = function(attribute, id) {
    var self = this;
    self.id = id ? id : "";
    self.attr_id = attribute.id;
    self.attr_name = attribute.name;
    self.min = ko.observable(3);
    self.max = ko.observable(18);
    self.modifier = ko.observable(0);
}

dnd.structs.Attribute = function(name, description, min, max, id) {
    var self = this;
    self.id = id ? id : "";
    self.name = ko.observable(name);
    self.description = ko.observable(description);
    self.min = ko.observable(min);
    self.max = ko.observable(max);
}

dnd.structs.Alignment = function(name, description, id) {
    var self = this;
    self.id = id ? id : "";
    self.name = ko.observable(name);
    self.description = ko.observable(description);
}

// Overall viewmodel for the character generation screen
dnd.vms.EditWorldVM = function() {
    var self = this;
    // These will come from the server later
    self.Races = ko.observableArray([]);
    self.Classes = ko.observableArray([]);
    self.Attributes = ko.observableArray([]);
    self.Alignments = ko.observableArray([]);

    self.username = Get.username;
    self.world_id = Get.world_id;
    self.world_name = ko.observable("");

    self.addRace = function() {
        self.Races.push(new dnd.structs.Race("", "", 1, "", self.Classes, self.Attributes));
    };

    self.removeRace = function(race) {
        if (race.id !== "") {
            self.Races.destroy(race);
        }
        else {
            self.Races.remove(race);
        }
    };

    self.addClass = function() {
        self.Classes.push(new dnd.structs.Class("", "", "", 1, 10, self.Attributes, self.Alignments));
    };

    self.removeClass = function(cls) {
        if (cls.id !== "") {
            self.Classes.destroy(cls);
        }
        else {
            self.Classes.remove(cls);
        }
    };

    self.addAttribute = function() {
        self.Attributes.push(new dnd.structs.Attribute("", "", 3, 18));
    };

    self.removeAttribute = function(attr) {
        if (attr.id !== "") {
            self.Attributes.destroy(attr);
        }
        else {
            self.Attributes.remove(attr);
        }
    };

    self.addAlignment = function() {
        self.Alignments.push(new dnd.structs.Alignment("", ""));
    };

    self.removeAlignment = function(ali) {
        if (ali.id !== "") {
            self.Alignments.destroy(ali);
        }
        else {
            self.Alignments.remove(ali);
        }
    };

    self.save = function() {
        $('#save').button('loading');
        $.post('/gateway?file=master&method=save_world', ko.toJSON(this), function(data) {
            $('#save').button('reset');
            if (data.success === "true") {
                self.reset(data);
            }
            else {
                alert(data.message);
            }
        });
    };

    self.toggle = function(val) {
        if (val() == true) {
            val(false);
        }
        else {
            val(true);
        }
    };

    self.reset = function(jsonData) {
        self.Attributes.removeAll();
        self.Alignments.removeAll();
        self.Classes.removeAll();
        self.Races.removeAll();
        $.each(jsonData.attributes, function(idx, attr) {
            self.Attributes.push(new dnd.structs.Attribute(attr.name, attr.description, attr.min, attr.max, attr.id));
        });
        $.each(jsonData.alignments, function(idx, al) {
            self.Alignments.push(new dnd.structs.Alignment(al.name, al.description, al.id));
        });
        $.each(jsonData.classes, function(idx, cls) {
            self.Classes.push(new dnd.structs.Class(cls.name, cls.description, cls.special, cls.min_hp, cls.max_hp, self.Attributes, self.Alignments, cls.id));
        });
        $.each(jsonData.races, function(idx, race) {
            self.Races.push(new dnd.structs.Race(race.name, race.description, race.class_limit, race.special, self.Classes, self.Attributes, race.id));
        });
    };

    if (self.world_id != "new") {
        $.post('/gateway?file=master&method=retrieve_world_info', ko.toJSON(this), function(data) {
            if (data.success === "true") {
                self.reset(data);
            }
            else {
                alert(data.message);
            }
        });
    }
}

dnd.instances.editWorld = new dnd.vms.EditWorldVM();

if (Get.world_id != 'new') {
    // Retrieve the data from the server

}
ko.applyBindings(dnd.instances.editWorld);
