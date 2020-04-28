from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    return render(request, "learning_logs/index.html")


def topics(request):
    """ the home page for learning log"""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")

    print(entries)
    context = {"topic": topic, "entries": entries}

    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs: topics")
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            # When we call save(), we include the argument commit=False to tell Django to create
            # a new entry object and assign it to new_entry without saving it to the database yet.
            new_entry = form.save(commit=False)
            # assign the topic of the new entry based on the topic we pulled from topic_id
            new_entry.topic = topic
            new_entry.save()
            form.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "learning_logs/new_entry.html", context)
