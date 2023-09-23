from django.urls import path
from .views import activity_type_views as act_type_views
from .views import activity_views as act_views
from .views import sheet_views as sh_views

urlpatterns = [
    # activity type
    path(r'activity-type', act_type_views.list_create_activity_type),
    path(r'activity-type/all', act_type_views.list_all_activity_types),
    path(r'activity-type/<int:pk>', act_type_views.get_update_activity_type),
    path(r'activity-type/<int:pk>/delete', act_type_views.delete_activity_type),
    path(r'activity-type/<int:pk>/deactivate',
         act_type_views.deactivate_activity_type),
    path(r'activity-type/<int:pk>/activate',
         act_type_views.activate_activity_type),
    path(r'activity-type/delete/all', act_type_views.delete_all_activity_types),
    path(r'activity-type/deactivate/all',
         act_type_views.deactivate_all_activity_types),
    path(r'activity-type/activate/all',
         act_type_views.activate_all_activity_types),


    # activity
    path(r'activity', act_views.list_create_activity),
    path(r'activity/<int:pk>', act_views.get_update_activity),
    path(r'activity/<int:pk>/delete', act_views.delete_activity),
    path(r'activity/<int:pk>/deactivate', act_views.deactivate_activity),
    path(r'activity/<int:pk>/activate', act_views.activate_activity),
    path(r'activity/delete/all', act_views.delete_all_activities),
    path(r'activity/deactivate/all', act_views.deactivate_all_activities),
    path(r'activity/activate/all', act_views.activate_all_activity),

    # sheet
    path(r'sheet', sh_views.create_sheet),

]
