from .user_views import \
    UserListCreateAPIView, UserRetrieveUpdateAPIView, \
    UserActivateAPIView, UserDeactivateAPIView, \
    UserDeleteAPIView, UserUnDeleteAPIView, ALLUserListAPIView, ALLCPSListAPIView, DisplayAdminUsers, ManagerAPIView, update_user
from .my_profile_views import MyProfileRetrieveUpdateAPIView, MyProfileUpdatePasswordAPIView

from .group_views import \
    GroupListCreateAPIView, PermissionListAPIView, \
    GroupRetrieveUpdateDestroyAPIView, ALLGroupListAPIView

from .group_views import GroupRetrieveAPIView