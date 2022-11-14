from pickle import TRUE
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models import signals
import datetime
from datetime import date
from heapq import nsmallest, nlargest
# Create your models here.


class Stock(models.Model):
    """
    A model to store all student related details
    """
    UP = "U"
    DOWN = "D"
    SIDE = "S"
    TREND_CHOICES = [
        (UP, "Upward"),
        (DOWN, "Downward"),
        (SIDE, "Side Wise")
    ]

    name = models.CharField(_("Name"), max_length=50, unique=True)
    trend = models.CharField(_("Trend"), choices=TREND_CHOICES,
                             max_length=30, blank=True)
    todays_high = models.FloatField(_("Today's High"), blank=True, null=True)
    todays_low = models.FloatField(_("Today's Low"), blank=True, null=True)
    open_price = models.FloatField(_("Open Price"), blank=True, null=True)
    close_price = models.FloatField(_("Close Price"), blank=True, null=True)
    volume = models.CharField(_("Volume"), max_length=30,
                              blank=True, null=True)
    support = models.FloatField(_("Support"), blank=True, null=True)
    resistance = models.FloatField(_("Resistance"), blank=True, null=True)
    buy_chance = models.FloatField(_("Chance Buy"), blank=True, null=True)
    sell_chance = models.FloatField(_("Chance Sell"), blank=True, null=True)
    change_rate = models.FloatField(_("Rate Of Change"), blank=True, null=True)
    price = models.CharField(_("Price"), max_length=30,
                             blank=True, null=True)


    def __str__(self):
        return self.name

    def get_current_price(self):
        price = self.stock.all()
        if price:
            return price[len(price)-1]


class PriceChange(models.Model):

    MNT = "Mnt"
    HR = "Hr"
    DAY = "Day"
    WK = "Wk"
    MTH = "Mnth"
    PERIOD_CHOICES = [
        (MNT, "Minitue"),
        (HR, "Hour"),
        (DAY, "Day"),
        (WK, "Week"),
        (MTH, "Month")
    ]

    stock = models.ForeignKey("stock_info.Stock",
                              on_delete=PROTECT)
    period = models.CharField(_("Period"), choices=PERIOD_CHOICES,
                              max_length=30)
    open_price = models.FloatField(_("Open Price"), blank=True)
    close_price = models.FloatField(_("Close Price"), blank=True)
    high_price = models.FloatField(_("High Price"), blank=True)
    low_price = models.FloatField(_("Low Price"), blank=True)
    volume = models.IntegerField(_("Volume"), blank=True)
    change_rate = models.FloatField(_("Rate Of Change"), blank=True)
    created_time = models.DateTimeField(_('Created Time'), auto_now_add=True,
                                        blank=False)

    def __str__(self):
        return self.stock.name + " : " + str(self.get_period_display())


stock_choice = ["yesbank/YB", "indianoverseasbank/IOB",
                "vodafoneidealimited/IC8",
                "indianrailwayfinancecorporation/IRF",
                "centralbankindia/CBO01", "ucobank/UCO"]


def fetch_chance(query):
    dic = {}
    dic["close"] = [item["close_price"] for item in query]
    dic["volume"] = [item["volume"] for item in query]
    dic["high"] = [item["high_price"] for item in query]
    dic["low"] = [item["low_price"] for item in query]
    print(dic)
    return dic


def smallest(array, count):
    new_list = []
    [new_list.append(item) for item in sorted(array) if item
        not in new_list and len(new_list) <= count-1]
    return new_list


def largest(array, count):
    new_list = []
    [new_list.append(item) for item in sorted(array)[::-1] if item
        not in new_list and len(new_list) <= count-1]
    return new_list


def inc_dec(array):
    if len(array) >= 6:
        if array[0] > array[5]:
            return 0
        else:
            return 1
    return 2


def check_volume(vol, price):
    if len(vol) >= 7 and len(price) >= 7:
        if vol[0] >= vol[6] and price[0] >= price[6]:
            return "buy"
        if vol[0] <= vol[6] and price[0] >= price[6]:
            return "low_buy"
        if vol[0] <= vol[6] and price[0] <= price[6]:
            return "sell"
        if vol[0] >= vol[6] and price[0] <= price[6]:
            return "low_sell"


