from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from item.models import Item


@login_required
def index(request):
    all_items = Item.objects.filter(created_by=request.user)
    items = Item.objects.filter(created_by=request.user, is_sold=False)
    sold = Item.objects.filter(created_by=request.user, is_sold=True)
    sold_sum = Item.objects.filter(created_by=request.user, is_sold=True).aggregate(sum_price=Sum('price'))['sum_price']
    sold_total = Item.objects.filter(created_by=request.user, is_sold=True).count()
    items_total = Item.objects.filter(created_by=request.user).count()
    sold_weight = Item.objects.filter(created_by=request.user, is_sold=True).aggregate(sum_weight=Sum('weight'))['sum_weight']

    percentage_sold = 0
    if items_total > 0:
        percentage_sold = (sold_total / items_total) * 100
    
    if all_items.count() > 0:
        seller = True
    
    else:
        seller = False

    return render(request, 'dashboard/index.html', {
        'seller':seller,
        'all_items':all_items,
        'items': items,
        'percentage_sold': percentage_sold,
        'sold_total':sold_sum,
        'sold_weight':sold_weight,
        'sold':sold,
    })

