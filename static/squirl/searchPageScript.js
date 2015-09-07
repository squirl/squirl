$("#formSubmit").on("submit", function(event){
    event.preventDefault();
    $.ajaxSetup({
        cache: false
    });
    
    var sendData = $("searchForm").serialize();
    
    $.post('/squirl/subGroupRequest/', sendData, function(data) {
        console.debug(data.size());
    });
});