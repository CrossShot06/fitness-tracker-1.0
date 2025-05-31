from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Custom Admin Panel"
    site_title = "Custom Admin"
    index_title = "Welcome to the Custom Admin"

custom_admin_site = CustomAdminSite(name='custom_admin')
