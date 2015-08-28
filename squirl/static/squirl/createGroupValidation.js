var groupName = document.getElementById("id_title");
var description = document.getElementById("id_description");
var interests = $("#interests input[type=text]");


$("#addInterest").on("click", function(event){
    event.preventDefault();
    interests = $("#interests input[type=text]");
    var interestList =$("#interests");
    $("#interests input:last")
   $("<input id='id_interests-"+ interests.length+ "-interest' maxlength='150' name='interests-"+ interests.length+ "-interest' type='text'>").insertBefore(this);
    $("#id_interests-TOTAL_FORMS").val(interests.length +1);
});
                     

function validateFields() {
    var valid = true;
    var regexp = /^[a-zA-Z0-9 -]+$/;
    var groupNameErrorMessage = "";
    if (groupName.value.length > 100 || groupName.value.length <= 0) {
        valid = false;
        groupNameErrorMessage = "The group name must be more than 0 charactersbut no more than 100 characters";
    }
    if (groupName.value.search(regexp) == -1) {
        groupNameErrorMessage += " Only alphanumeric characters and '-' are allowed.";
    }

    //description validation.

    var descriptionErrorMessage = "";

    if (description.value.length <= 0) {
        valid = false;
        descriptionErrorMessage = "Description needed!";
    } else if (description.value.length > 1000) {
        valid = false;
        descriptionErrorMessage = "The description cannot be over 1000 characters";
    }



    //interests validation
    interestsErrorMessage = "";
    var found = false;
    var i =0;
    console.debug(interests.length);
    for (i = 0; i < interests.length; i++) {
        if ($(interests[i]).val().length >0) {
            found = true;
        }
    }

    if (!found) {
        interestsErrorMessage = "Please select at least one interest";
        valid = false;
    }
    //now print all of the error messages.

    var errorBox = document.getElementById("errors");
    var message = "";

    if (groupNameErrorMessage.length > 0) {
        message += groupNameErrorMessage;
    }
    if (descriptionErrorMessage.length > 0) {
        message += descriptionErrorMessage;
    }
    if (interestsErrorMessage.length > 0) {
        message += interestsErrorMessage;
    }
    errorBox.innerHTML = message;
    if (message.length > 0) {

        errorBox.style.display = "";
    } else {
        errorBox.style.display = "none";
    }
    return valid;
}