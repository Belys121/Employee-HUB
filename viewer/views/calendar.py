import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from viewer.models import Event


@login_required
def calendar_view(request):
    """
    Renders calendar.
    """
    return render(request, 'other/calendar.html')


@login_required
def events_feed(request):
    """
    Returns a JSON response with all events formatted for calendar display.
    """
    events = Event.objects.all()
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'extendedProps': {
                'group': event.group.name if event.group else 'No Group'
            }
        } for event in events
    ]
    return JsonResponse(events_data, safe=False)


@login_required
@csrf_exempt
def create_event(request):
    """
    Creates a new event based on the POSTed JSON data and returns success or error.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        group_name = data.get('group')

        group = Group.objects.filter(name=group_name).first()
        if group:
            event = Event.objects.create(
                title=title,
                start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M'),
                end_time=datetime.strptime(end_time, '%Y-%m-%dT%H:%M'),
                group=group
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Group not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def get_groups(request):
    """
    Returns a JSON response with all available groups including their names.
    """
    groups = Group.objects.all()
    groups_data = [{'name': group.name} for group in groups]
    return JsonResponse(groups_data, safe=False)


@login_required
@csrf_exempt
def update_event(request, event_id):
    """
    Updates the details of an existing event based on the PUT request data and returns a success or error response.
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            event = Event.objects.get(pk=event_id)
            event.title = data.get('title', event.title)
            event.start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
            event.end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
            group_name = data.get('group')
            if group_name:
                group = Group.objects.filter(name=group_name).first()
                if group:
                    event.group = group
            event.save()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def delete_event(request, event_id):
    """
    Removes the event, if any, based on its event_id and returns a success or error response.
    """
    if request.method == 'DELETE':
        try:
            event = Event.objects.get(pk=event_id)
            event.delete()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
