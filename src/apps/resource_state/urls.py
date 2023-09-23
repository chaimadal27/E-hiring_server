from django.urls import path
from .views import resource_state_view as v
urlpatterns = [
   
    path(r'resource-state', v.list_create_resource_state),
    path(r'resource-state/<int:pk>', v.get_update_resource_state),
    path(r'resource-state/<int:pk>/delete', v.delete_resource_state),
    path(r'resource-state/<int:pk>/deactivate', v.deactivate_resource_state),
    path(r'resource-state/<int:pk>/activate', v.activate_resource_state),
    path(r'resource-state/delete/all', v.delete_all_resource_states),
    path(r'resource-state/deactivate/all', v.deactivate_all_resource_states),    
    path(r'resource-state/activate/all', v.activate_all_resource_states),
]
