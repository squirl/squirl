$('a.eventLink').on('click', function(e){
    e.preventDefault();
    $('#eventTemp').html('test');
    $.ajaxSetup({cache: false});
    $.get('/QED/', function(data){
        $('#eventTemp').html(data);
    });
});
function getEvent(eventId){
    var sendData = 'event=' + eventId;
    $.ajaxSetup({cache: false});
    $.get('/QED/', sendData, function(data){
        $('#eventTemp').html(data);
    });
    
    
    
    //var xhr = new XMLHttpRequest();

    
    //xhr.onload = function(){
      //  if(xhr.status === 200){
        //    document.getElementById('eventTemp').innerHTML = xhr.responseText;
        //}
        
        //document.getElementById('eventTemp').innerHTML =xhr.responseText;
    //};
    //xhr.open('GET', '/QED/', true);
    //xhr.send(null);
    //document.getElementById('eventTemp').innerHTML = "Script working";
}