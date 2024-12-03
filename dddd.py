# @admin.register(BrokenOrderProxy)
# class BrokenOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.BROKEN, product__owner=request.user.brand)


# @admin.register(ReturnedOrderProxy)
# class ReturnedOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.RETURNED, product__owner=request.user.brand)


# @admin.register(CanceledOrderProxy)
# class CanceledOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.CANCELED, product__owner=request.user.brand)


# @admin.register(WaitingOrderProxy)
# class WaitingOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.WAITING, product__owner=request.user.brand)

# @admin.register(ArchivedOrderProxy)
# class ArchivedOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.ARCHIVED, product__owner=request.user.brand)


# @admin.register(ReadyToDeliverOrderProxy)
# class ReadyToDeliverOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.READY_TO_DELIVER,
#                                                     product__owner=request.user.brand)



# @admin.register(AdminUserProxy)
# class AdminUserProxyModelAdmin(CustomUserAdmin):
#     list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'change_button', 'delete_button'
#     _type = User.Type.ADMIN
#
#     @admin.display(description=_('Photo'))
#     def image(self, obj):
#         img = obj.photo
#         if img:
#             return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
#         return _('No Image')


#
# operator :
#
#
# class OperatorStackedInline(StackedInline):
#     model = Operator
#
#
# @admin.register(OperatorUserProxy)
# class OperatorUserProxyModelAdmin(CustomUserAdmin):
#     list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'readies', 'change_button', 'delete_button'
#     _type = User.Type.OPERATOR
#     inlines = OperatorStackedInline,
#
#     @admin.display(description=_('Amount of ready to delivery'))
#     def readies(self, obj: OperatorUserProxy):
#         count = Order.objects.filter(Q(status=Order.Status.READY_TO_DELIVER) & Q(operator=obj)).count()
#         if count > 0:
#             url = reverse(f'admin:{obj._meta.app_label}_{Order._meta.model_name}_changelist')
#             url += f'?status={Order.Status.READY_TO_DELIVER}&operator__id__exact={obj.id}'
#             return format_html('<a href="{}">{}</a>', url, count)
#         return count
#
#     @admin.display(description=_('Photo'))
#     def image(self, obj):
#         img = obj.photo
#         if img:
#             return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
#         return _('No Image')
#
#
# @admin.register(OperatorStatisticUserProxy)
# class OperatorStatisticUserProxyModelAdmin(CustomUserAdmin):
#     change_list_template = 'admin/operator_statistics.html'
#     _type = User.Type.OPERATOR
#
#     def changelist_view(self, request, extra_context=None):
#         # Call the parent class's changelist view
#         response = super().changelist_view(request, extra_context)
#
#         try:
#             qs = response.context_data['cl'].queryset
#         except (AttributeError, KeyError):
#             return response
#
#         # Define the metrics
#         metrics = {
#             'total': Count('operator_orders'),
#             'succeed': Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED)),
#             'operator_full_name': F('first_name')
#         }
#
#         # Annotate the queryset with metrics
#         response.context_data['summary'] = list(
#             qs
#             .annotate(**metrics)
#             .annotate(
#                 # Safe division to avoid ZeroDivisionError
#                 of_total_talks=Case(
#                     When(total=0, then=Value(0)),  # If total is zero, return 0
#                     default=F('succeed') * 100 / F('total'),  # Otherwise, divide as usual
#                     output_field=IntegerField()
#                 )
#             )
#             .order_by('first_name')
#         )
#
#         # Prepare the total summary for the metrics
#         updated_metrics = metrics.copy()  # Copy the dictionary to update it
#         del updated_metrics['operator_full_name']  # Remove the 'operator_full_name' key
#         response.context_data['summary_total'] = dict(
#             qs.aggregate(**updated_metrics)
#         )
#
#         # Calculate the overall percentage
#         total_succeed = response.context_data['summary_total'].get('succeed', 0)
#         total_count = max(response.context_data['summary_total'].get('total', 1), 1)  # Prevent division by zero
#         response.context_data['overall'] = (total_succeed * 100) // total_count
#
#         # Calculate the statistics over time (monthly)
#         summary_over_time = OperatorStatisticUserProxy.objects.filter(
#             operator_orders__status=Order.Status.DELIVERED
#         ).annotate(
#             period=TruncMonth('operator_orders__created_at', output_field=DateTimeField())
#         ).values('period').annotate(
#             total=Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED))
#         ).order_by('period')
#
#         # Get the range (low/high) of totals for the entire time range
#         summary_range = summary_over_time.aggregate(
#             low=Min('total'),
#             high=Max('total'),
#         )
#         high = summary_range.get('high', 0)
#         low = summary_range.get('low', 0)
#
#         # Prepare the summary over time with percentages
#         response.context_data['summary_over_time'] = [{
#             'period': x['period'],
#             'total': x['total'] or 0,
#             'pct': ((x['total'] or 0) - low) / (high - low) * 100 if high > low else 0,
#         } for x in summary_over_time]
#
#         return response