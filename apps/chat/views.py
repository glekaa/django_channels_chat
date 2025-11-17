from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from .models import Group


@login_required
def home_view(request):
    groups = Group.objects.all()
    user = request.user
    context = {"groups": groups, "user": user}
    return render(request, template_name="chat/home.html", context=context)


def group_chat_view(request, uuid):
    group = get_object_or_404(Group, uuid=uuid)
    if not group.members.filter(id=request.user.id).exists():
        return HttpResponseForbidden(
            "You are not the member of this group. Kindly use the join button"
        )

    messages = group.messages.all()
    events = group.events.all()

    message_and_event_list = [*messages, *events]
    sorted_message_event_list = sorted(
        message_and_event_list, key=lambda x: x.timestamp
    )

    group_members = group.members.all()

    context = {
        "message_and_event_list": sorted_message_event_list,
        "group_members": group_members,
    }

    return render(request, template_name="chat/groupchat.html", context=context)
