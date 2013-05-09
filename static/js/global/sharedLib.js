// A shared library with common functions and utilities
// as well as some boilerplate behind-the-scenes stuff

// Global namespace for all dnd View Models
dnd = {
    vms: {},
    instances: {},
    structs: {}
};

ko.validation.init({
   decorateElement: true,
   insertMessages: false,
});

//Ajax hotwire to send appropriate JSON headers.
$.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader('X-Request', 'JSON');
    }
});

