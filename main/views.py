from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import *
from main.models import Ticket, Status
from django.views.generic import DetailView, ListView
from .models import Ticket, Status


def index(request):
    closed_status = Status.objects.filter(title='Решена').first()
    closed_tickets_count = Ticket.objects.filter(status=closed_status).count() if closed_status else 0
    problems = Ticket.objects.filter(status=closed_status).order_by('-created_at')[:4]
    context = {
        'closed_tickets_count': closed_tickets_count,
        'problems': problems,
    }
    return render(request, 'main/index.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def ticket_view(request):
    tickets = Ticket.objects.all()
    statuses = Status.objects.all()
    return render(request, 'main/tickets.html', {'tickets': tickets, 'statuses': statuses})


def add_ticket(request):
    closed_status = Status.objects.filter(title='Решена').first()
    closed_tickets_count = Ticket.objects.filter(status=closed_status).count() if closed_status else 0
    problems = Ticket.objects.filter(status=closed_status).order_by('-created_at')[:4]

    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES)
        form.instance.creator = request.user
        form.instance.status = Status.objects.get(title="Новая")
        if form.is_valid():
            form.save()
            return redirect('tickets')
        else:
            raise Http404
    else:
        form = NewTicketForm()

    context = {
        'form': form,
        'closed_tickets_count': closed_tickets_count,
        'problems': problems,
    }
    return render(request, 'main/add-ticket.html', context)

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        new_status_title = request.POST.get('status')
        new_status = Status.objects.get(title=new_status_title)
        ticket.status = new_status
        ticket.save()
        return redirect('tickets')
    return redirect('tickets')
