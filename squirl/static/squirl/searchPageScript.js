$("#searchForm").on("submit", function(event){
    event.preventDefault();
    $.ajaxSetup({
        cache: false
    });
    
    var sendData = $("#searchForm").serialize();
    
    $.post('/squirl/searchSubmit/', sendData, function(data) {
        console.debug(data.message);
        $eventList = $('#eventList');
        $groupList = $("#groupList");
        $userList = $("#userList");
        $userList.html("");
        $groupList.html("");
        $eventList.html("");
        var events = [];
        $.each(data.events, function(index, element) {
            $eventList.append("<div class='event'><h3><a id='id_eventLink' href='/squirl/event/" + element.eventId +"'>" +element.eventName+ "</a></h3></div>");
        });
        
        $.each(data.groups, function(index, element) {
            $groupList.append("<div class='group'> <h3><a href='/squirl/group/" +element.groupPk+"'>"+ element.groupName +"</a></h3></div>");
        });
        
        $.each(data.users, function(index, element) {
            $userList.append("<div class='person'><h4><a href='/squirl/profile/"+ element.userId+"'>"+element.userName+ "</a></h4></div>");
        });
        

        
    });
});