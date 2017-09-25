var BASE = window.location.origin + "/socialinsight";

function searchIntel(el, e) {
    e.preventDefault();
    search  = $("#intelSearch").val();
    $("#result").load(BASE+"/default/search?search="+encodeURIComponent(search));
}

function intelSearchInsert(d) {
    var command = d.getAttribute('data-insert');
    console.log(command);
    //$("#intelSearch").val($("#intelSearch").val() + command + " ");
    $("#intelSearch").val(command);
    $("#intelSearch").focus();
}


function saveSearchIntel() {
    var search_input = $("#intelSearch").val();
    $("#intel_search").val(search_input);
    $("#intelSearchModal").modal('show');
}

function intelSearchSavePost(e) {
    e.preventDefault();
    var intel_name = $("#intel_name").val();
    var intel_description = $("#intel_description").val();
    var intel_search = $("#intel_search").val();
    $.post({
        url:BASE+"/default/_add_search",
        data: {
            intel_name: intel_name,
            intel_description: intel_description,
            intel_search: intel_search
        }
    }).done(function() {
        loadSavedSearches();
        $("#intelSearchModal").modal('hide');
        $("#intelSearchSavePost").trigger("reset");
    });
}

function loadSavedSearches() {
    $("#intelSavedSearches").load(BASE+"/default/_searches");
}
