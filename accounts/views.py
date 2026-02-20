from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from chat.models import Message 

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username:
            messages.error(request, "Username is required.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return render(request, "register.html")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            user.is_online = True
            user.save()
            return redirect("user_list")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_online = False
        request.user.save()
    auth_logout(request)
    return redirect("login")

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    for user in users:
        # Count messages where this user is sender and YOU are receiver
        user.unread_count = Message.objects.filter(
            sender=user, 
            receiver=request.user, 
            is_read=False
        ).count()
    return render(request, "user_list.html", {"users": users})

@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Mark messages as read when you enter the chat
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, "chat.html", {
        "other_user": other_user,
        "chat_messages": messages_list
    })

