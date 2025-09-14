from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_member(user):
    return getattr(user, "userprofile", None) and user.userprofile.role == "member"

@user_passes_test(is_member)
def member_view(request):
    return render(request, "member_view.html")