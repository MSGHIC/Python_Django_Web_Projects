from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm, DeleteForm

# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

#ONLY logged in users can access data called by functions below
@login_required
def topics(request):
    """Show all topics."""
    #retrieve only the Topic objects from the database whose owner
    #attribute matches the current user
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
    
@login_required
def new_topic(request):
   """Add a new topic."""
   if request.method != 'POST':
       # No data submitted; create a blank form.
       form = TopicForm()
   else:
       # POST data submitted; process data.
       form = TopicForm(request.POST)
       if form.is_valid():
           new_topic = form.save(commit=False)
           new_topic.owner = request.user
           new_topic.save()
           #redirects  browser to the topics page.
           return HttpResponseRedirect(reverse('learning_logs:topics'))
   #send the form to the template in the context dictionary
   context = {'form': form}
   return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add new_entry to a given topic"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
       # No data submitted; create a blank form.
       form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # commit=False ;create a new entry object and store 
            #it in new_entry without saving
            #it to the database yet
            new_entry = form.save(commit=False)
            #saves the entry to the database with 
            #the correct associated topic.
            new_entry.topic = topic
            # Make sure the topic belongs to the current user.
            check_topic_owner(request, topic)
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    # Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)
        
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def edit_topic(request, topic_id):
    """Edit an existing topic."""
    topic = Topic.objects.get(id=topic_id)    
    # Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)
        
    if request.method != 'POST':
        # Initial request; pre-fill form with the current topic.
        form = TopicForm(instance=topic)
    else:
        # POST data submitted; process data.
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

@login_required
def delete_topic(request, topic_id):
  
   topic = Topic.objects.get(id=topic_id)
   
   if request.method != 'POST':
       form = DeleteForm()
   else:
       form = DeleteForm(data=request.POST)
       if form.is_valid():
            
           if request.POST['text']== topic.text:
               #delete topic
               Topic.objects.get(id=topic_id).delete()
               #display updated topics list
               return HttpResponseRedirect(reverse('learning_logs:topics',
                                                ))
           else:
               return HttpResponseRedirect(reverse('learning_logs:delete_topic',
                                                args=[topic.id]))

   context = {'topic': topic, 'form': form}
   return render(request, 'learning_logs/delete_topic.html', context)   
   
@login_required
def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
   
    if request.method != 'POST':
       
       form = DeleteForm()
    else:
       form = DeleteForm(data=request.POST)
       if form.is_valid():
            
           if request.POST['text'].lower()== "yes":
               #delete entry
               Entry.objects.get(id=entry_id).delete()
               #display updated topic entries list
               return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
           else:
               return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/delete_entry.html', context)   
   
  