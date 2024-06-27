from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError
from .models import Task
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import DatabaseError  # Import DatabaseError

from .models import Task

def addTask(request):
    try:
        task = request.POST['task']
        Task.objects.create(task=task)
    except KeyError as e:
        return HttpResponse(f"KeyError: {e}", status=400)  # Bad request if 'task' key is missing
    except DatabaseError as e:
        return HttpResponse(f"DatabaseError: {e}", status=500)  # Server error if database operation fails
    return redirect('home')


def mark_as_done(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = True 
        task.save()
        return redirect('home')
    except (Http404, ValidationError) as e:
        # Log the exception or handle it gracefully
        return HttpResponse(f"Error occurred: {e}", status=400)

def mark_as_undone(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = False 
        task.save()
        return redirect('home')
    except (Http404, ValidationError) as e:
        # Log the exception or handle it gracefully
        return HttpResponse(f"Error occurred: {e}", status=400)

def edit_task(request, pk):
    try:
        get_task = get_object_or_404(Task, pk=pk)
        if request.method == 'POST':
            new_task = request.POST['task']
            get_task.task = new_task
            get_task.save()
            return redirect('home')
        else:
            context = {
                'get_task': get_task,
            }
            return render(request, 'edit_task.html', context)
    except (Http404, ValidationError) as e:
        # Log the exception or handle it gracefully
        return HttpResponse(f"Error occurred: {e}", status=400)
    
def delete_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('home')
    except (Http404, ValidationError) as e:
        # Log the exception or handle it gracefully
        return HttpResponse(f"Error occurred: {e}", status=400)