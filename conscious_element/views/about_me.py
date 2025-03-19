from django.shortcuts import render


def about_me(request):
    return render(request, template_name="about_me.html")
