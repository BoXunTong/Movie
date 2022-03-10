function add_to_watchlist_function(movie_id){
    
    var endpoint = $("#add_to_watchlist").attr("data-url");
    $.ajax({
        type: "get",
        url: endpoint,
        data: {
            movie_id:movie_id
        },
        success: function (){
            location.reload(true);
        },
        error: function(){}
    });
    return false;
}

function remove_from_watchlist_function(movie_id){
    
    var endpoint = $("#remove_from_watchlist").attr("data-url");
    $.ajax({
        type: "get",
        url: endpoint,
        data: {
            movie_id:movie_id
        },
        success: function (){
            location.reload(true);
        },
        error: function(){}
    });
    return false;
}