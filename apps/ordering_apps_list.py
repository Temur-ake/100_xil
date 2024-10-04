# from django.contrib import admin
#
#
# def get_app_list(self, request, app_label=None):
#     """
#     Return a sorted list of all the installed apps that have been
#     registered in this site.
#     """
#     ordering = {
#         "Buyurtmalar": 1,
#         "Yangilar": 2,
#         "Arxivlanganlar": 3,
#         "Yetkazishga tayyorlar": 4,
#         "Yetkazilayoganlar": 5,
#         "Yetkazilganlar": 6,
#         "Nosozlar": 7,
#         "Qaytganlar": 8,
#         "Bekor qilinganlar": 9,
#         "Kutayotganlar": 10,
#     }
#     app_dict = self._build_app_dict(request)
#
#     app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
#
#     for app in app_list:
#         app['models'].sort(key=lambda x: ordering[x['name']])
#
#     return app_list
#
#
# admin.AdminSite.get_app_list = get_app_list
