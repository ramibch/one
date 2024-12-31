from django.shortcuts import render


def change_client_theme(request):
    request.client.dark_theme = not request.client.dark_theme
    request.client.save()
    return render(request, "snippets/change_theme.html", {"request": request})
