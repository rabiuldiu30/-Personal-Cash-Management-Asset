from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import AddCashForm, ExpenseForm, LoginForm, ProfileForm, RegistrationForm
from .models import AddCash, Expense


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identity = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']
        username = identity

        if '@' in identity:
            user = User.objects.filter(email__iexact=identity).first()
            username = user.username if user else identity

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username/email or password.')

    return render(request, 'ManageCash/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Registration successful. Welcome to ManageCash.')
        return redirect('dashboard')

    return render(request, 'ManageCash/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    cash_entries = AddCash.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_cash = cash_entries.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_cash - total_expense

    transactions = []
    for item in chain(cash_entries[:20], expenses[:20]):
        transactions.append({
            'type': 'Income' if isinstance(item, AddCash) else 'Expense',
            'title': item.source if isinstance(item, AddCash) else item.description,
            'amount': item.amount,
            'datetime': item.datetime,
        })
    transactions.sort(key=lambda item: item['datetime'], reverse=True)

    context = {
        'total_cash': total_cash,
        'total_expense': total_expense,
        'balance': balance,
        'transactions': transactions[:20],
    }
    return render(request, 'ManageCash/dashboard.html', context)


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'ManageCash/profile.html', {'form': form})


@login_required
def add_cash_view(request):
    form = AddCashForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cash = form.save(commit=False)
        cash.user = request.user
        cash.save()
        messages.success(request, 'Cash entry added.')
        return redirect('dashboard')
    return render(request, 'ManageCash/transaction_form.html', {'form': form, 'title': 'Add Cash'})


@login_required
def add_expense_view(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Expense recorded.')
        return redirect('dashboard')
    return render(request, 'ManageCash/transaction_form.html', {'form': form, 'title': 'Add Expense'})