def calculate_chance(sender, instance, created, **kwargs):
    chance = 0
    sell = 0
    values = fetch_chance(PriceChange.objects.filter(
                              stock=instance.stock).values()[::-1])
    stock = Stock.objects.get(id=instance.stock.id)

    support = sum(smallest(values["low"], 4))/4
    resistance = sum(largest(values["high"], 4))/4
    nearest = min([support, resistance],
                  key=lambda x: abs(x-instance.close_price))
    vol = check_volume(values["volume"], values["close"])
    # Checking Chance
    if instance.open_price == instance.low_price:
        chance += 10
    if instance.close_price == instance.high_price:
        chance += 10
    if instance.open_price == instance.low_price and instance.close_price == instance.high_price:
        chance += 5
    if stock.open_price < instance.close_price:
        chance += 5
    if instance.change_rate >= 3 and instance.open_price < instance.close_price:
        chance += 10
    if instance.close_price >= resistance:
        chance += 10
    if inc_dec(values["close"]) == 1 and nearest == resistance:
        chance += 10

    if instance.open_price == instance.high_price:
        sell += 10
    if instance.close_price == instance.low_price:
        sell += 10
    if instance.open_price == instance.high_price and instance.close_price == instance.low_price:
        sell += 5
    if stock.open_price > instance.close_price:
        sell += 5
    if instance.change_rate >= 3 and instance.open_price > instance.close_price:
        sell += 10
    if instance.close_price <= support:
        sell += 10
    if inc_dec(values["close"]) == 0 and nearest == support:
        sell += 10

    stock.support = support
    stock.resistance = resistance
    stock.buy_chance = chance
    stock.sell_chance = sell
    print(vol)
    stock.volume = vol
    stock.save()
    print("Stock Name : ",stock.name,", CHANCE : ", chance,"/75")


signals.post_save.connect(receiver=calculate_chance, sender=PriceChange)


class CurrentPrice(models.Model):
    stock = models.ForeignKey("stock_info.Stock",
                              on_delete=PROTECT, related_name='stock')
    price = models.FloatField(_("Price"), blank=True)
    volume = models.IntegerField(_("Voulume"), blank=True)
    created_time = models.DateTimeField(_('Created Time'), auto_now_add=True,
                                        blank=False)

    def __str__(self):
        return self.stock.name + " : " + str(self.price)


count = 1


def query_to_list(query):
    dic = {}
    dic["price"] = [item["price"] for item in query]
    dic["volume"] = [item["volume"] for item in query]
    # print([item["id"] for item in query])
    return dic


def uniq_valus(array):
    new_list = []
    for item in array:
        if item not in new_list:
            new_list.append(item)
    return len(new_list)


def create_price_change(query):
    dic = {}
    price_and_volume = query_to_list(query)
    dic["open"] = price_and_volume["price"][4]
    dic["close"] = price_and_volume["price"][0]
    dic["max"] = max(price_and_volume["price"])
    dic["min"] = min(price_and_volume["price"])
    dic["volume"] = sum(price_and_volume["volume"])//5
    dic["change"] = uniq_valus(price_and_volume["price"])
    return dic


def create_change(sender, instance, created, **kwargs):
    global count
    print(count)
    if count % 61 == 0:
        for item in stock_choice:
            stock = Stock.objects.get(name=item)
            values = create_price_change(CurrentPrice.objects.filter(
                                         stock=stock).values()[::-1][:5])
            PriceChange.objects.create(stock=stock, period="Mnt",
                                       open_price=values["open"],
                                       close_price=values["close"],
                                       high_price=values["max"],
                                       low_price=values["min"],
                                       volume=values["volume"],
                                       change_rate=values["change"])
            stock.change_rate = values["change"]
            stock.save()
            print("price change added")
    elif count % 3660 == 0:
        for item in stock_choice:
            stock = Stock.objects.get(name=item)
            values = create_price_change(CurrentPrice.objects.filter(
                                         stock=stock).values()[::-1][:300])
            PriceChange.objects.create(stock=stock, period="Hr",
                                       open_price=values["open"],
                                       close_price=values["close"],
                                       high_price=values["max"],
                                       low_price=values["min"],
                                       volume=values["volume"],
                                       change_rate=values["change"])
            print("price change for hour added")
    else:
        pass
    count += 1


