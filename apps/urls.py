from django.urls import path

from apps.views import AllProductListView, LogoutView, ProfileTemplateView, ProfileUpdateView, \
    PasswordUpdateView, ProductListView, ProductDetailView, ProductSearchListView, \
    MarketListView, MyStreamsListView, StreamCreateView, StreamDetailView, \
    StatisticsListView, MyOrdersTemplateView, OrderDetailView, LoginRegisterView

urlpatterns = [
    path('', AllProductListView.as_view(), name='main-page'),
    path('category', ProductListView.as_view(), name='category'),
    path('market', MarketListView.as_view(), name='market'),
    path('stream', MyStreamsListView.as_view(), name='stream'),
    path('stream-create', StreamCreateView.as_view(), name='stream_create'),
    path('stream/<int:pk>', StreamDetailView.as_view(), name='stream_detail'),
    path('statistic', StatisticsListView.as_view(), name='statistic'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('success-product/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('ordered-products', MyOrdersTemplateView.as_view(), name='ordered-products'),
    path('search/', ProductSearchListView.as_view(), name='product-search'),
    path('login', LoginRegisterView.as_view(), name='login-page'),
    path('logout', LogoutView.as_view(), name='logout-page'),
    path('users/profile', ProfileTemplateView.as_view(), name='profile'),
    path('users/profile-settings', ProfileUpdateView.as_view(), name='profile-settings'),
    path('users/password-change', PasswordUpdateView.as_view(), name='pass-settings')
]
