var groupName = document.getElementById("id_title");
var description = document.getElementById("id_description");
var interests = document.querySelectorAll("#id_interests input");

function validateFields() {
    var valid = true;

    var groupNameErrorMessage = "";
    if (groupName.value.length > 100 || groupName.value.length <= 0) {
        valid = false;
        groupNameErrorMessage = "The group name must be more than 0 charactersbut no more than 100 characters";
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
    for (i = 0; i < interests.length; i++) {
        if (interests[i].checked) {
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