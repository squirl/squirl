var isUserEvent = document.getElementById('id_isUserEvent');
$("#addInterest").on("click", function(event){
    event.preventDefault();
    interests = $("#interests input[type=text]");
    var interestList =$("#interests");
    $("#interests input:last")
   $("<input id='id_interests-"+ interests.length+ "-interest' maxlength='150' name='interests-"+ interests.length+ "-interest' type='text'>").insertBefore(this);
    $("#id_interests-TOTAL_FORMS").val(interests.length +1);
});
$("#formSubmit").on('submit', function(e) {
    e.preventDefault();
    if(!validateFields()){
        e.preventDefault();
    }
});

function viewGroup() {
    var groupSelect = document.getElementById('groupSelection');

    if (isUserEvent.checked == 1) {

        groupSelect.style.display = 'none';
    } else {
        groupSelect.style.display = '';

    }


}


function validateFields() {
    var valid = true;
    var regexp = /^[a-zA-Z0-9 -]+$/;
    //title error
    var title = document.getElementById('id_title');
    var titleError = document.getElementById('titleErrors');
    var messTitleError = '';

    //check for title errors
    if (title.value.length > 150 || title.value.length == 0) {
        messTitleError += "Title must be between 0 and 150 characters";
        valid = false;
    }
    if (title.value.search(regexp) == -1) {
        messTitleError += " Only alphanumeric characters and '-' are allowed.";
    }

    //startTime
    var startTime = document.getElementById('id_startTime_0');
    var startTimeError = document.getElementById('startTimeErrors');

    var messStartError = '';

    var date1 = Date.parse(startTime.value);
    var d1Valid = !isNaN(date1.valueOf());
    if (startTime.length == 0 || !d1Valid) {
        messStartError += "Invalid Start Time!";
        valid = false;
    }

    //endtime
    var endTimeError = document.getElementById('endTimeErrors');
    var endTime = document.getElementById('id_endTime_0');

    var messEndError = '';

    var date2 = Date.parse(endTime.value);
    var d2Valid = !isNaN(date2.valueOf());
    if (endTime.length == 0 || !d2Valid) {
        messEndError += "Invalid end time!";
        valid = false;
    }

    //check if time 1 is before time 2
    if (d1Valid && d2Valid && date1 > date2) {
        messStartError += 'The start date must be before the end date';
    }


    //description
    var description = document.getElementById('id_description');
    var descriptionError = document.getElementById('descriptionErrors');

    var messDescription = '';

    if (description.value.length == 0 || description.value.length > 1000) {
        messDescription += "Description must be more than 0 characters and no more than 1000";
        valid = false;
    }


    //location


    //group/user event

    var userEvent = document.getElementById('id_isUserEvent');
    var group = document.getElementById('id_group');
    var userError = document.getElementById('eventTypeErrors');
    var groupErrors = document.getElementById('groupErrors');


    var messGroup = '';
    var messUser = '';

    if (!userEvent.checked) {
        if (group[0].value == group.options[group.selectedIndex].value) {
            messGroup += "Select a group or check user event!";
            messUser += "Select a group or check user event!";
            valid = false;
        }
    }


    //
    //display errors
    //

    titleError.innerHTML = messTitleError;

    startTimeError.innerHTML = messStartError;

    endTimeError.innerHTML = messEndError;

    descriptionError.innerHTML = messDescription;

    

    groupErrors.innerHTML = messGroup;

    userError.innerHTML = messUser;
    return valid;

}

function formSubmit(event) {
    if (!validateFields()) {
        event.preventDefault();
        var titleError = document.getElementById('titleErrors');
    } else {

    }
}

var elForm = document.getElementById("eventForm");
elForm.addEventListener('submit', formSubmit, false);