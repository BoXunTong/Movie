function add_to_watchlist_function(){
    
    var endpoint = $("#add_to_watchlist").attr("data-url");
    $.ajax({
        type: "get",
        url: endpoint,
        data: {},
        success: function (){
            location.reload(true);
        },
        error: function(){}
    });
    return false;
}

function remove_from_watchlist_function(){
    
    var endpoint = $("#remove_from_watchlist").attr("data-url");
    $.ajax({
        type: "get",
        url: endpoint,
        data: {},
        success: function (){
            location.reload(true);
        },
        error: function(){}
    });
    return false;
}