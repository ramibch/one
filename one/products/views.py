from one.base.utils.generic_views import MultilinguageDetailView

from .models import Product


class ProductDetailView(MultilinguageDetailView):
    model = Product
