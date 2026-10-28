# FreshMart UI update

This version changes the project into a grocery-first FreshMart storefront with separate routes/pages.

## Main routes
- `/` — FreshMart home page
- `/shop/` — all grocery products
- `/shop/fruits-vegetables/` — Fruits & Vegetables category
- `/shop/dairy-eggs/` — Dairy & Eggs category
- `/shop/beverages/` — Beverages category
- `/shop/snacks-munchies/` — Snacks & Munchies category
- `/shop/staples/` — Staples category
- `/shop/personal-care/` — Personal Care category
- `/shop/household/` — Household category
- `/shop/baby-care/` — Baby Care category
- `/shop/bakery/` — Bakery category
- `/shop/meat-fish/` — Meat & Fish category
- `/shop/frozen-foods/` — Frozen Foods category
- `/shop/health-wellness/` — Health & Wellness category
- `/shop/pet-care/` — Pet Care category
- `/shop/organic-products/` — Organic Products category
- `/shop/international-foods/` — International Foods category
- `/product/<id>/` — separate product detail page
- `/cart/` — cart
- `/orders/` — orders
- `/orders/<id>/` — order details
- `/profile/` — account dashboard
- `/address/` — saved addresses
- `/wishlist/` — wishlist
- `/password/change/` — change password

## Seed the grocery catalog
Run:

```bash
python manage.py seed_grocery
```

This creates 15 grocery categories, sample grocery products, prices in BDT and cart-ready variants.

The new design uses local image assets under `static/images/freshmart/` and fallback product images under `media/products/images/`, so it does not depend on an external image host.
