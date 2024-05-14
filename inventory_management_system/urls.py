"""inventory_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views, Hod_Views, Staff_Views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.base, name='base'),

                  # LoginPath
                  path('', views.LOGIN, name='login'),
                  path('doLogin', views.do_login, name='doLogin'),
                  path('doLogout', views.do_logout, name='logout'),
                  path('register', views.register, name='register'),

                  # Profile Update
                  path('Profile', views.profile, name='Profile'),
                  path('Profile/update', views.profile_update, name='Profile_update'),

                  # This is Hod Panel url
                  path('Home', Hod_Views.home, name='hod_home'),
                  path('Home/Items/Add', Hod_Views.add_items, name='add_items'),
                  path('Home/Items/Views', Hod_Views.view_items, name='view_items'),
                  path('Home/Items/Edit/<str:id>', Hod_Views.edit_items, name='edit_items'),
                  path('Home/Items/Update', Hod_Views.update_items, name='update_items'),
                  path('Home/Items/Delete/<str:id>', Hod_Views.delete_items, name='delete_items'),
                  path('Home/Items/Detail/<str:item_id>', Hod_Views.item_detail, name="item_detail"),
                  path('issue_item/<str:pk>/', Hod_Views.issue_item, name='issue_item'),
                  path('add_to_stock/<str:pk>', Hod_Views.add_to_stock, name='add_to_stock'),
                  path('stock_out/', Hod_Views.stock_out, name='stock_out'),
                  path('receipt/', Hod_Views.receipt, name='receipt'),

                  path('Home/Department/Add', Hod_Views.add_departments, name='add_departments'),
                  path('Home/Department/View', Hod_Views.view_departments, name='view_departments'),
                  path('Home/Department/Edit/<str:id>', Hod_Views.edit_departments, name='edit_departments'),
                  path('Home/Department/Update', Hod_Views.update_departments, name='update_departments'),
                  path('Home/Department/Delete/<str:id>', Hod_Views.delete_departments, name='delete_departments'),

                  path('Home/Location/Add', Hod_Views.add_locations, name='add_locations'),
                  path('Home/Location/View', Hod_Views.view_locations, name='view_locations'),
                  path('Home/Location/Edit/<str:id>', Hod_Views.edit_locations, name='edit_locations'),
                  path('Home/Location/Update', Hod_Views.update_locations, name='update_locations'),
                  path('Home/Location/Delete/<str:id>', Hod_Views.delete_locations, name='delete_locations'),

                  path('Home/Purpose/Add', Hod_Views.add_purposes, name='add_purposes'),
                  path('Home/Purpose/View', Hod_Views.view_purposes, name='view_purposes'),
                  path('Home/Purpose/Edit/<str:id>', Hod_Views.edit_purposes, name='edit_purposes'),
                  path('Home/Purpose/Update', Hod_Views.update_purposes, name='update_purposes'),
                  path('Home/Purpose/Delete/<str:id>', Hod_Views.delete_purposes, name='delete_purposes'),

                  path('Home/Category/Add', Hod_Views.add_categories, name='add_categories'),
                  path('Home/Category/View', Hod_Views.view_categories, name='view_categories'),
                  path('Home/Category/Edit/<str:id>', Hod_Views.edit_categories, name='edit_categories'),
                  path('Home/Category/Update', Hod_Views.update_categories, name='update_categories'),
                  path('Home/Category/Delete/<str:id>', Hod_Views.delete_categories, name='delete_categories'),

                  path('Home/Staff/Add', Hod_Views.add_staff, name='add_staff'),
                  path('Home/Staff/View', Hod_Views.view_staff, name='view_staff'),
                  path('Home/Staff/Edit/<str:id>', Hod_Views.edit_staff, name='edit_staff'),
                  path('Home/Staff/Update', Hod_Views.update_staff, name='update_staff'),
                  path('Home/Staff/Delete/<str:admin>', Hod_Views.delete_staff, name='delete_staff'),

                  path('Home/Staff/LeaveView', Hod_Views.leave_view, name='leave_view'),
                  path('Home/Staff/LeaveDetail/<str:staff_id>', Hod_Views.leave_detail, name="leave_detail"),
                  path('Home/Staff/ApproveLeave/<str:id>', Hod_Views.approve_leave, name='approve_leave'),
                  path('Home/Staff/DisapproveLeave/<str:id>', Hod_Views.disapprove_leave, name='disapprove_leave'),

                  path('Home/Staff/Feedback', Hod_Views.feedback, name='feedback'),
                  path('Home/Staff/Feedback/Save', Hod_Views.feedback_save, name='feedback_reply_save'),

                  path('Home/Staff/RequestView', Hod_Views.item_request, name='request_view'),
                  path('Home/Staff/RequestDetail/<str:staff_id>', Hod_Views.item_request_detail, name="request_detail"),
                  path('Home/Staff/ApproveRequest/<str:id>', Hod_Views.approve_request, name='approve_request'),
                  path('Home/Staff/DisapproveRequest/<str:id>', Hod_Views.deny_request, name='deny_request'),

                  path('Home/Medicine/Add', Hod_Views.add_medicines, name='add_medicines'),
                  path('Home/Medicine/manage_medicine', Hod_Views.manage_medicines, name='manage_medicine'),
                  path('Home/Medicine/medicine_detail/<str:pk>', Hod_Views.medicine_detail, name="medicine_detail"),
                  path('Home/Medicine/edit_medicines/<str:pk>', Hod_Views.edit_medicines, name='edit_medicines'),
                  path('Home/Medicine/delete_medicine/<str:pk>/', Hod_Views.delete_medicine, name='delete_medicine'),
                  path('Home/reorder_level/<str:pk>', Hod_Views.reorder_level, name="reorder_level"),
                  path('issue_medicine/<str:pk>/', Hod_Views.issue_medicine, name='issue_medicine'),
                  path('add_to_stock_medicine/<str:pk>', Hod_Views.add_to_stock_medicine, name='add_to_stock_medicine'),
                  path('dispense_receipt/', Hod_Views.medicine_receipt, name='dispense_receipt'),
                  
                  path('download-csv/', Hod_Views.item_csv, name='download_csv'),
                  path('medicine-csv/', Hod_Views.medicine_csv, name='medicine_csv'),

                  
                  # This is Staff urls
                  path('Staff/Home', Staff_Views.home, name='staff_home'),
                  path('Staff/ApplyLeave', Staff_Views.apply_leave, name='apply_leave'),
                  path('Staff/ApplyLeaveSave', Staff_Views.apply_leave_save, name='apply_leave_save'),
                  path('Staff/DeleteLeave/<int:leave_id>/', Staff_Views.delete_leave, name='delete_leave'),

                  path('Staff/Feedback', Staff_Views.staff_feedback, name='staff_feedback'),
                  path('Staff/Feedback/Save', Staff_Views.staff_feedback_save, name='feedback_save'),

                  path('Staff/ItemRequest', Staff_Views.item_request, name='item_request'),
                  path('Staff/ItemRequestSave', Staff_Views.item_request_save, name='item_request_save'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
