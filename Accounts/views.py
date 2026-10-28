from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from Accounts.models import CustomerProfile, Address
from Accounts.forms import RegistrationForm, ProfileForm, AddressForm
from Product.models import Product


def register(request):
    if request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.create(user=user)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request=request, template_name='Accounts/register.html', context={'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = None

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

        if user is not None:
            user = authenticate(request=request, username=user.username, password=password)

        if user:
            login(request=request, user=user)
            return redirect('/')

        messages.error(request, 'Invalid email or password.')

    return render(request=request, template_name='Accounts/login.html')


def logout_view(request):
    logout(request=request)
    return redirect('home')


@login_required
def profile(request):
    customer = CustomerProfile.objects.get_or_create(user=request.user, defaults={'phone': ''})[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('/profile/')
    else:
        form = ProfileForm(instance=customer)

    return render(request=request, template_name='Accounts/profile.html', context={'form': form, 'customer': customer})


@login_required
def address_create(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            customer.address.add(address)
            messages.success(request, 'Address added successfully.')
            return redirect('address_list')
    else:
        form = AddressForm()

    return render(request=request, template_name='Accounts/address_form.html', context={'form': form})


@login_required
def address_list(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    addresses = customer.address.all()
    return render(request=request, template_name='Accounts/address_list.html', context={'addresses': addresses})


@login_required
def address_update(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    address = get_object_or_404(Address, pk=pk)

    if address not in customer.address.all():
        return redirect('address_list')

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)

    return render(request=request, template_name='Accounts/address_form.html', context={'form': form, 'address': address})


@login_required
def address_delete(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    address = get_object_or_404(Address, pk=pk)

    if address not in customer.address.all():
        return redirect('address_list')

    if request.method == 'POST':
        customer.address.remove(address)
        address.delete()
        messages.success(request, 'Address deleted successfully.')
        return redirect('address_list')

    return render(request=request, template_name='Accounts/address_confirm_delete.html', context={'address': address})
@login_required
def wishlist(request):
    ids = request.session.get('wishlist', [])
    products = Product.objects.filter(pk__in=ids).prefetch_related('product_image_set')
    return render(request, 'Accounts/wishlist.html', {'products': products})

@login_required
def change_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
        return redirect('profile')
    return render(request, 'Accounts/change_password.html', {'form': form})

@login_required
def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ids = request.session.get('wishlist', [])
    ids = [int(x) for x in ids]
    if product.pk in ids:
        ids.remove(product.pk)
        messages.success(request, 'Removed from wishlist.')
    else:
        ids.append(product.pk)
        messages.success(request, 'Added to wishlist.')
    request.session['wishlist'] = ids
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or 'wishlist')
