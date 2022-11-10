from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from MAuthentication.models import User
# Create your views here.
from .models import Thread


@login_required
def messages_page(request):
    user_obj = User.objects.filter(username=request.user.username).first()
    threads = Thread.objects.filter(first_person=user_obj).prefetch_related('chatmessage_thread').order_by('timestamp')
    print(threads)
    context = {
        'Threads': threads
    }
    return render(request, 'chat.html', context)


# @login_required
# def messages_page(request):
#     threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
#     print(threads)
#     context = {
#         'Threads': threads
#     }
#     return render(request, 'messages.html', context)
