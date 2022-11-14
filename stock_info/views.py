from django.shortcuts import render,redirect
from django.views.generic import TemplateView, RedirectView
from .models import  Trade, Stock, Today
from .tasks import stock
from django.contrib import messages
from datetime import date
from django.db.models import Sum


# Create your views here.

class Home_view(TemplateView):
    template_name = 'home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(Home_view, self).get_context_data(**kwargs)
        context["stocks"] = Stock.objects.all()
        # today = Trade.objects.filter(created_time=date.today())
        # context["trades"] = today
        # context["today_revenue"] = today.aggregate(Sum('revenue'))
        # context["trades_today"] = today.count()
        # context["total_revenue"] = Trade.objects.all().aggregate(Sum('revenue'))
        # # day = Today.objects.get(created_time=date.today())
        # context["today"] = day
        # context["target"] = (day.target * 100)//day.capital

        return context

    def post(self, request):
        sto = request.POST.get('stock', '')
        option = request.POST.get('option', '')
        price = request.POST.get('price', '')
        units = request.POST.get('units', '')
        stop_loss = request.POST.get('stop_loss', '')
        target = request.POST.get('target', '')
        print(sto, option, price, units)
        stock.delay("https://groww.in/charts/stocks/"+sto+"?exchange=NSE",
                    sto, int(units), float(price), option, float(stop_loss),
                    float(target))
        messages.error(request, "Invalid Credentials")
        return redirect("home")
