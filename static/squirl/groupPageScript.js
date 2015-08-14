//var script = document.createElement('script');
//script.src = 'jquery-2.1.4.js';
//script.type = 'text/javascript';
//document.getElementsByTagName('head')[0].appendChild(script);

console.debug("test");
$("#subGroupForm").on('submit', function(event) {

    event.preventDefault();
    $.ajaxSetup({
        cache: false
    });
    var sendData = $("#subGroupForm").serialize();
    $.post('/QED/subGroupRequest/', sendData, function(data) {
        if ($(".formMessage").size() === 0) {
            var message = document.createElement("div");
            message.setAttribute("class", "formMessage");
            message.textContent = data.message;
            var form = $("#subGroupForm").after(message);
        } else {
            $(".formMessage").text(data.message);
        }




    });
});