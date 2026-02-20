from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q, Count, F
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def user_list(request):
    """List of users with unread message counts."""
    users = User.objects.exclude(id=request.user.id).annotate(
        unread_count=Count(
            'received_messages', 
            filter=Q(
                received_messages__sender=F('id'), 
                received_messages__receiver=request.user, 
                received_messages__is_read=False
            )
        )
    ).order_by('username')
    
    return render(request, "user_list.html", {"users": users})

@login_required
def chat_view(request, username):
    """Chat room with read-status update logic."""
    other_user = get_object_or_404(User, username=username)

    Message.objects.filter(
        sender=other_user, 
        receiver=request.user, 
        is_read=False
    ).update(is_read=True)

    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'other': other_user,
        'chat_messages': chat_messages
    })

def logout_view(request):
    """Logs out user and redirects to login."""
    logout(request)
    return redirect('login')