signals.post_save.connect(receiver=create_change, sender=CurrentPrice)


class Trade(models.Model):

    PRO = "Po"
    LOSS = "Ls"
    NEUT = "No"
    IN = "In"

    STATUS_CHOICES = [
        (PRO, "Profit"),
        (LOSS, "Loss"),
        (NEUT, "NO Change"),
        (IN, "In Progress")
    ]

    stock = models.ForeignKey("stock_info.Stock",
                              on_delete=PROTECT)
    buy = models.FloatField(_("Buy Price"), blank=True, null=True)
    sale = models.FloatField(_("Sale Price"), blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), blank=True)
    revenue = models.FloatField(_("Revenue"), blank=True, null=True)
    status = models.CharField(_("Status"), choices=STATUS_CHOICES,
                              max_length=30, blank=True)
    day = models.ForeignKey("stock_info.Today",
                            on_delete=PROTECT, blank=True, null=True)
    log = models.TextField(blank=True)
    created_time = models.DateField(_('Created Time'), auto_now_add=True,
                                        blank=False)

    def __str__(self):
        return str(self.stock.name) + ",  " + self.status + ",  " +str(self.day)


class MyProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=PROTECT)
    mobile = PhoneNumberField(unique=True)
    trades = models.IntegerField(_("Number Of Trades"), blank=True)
    success = models.IntegerField(_("Success"), blank=True)
    failure = models.IntegerField(_("Failure"), blank=True)
    profit = models.FloatField(_("Total Profit"), blank=True)
    loss = models.FloatField(_("Total Loss"), blank=True)
    wallet = models.FloatField(_("Wallet Balance"), blank=True)
    target_percentage = models.FloatField(_("Target Percentage"), blank=True)
    gain_margin = models.FloatField(_("Margin"), blank=True)

    def __str__(self):
        return str(self.user.username)


class Today(models.Model):
    capital = models.IntegerField(_("Capital"), blank=True, null=True)
    target = models.FloatField(_("Target Amount"), blank=True, null=True)
    target_points = models.FloatField(_("Target Points"), blank=True, null=True)
    today_target = models.FloatField(_("Target Today"), blank=True, null=True)
    trades_required = models.IntegerField(_("Number Of Trades"), blank=True,
                                          default=10)
    per_trade = models.FloatField(_("Per Trade"), blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), blank=True)
    target_accured = models.BooleanField(default=False)
    diffrence = models.FloatField(_("Diffrence From Target"), blank=True, null=True)
    created_time = models.DateField(_('Created Time'), auto_now_add=True,
                                        blank=False)

    def __str__(self):
        return str(self.created_time.strftime("%b %d, %Y"))


def determine_today(sender, instance, created, **kwargs):
    today = Today.objects.get(id=instance.id)
    if today.capital and today.target_points and today.today_target is None:
        today.today_target = today.capital // 25
        today.per_trade = (today.today_target // today.trades_required)*2
        today.quantity = today.per_trade/today.target_points
        today.save()


signals.post_save.connect(receiver=determine_today, sender=Today)


def trade_analyise(sender, instance, created, **kwargs):
    trade = Trade.objects.get(id=instance.id)
    trade.day = Today.objects.get(created_time=instance.created_time)
    if trade.sale and trade.buy and trade.revenue is None:
        trade.revenue = round((trade.sale-trade.buy)*trade.quantity, 2)
        if trade.revenue > 0:
            trade.status = "Po"
        elif trade.revenue == 0:
            trade.status = "No"
        else:
            trade.status = "Ls"
        trade.save()


signals.post_save.connect(receiver=trade_analyise, sender=Trade)
