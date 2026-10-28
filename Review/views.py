from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review
from Product.models import Product
from Accounts.models import CustomerProfile
from .forms import ReviewForm


@login_required
def review_create(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    customer = get_object_or_404(CustomerProfile, user=request.user)

    if Review.objects.filter(product=product, customer=customer).exists():
        messages.error(request, 'You have already submitted a review for this product.')
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = customer
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'review/review_list.html', {'form': form, 'product': product})


@login_required
def review_update(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    review = get_object_or_404(Review, pk=pk, customer=customer)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request=request, message='Review updated')
            return redirect('product_detail', pk=review.product.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request=request,
        template_name='reviews/review_form.html',
        context={'form': form, 'review': review},
    )


@login_required
def review_delete(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    review = get_object_or_404(Review, pk=pk, customer=customer)

    if request.method == 'POST':
        product_pk = review.product.pk
        review.delete()
        messages.success(request=request, message='Review Deleted')
        return redirect('product_detail', pk=product_pk)

    return render(
        request=request,
        template_name='reviews/review_confirm_delete.html',
        context={'review': review},
    )