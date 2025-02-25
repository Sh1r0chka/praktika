from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import *
from main.models import Ticket, Status
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from .forms import NewTicketForm, TicketForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


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
@login_required
def ticket_view(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(creator=request.user)

    statuses = Status.objects.all()

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketStatusForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            new_status = form.cleaned_data['status']
            if new_status.title == "Отклонена" and not form.cleaned_data['rejection_reason']:
                form.add_error('rejection_reason', 'Укажите причину отказа')
            elif new_status.title == "Решена" and not form.cleaned_data['solved_image']:
                form.add_error('solved_image', 'Загрузите фотографию решения')
            else:
                form.save()
                return redirect('tickets')
    else:
        form = TicketStatusForm()

    context = {
        'tickets': tickets,
        'statuses': statuses,
        'form': form,
    }
    return render(request, 'main/tickets.html', context)

@login_required
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

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            if new_status.title == "Отклонена" and not form.cleaned_data['rejection_reason']:
                form.add_error('rejection_reason', 'Укажите причину отказа')
            elif new_status.title == "Решена" and not form.cleaned_data['solved_image']:
                form.add_error('solved_image', 'Загрузите фотографию решения')
            else:
                form.save()
                return redirect('tickets')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'main/edit-ticket.html', {'form': form, 'ticket': ticket})

@login_required
@require_POST
def delete_ticket(request, ticket_id):
    try:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.creator == request.user and ticket.can_delete():
            ticket.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Нельзя удалить эту заявку'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})