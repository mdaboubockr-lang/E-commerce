from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from Product.models import Product, Category
from Cart.views import get_cart_summary_for_user

FALLBACKS = {
    'fruits-vegetables': '/static/images/freshmart/cat-fruits.jpg',
    'dairy-eggs': '/static/images/freshmart/cat-dairy.jpg',
    'beverages': '/static/images/freshmart/cat-beverages.jpg',
    'snacks-munchies': '/static/images/freshmart/cat-snacks.jpg',
    'staples': '/static/images/freshmart/cat-staples.jpg',
    'personal-care': '/static/images/freshmart/cat-personal-care.jpg',
    'household': '/static/images/freshmart/cat-household.jpg',
    'baby-care': '/static/images/freshmart/cat-baby-care.jpg',
    'bakery': '/static/images/freshmart/cat-bakery.jpg',
    'meat-fish': '/static/images/freshmart/cat-meat-fish.jpg',
    'frozen-foods': '/static/images/freshmart/cat-frozen.jpg',
    'health-wellness': '/static/images/freshmart/cat-health.jpg',
    'pet-care': '/static/images/freshmart/cat-pet.jpg',
    'organic-products': '/static/images/freshmart/cat-organic.jpg',
    'international-foods': '/static/images/freshmart/cat-international.jpg',
}
PRODUCT_FALLBACKS = ['/static/images/freshmart/product-banana.jpg','/static/images/freshmart/product-milk.jpg','/static/images/freshmart/product-rice.jpg','/static/images/freshmart/product-eggs.jpg','/static/images/freshmart/product-tomato.jpg','/static/images/freshmart/product-potato.jpg','/static/images/freshmart/product-apple.jpg','/static/images/freshmart/product-oil.jpg']
CATEGORY_CARDS = [
    ('Fruits & Vegetables','fruits-vegetables','images/freshmart/cat-fruits.jpg'),('Dairy & Eggs','dairy-eggs','images/freshmart/cat-dairy.jpg'),('Beverages','beverages','images/freshmart/cat-beverages.jpg'),('Snacks & Munchies','snacks-munchies','images/freshmart/cat-snacks.jpg'),('Staples','staples','images/freshmart/cat-staples.jpg'),('Personal Care','personal-care','images/freshmart/cat-personal-care.jpg'),('Household','household','images/freshmart/cat-household.jpg'),('Baby Care','baby-care','images/freshmart/cat-baby-care.jpg'),('Bakery','bakery','images/freshmart/cat-bakery.jpg'),('Meat & Fish','meat-fish','images/freshmart/cat-meat-fish.jpg'),('Frozen Foods','frozen-foods','images/freshmart/cat-frozen.jpg'),('Health & Wellness','health-wellness','images/freshmart/cat-health.jpg'),('Pet Care','pet-care','images/freshmart/cat-pet.jpg'),('Organic Products','organic-products','images/freshmart/cat-organic.jpg'),('International Foods','international-foods','images/freshmart/cat-international.jpg')]
GROCERY_SLUGS = [s for _,s,_ in CATEGORY_CARDS]

def _cart(request):
    if request.user.is_authenticated:
        return get_cart_summary_for_user(request.user)
    return {'cart_items': [], 'cart_total': 0}

def _cards(products):
    result=[]
    for i,p in enumerate(products):
        img = None
        first = p.product_image_set.first()
        if first and first.image:
            img = first.image.url
        else:
            img = FALLBACKS.get(p.product_category.slug, PRODUCT_FALLBACKS[i % len(PRODUCT_FALLBACKS)])
        result.append({'product':p,'image':img})
    return result

def home(request):
    categories = Category.objects.filter(slug__in=GROCERY_SLUGS).order_by('category_name')
    products = Product.objects.filter(product_category__slug__in=GROCERY_SLUGS).select_related('product_category').prefetch_related('product_image_set').all()[:8]
    cart = _cart(request)
    return render(request, 'product/home.html', {'categories':categories,'product_cards':_cards(products),'category_cards':[{'name':n,'slug':s,'image':i} for n,s,i in CATEGORY_CARDS], 'cart_items':cart.get('cart_items',[])})

def product_list(request):
    products = Product.objects.filter(product_category__slug__in=GROCERY_SLUGS).select_related('product_category').prefetch_related('product_image_set').all()
    categories = Category.objects.filter(slug__in=GROCERY_SLUGS).order_by('category_name')
    search_query = request.GET.get('q','').strip()
    if search_query:
        products = products.filter(Q(product_name__icontains=search_query)|Q(description__icontains=search_query)|Q(product_category__category_name__icontains=search_query))
    cart = _cart(request)
    return render(request,'product/product_list.html',{'products':products,'product_cards':_cards(products),'categories':categories,'search_query':search_query,'cart_items':cart.get('cart_items',[]),'cart_total':cart.get('cart_total',0),'page_title':'All Products'})

def category_shop(request, slug):
    category = get_object_or_404(Category, slug=slug, slug__in=GROCERY_SLUGS)
    products = Product.objects.filter(product_category=category).select_related('product_category').prefetch_related('product_image_set')
    categories = Category.objects.filter(slug__in=GROCERY_SLUGS).order_by('category_name')
    cart = _cart(request)
    return render(request,'product/product_list.html',{'products':products,'product_cards':_cards(products),'categories':categories,'current_category':category,'page_title':category.category_name,'cart_items':cart.get('cart_items',[]),'cart_total':cart.get('cart_total',0)})

def product_detail_view(request, pk):
    product = Product.objects.filter(pk=pk).prefetch_related('product_image_set','productvariant_set').first()
    cart = _cart(request)
    return render(request,'product/product_detail.html',{'product':product,'cart_items':cart.get('cart_items',[]),'cart_total':cart.get('cart_total',0),'cart_open':request.GET.get('cart_open')=='1'})
