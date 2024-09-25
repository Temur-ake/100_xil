from django.urls import path

from apps.views import AllProductListView, LogoutView, ProfileTemplateView, ProfileUpdateView, \
    PasswordUpdateView, ProductListView, ProductDetailView, ProductSearchListView, \
    MarketListView, MyStreamsListView, StreamCreateView, StreamDetailView, \
    StatisticsListView, MyOrdersTemplateView, OrderDetailView, LoginRegisterView, ProductStatisticListView, \
    RequestsTemplateView, ConcursTemplateView, PaymentTemplateView, DiagramTemplateView, OperatorTemplateView, \
    AdminPageTemplateView, OrderListView, OperatorOrderDetail, UserPhotoUpdateView

urlpatterns = [
    path('', AllProductListView.as_view(), name='main-page'),
    path('category', ProductListView.as_view(), name='category'),
    path('product-statistic/<int:pk>', ProductStatisticListView.as_view(), name='product_statistic'),
    path('market', MarketListView.as_view(), name='market'),
    path('stream', MyStreamsListView.as_view(), name='stream'),
    path('stream-create', StreamCreateView.as_view(), name='stream_create'),
    path('stream/<int:pk>', StreamDetailView.as_view(), name='stream_detail'),
    path('statistic', StatisticsListView.as_view(), name='statistic'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('success-product/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('ordered-products', MyOrdersTemplateView.as_view(), name='ordered-products'),
    path('search/', ProductSearchListView.as_view(), name='product-search'),
    path('requests', RequestsTemplateView.as_view(), name='requests'),
    path('competition', ConcursTemplateView.as_view(), name='competition'),
    path('payment', PaymentTemplateView.as_view(), name='payment'),
    path('diagrams', DiagramTemplateView.as_view(), name='diagrams'),
    path('operator', OrderListView.as_view(), name='operator'),
    path('operator/<str:status>', OrderListView.as_view(), name='operator'),
    path('operator/order/<int:pk>', OperatorOrderDetail.as_view(), name='operator-order-detail'),
    path('admin-page', AdminPageTemplateView.as_view(), name='admin_page'),
    path('login', LoginRegisterView.as_view(), name='login-page'),
    path('logout', LogoutView.as_view(), name='logout-page'),
    path('users/profile', ProfileTemplateView.as_view(), name='profile'),
    path('users/profile-settings', ProfileUpdateView.as_view(), name='profile-settings'),
    path('users/photo-settings', UserPhotoUpdateView.as_view(), name='photo-settings'),
    path('users/password-change', PasswordUpdateView.as_view(), name='pass-settings')
]
