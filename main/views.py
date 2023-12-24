from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import TransactionForm
from datetime import date
from django.http import HttpResponse
from django.conf import settings
import subprocess

from .models import *

from coinlore_parser.views import CoinloreParser


ALL_TICKERS_URL = 'https://api.coinlore.net/api/tickers/?start={}&limit=100'
TICKER_URL = 'https://api.coinlore.net/api/ticker/?id={}'

def home(request):
    context = {}

    user = request.user
    try:
        transactions = Transaction.objects.filter(user=user)

        sell_transactions = transactions.filter(reason='Продажа').values('token').annotate(total_qnt=Sum('qnt'))
        buy_transactions = transactions.filter(reason='Покупка').values('token').annotate(total_qnt=Sum('qnt')).annotate(avg_price=Avg('price'))

        balance = []

        tickers = []

        for buy_trs in buy_transactions:
            token = buy_trs['token']
            bought_qnt = buy_trs['total_qnt']
            sold_qnt = 0

            for sell_trs in sell_transactions:
                if sell_trs['token'] == token:
                    sold_qnt = sell_trs['total_qnt']

            res_qnt = bought_qnt - sold_qnt

            ticker = Token.objects.get(id=token).ticker

            tickers.append(ticker)

            balance.append({'token_id': token, 'ticker': ticker, 'qnt': res_qnt, 'avg_price': round(buy_trs['avg_price'], 2)})

        cl_parser = CoinloreParser(tickers, ALL_TICKERS_URL, TICKER_URL)
        tickers_prices = cl_parser.get_tickers_prices()

        for balance_item in balance:
            for item in tickers_prices:
                if balance_item['ticker'] == item[0]:
                    balance_item['price'] = round(float(item[-1]), 2)
                    balance_item['price_change'] = round((balance_item['price'] - float(balance_item['avg_price'])) / float(balance_item['avg_price']) * 100, 2)

        context.update({'balance': balance})
    except:
        pass

    return render(request, "home.html", context)


def developers(request):

    developers = Developer.objects.all()

    return render(request, 'developers.html', {'developers': developers})

def projects(request):

    tokens = Token.objects.all()

    return render(request, 'projects.html', {'projects': tokens})

def developer(request, id):
    context = {}

    developer = Developer.objects.get(id=id)

    context.update({'developer': developer})

    dev_tags = developer.tags.all()

    tags = []

    for tag in dev_tags:
        tags.append(tag.title)

    context.update({'tags': tags})

    projects = Token.objects.filter(developer=developer)
    context.update({'projects': projects})

    try:
        is_saved = False
        user = request.user

        user_saved_developers = SavedDeveloper.objects.get(user=user)
        if developer in user_saved_developers.developers.all():
            is_saved = True

        context.update({'is_saved': is_saved})
    except:
        pass

    return render(request, 'developer.html', context)


def project(request, id):
    context = {}

    token = Token.objects.get(id=id)

    context.update({'project': token})

    token_tags = token.tags.all()

    tags = []

    for tag in token_tags:
        tags.append(tag.title)

    context.update({'tags': tags})

    try:
        is_saved = False
        user = request.user

        user_saved_tokens = SavedToken.objects.get(user=user)
        if token in user_saved_tokens.tokens.all():
            is_saved = True

        context.update({'is_saved': is_saved})
    except:
        pass

    return render(request, 'project.html', context)

@login_required
def add_developer_saved(request, dev_id):
    try:
        saved_developer, created = SavedDeveloper.objects.get_or_create(user=request.user)
        developer = get_object_or_404(Developer, id=dev_id)

        if developer in saved_developer.developers.all():
            pass
        else:
            saved_developer.developers.add(developer)
    except:
        pass

    return HttpResponseRedirect(reverse('saved'))

@login_required
def remove_developer_saved(request, dev_id):
    try:
        saved_developer = get_object_or_404(SavedDeveloper, user=request.user)

        if saved_developer.developers.filter(id=dev_id).exists():
            developer = get_object_or_404(Developer, id=dev_id)
            saved_developer.developers.remove(developer)
    except:
        pass

    return HttpResponseRedirect(reverse('saved'))

@login_required
def add_project_saved(request, prj_id):
    try:
        saved_project, created = SavedToken.objects.get_or_create(user=request.user)
        project = get_object_or_404(Token, id=prj_id)

        if project in saved_project.tokens.all():
            pass
        else:
            saved_project.tokens.add(project)
    except:
        pass

    return HttpResponseRedirect(reverse('saved'))

@login_required
def remove_project_saved(request, prj_id):
    try:
        saved_project = get_object_or_404(SavedToken, user=request.user)

        if saved_project.tokens.filter(id=prj_id).exists():
            project = get_object_or_404(Token, id=prj_id)
            saved_project.tokens.remove(project)
    except:
        pass

    return HttpResponseRedirect(reverse('saved'))

def saved(request):
    context = {}

    user = request.user
    context.update({'user': user})

    try:
        saved_tokens = SavedToken.objects.get(user = user).tokens.all()
        saved_developers = SavedDeveloper.objects.get(user=user).developers.all()

        context.update({'developers': saved_developers})
        context.update({'projects': saved_tokens})
    except:
        pass

    return render(request, 'saved.html', context)


def transactions(request):

    context = {}

    user = request.user

    try:
        transactions = Transaction.objects.filter(user=user).order_by('-date')

        context.update({'transactions': transactions})
    except:
        pass

    return render(request, 'transactions.html', context)


def delete_transaction(request, transaction_id):

    try:
        transaction = get_object_or_404(Transaction, id=transaction_id)

        try:
            if transaction.user == request.user:
                transaction.delete()
        except:
            pass
    except:
        pass

    return HttpResponseRedirect(reverse('transactions'))

def add_transaction(request):
    if request.method == 'POST':
        try:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.date = date.today()
                transaction.save()
        except:
            pass

        return HttpResponseRedirect(reverse('transactions'))
    else:
        form = TransactionForm()

        tokens = Token.objects.all()

        reasons_raw = Transaction.REASONS
        reasons = []

        for reason in reasons_raw:
            reasons.append(reason[0])

        return render(request, 'add_transaction.html', {'form': form, 'tokens': tokens, 'reasons': reasons})
