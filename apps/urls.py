from django.urls import path, re_path

from apps.views import AllProductListView, LogoutView, ProfileTemplateView, ProfileUpdateView, \
    PasswordUpdateView, ProductListView, ProductSearchListView, \
    MarketListView, MyStreamsListView, StreamCreateView, \
    StatisticsListView, MyOrdersTemplateView, OrderDetailView, LoginRegisterView, ProductStatisticListView, \
    RequestListView, CompetitionListView, DiagramTemplateView, \
    AdminPageTemplateView, OrderListView, OperatorOrderDetail, UserPhotoUpdateView, get_districts_by_region, \
    PaymentListView, CurrierListView, CurrierDetail
from apps.views.product_views import ProductStreamDetail
from apps.views.shop_views import AddOrderCreateView
from apps.views.transaction_views import PaymentFormView

urlpatterns = [

    # products - categories
    path('', AllProductListView.as_view(), name='main-page'),
    path('category', ProductListView.as_view(), name='category'),
    path('product-statistic/<int:pk>', ProductStatisticListView.as_view(), name='product_statistic'),
    re_path(r'^product/(?P<slug>[-\w\u0400-\u04FF]+)/$', ProductStreamDetail.as_view(), name='product-detail'),
    path('success-product/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('ordered-products', MyOrdersTemplateView.as_view(), name='ordered-products'),
    path('search/', ProductSearchListView.as_view(), name='product-search'),
    # path('product-search/', product_search, name='product_search'),

    # streams
    path('stream', MyStreamsListView.as_view(), name='stream'),
    path('stream-create', StreamCreateView.as_view(), name='stream_create'),
    path('stream/<int:pk>', ProductStreamDetail.as_view(), name='stream_detail'),
    path('statistic', StatisticsListView.as_view(), name='statistic'),
    path('market', MarketListView.as_view(), name='market'),

    # transaction
    path('payment-history', PaymentListView.as_view(), name='payment_history'),
    path('payment-form', PaymentFormView.as_view(), name='payment_form'),

    # operator
    path('operator', OrderListView.as_view(), name='operator'),
    path('operator/orders/currier-list', CurrierListView.as_view(), name='currier_list'),
    path('operator/ordered-info/<int:pk>', CurrierDetail.as_view(), name='ordered_info_detail'),
    path('operator/product-add', AddOrderCreateView.as_view(), name='operator_product_add'),
    path('operator/<str:status>', OrderListView.as_view(), name='operator'),
    path('operator/order/<int:pk>', OperatorOrderDetail.as_view(), name='operator-order-detail'),

    # currier

    # auth
    path('admin-page', AdminPageTemplateView.as_view(), name='admin_page'),
    path('login', LoginRegisterView.as_view(), name='login-page'),
    path('logout', LogoutView.as_view(), name='logout-page'),
    path('users/profile', ProfileTemplateView.as_view(), name='profile'),
    path('users/profile-settings', ProfileUpdateView.as_view(), name='profile-settings'),
    path('users/photo-settings', UserPhotoUpdateView.as_view(), name='photo-settings'),
    path('users/password-change', PasswordUpdateView.as_view(), name='pass-settings'),
    path('logout', LogoutView.as_view(), name='logout-page'),

    # shop
    path('requests', RequestListView.as_view(), name='requests'),
    path('competition', CompetitionListView.as_view(), name='competition'),
    path('diagrams', DiagramTemplateView.as_view(), name='diagrams'),
    path('get_districts_by_region/<int:region_id>', get_districts_by_region, name='get_districts_by_region')
]
