from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import NewItemForm, EditItemForm, ReviewMessageForm
from .models import Item, Category, Review, ReviewMessage
from chat.models import Chat
from chat.forms import ChatMessage, ChatMessageForm 

def browse(request):
    query=request.GET.get('query','')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    item = Item.objects.filter(is_sold=False)

    if category_id:
        item = item.filter(category_id=category_id)

    if query: 
        item = item.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/browse.html', {
        'items': item,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })




def detail(request, pk,):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    review = Review.objects.filter(user=item.created_by).first()

    if request.method == "POST":
        form = ReviewMessageForm(request.POST)

        if form.is_valid():
            review_message = form.save(commit=False)

            # Check if a valid Review instance exists
            if review:
                review_message.review = review
                review_message.created_by = request.user
                review_message.save()

                # Optionally, update the review instance (if needed)
                review.save()

                return redirect('item:detail', pk=pk)
            else:
                return redirect('item:detail', pk=pk)
    else:
        form = ReviewMessageForm()

    return render(request, 'item/detail.html', {
        'review': review,
        'form': form,
        'item': item,
        'related_items': related_items,
    })

@login_required
def new(request):

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')



@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })

