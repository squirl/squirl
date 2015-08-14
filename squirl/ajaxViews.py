from django.shortcuts import render
from django.http import HttpResponse
from .views import squirl_login
from .groupForms import CreateSubGroupRequestForm
from .methods import get_squirl
from .groupMethods import create_subgroup_request, validate_create_subgroup_request_form
from .models import SubGroupNotification
import json
def handle_sub_group_request(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        if request.method == 'POST':
            success = True
            print("post")
            #handle the post
            print request.POST
            form = CreateSubGroupRequestForm(request.POST)
           
            
            squirl = get_squirl(request.user.id)
            message = ""
            if form.is_valid():
                print("valid")
                data = form.cleaned_data
                success = validate_create_subgroup_request_form(data, squirl)
                print(success)
                message = create_subgroup_request(data, squirl)
                if message == "":
                    message = "no news"
            else:
                print("form not valid")
                print(form)
               
                success= False
            if request.is_ajax():
                print("ajax")
                if message is None:
                    message = "Form was not valid"
                response_data = {'message': message}
                print(response_data);
                return HttpResponse(json.dumps(response_data), content_type="application/json")
                #this is where we have a something
        else:
            
            return HttpResponse("Error. Can only post to this page.")
            
