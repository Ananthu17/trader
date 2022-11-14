from django.contrib import admin
# Register your models here.
from .models import Stock, PriceChange, CurrentPrice, \
                    Trade, MyProfile, Today
# Register your models here.


admin.site.register(Stock)
admin.site.register(PriceChange)
admin.site.register(CurrentPrice)
admin.site.register(Trade)
admin.site.register(MyProfile)
admin.site.register(Today)
