from django.urls import path

from apps.views import AllProductListView, LoginRegisterView, LogoutView, ProfileTemplateView, ProfileUpdateView, \
    PasswordUpdateView, ProductListView, ProductDetailView, ProductSearchListView, OrderAttemptedTemplateView, \
    ProductOrderCreateView, MyOrdersListView, MarketListView

urlpatterns = [
    path('', AllProductListView.as_view(), name='main-page'),
    path('category', ProductListView.as_view(), name='category'),
    path('market', MarketListView.as_view(), name='market'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product-order', ProductOrderCreateView.as_view(), name='product-order'),
    path('success-product', OrderAttemptedTemplateView.as_view(), name='success-product'),
    path('ordered-products', MyOrdersListView.as_view(), name='ordered-products'),
    path('search/', ProductSearchListView.as_view(), name='product-search'),
    path('login', LoginRegisterView.as_view(), name='login-page'),
    path('logout', LogoutView.as_view(), name='logout-page'),
    path('users/profile', ProfileTemplateView.as_view(), name='profile'),
    path('users/profile-settings', ProfileUpdateView.as_view(), name='profile-settings'),
    path('users/password-change', PasswordUpdateView.as_view(), name='pass-settings')
]
