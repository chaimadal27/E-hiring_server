from apps.core.mixins.serializers import NestedUpdateMixin, NestedCreateMixin
from rest_framework import serializers
from ..models.activity_type import ActivityType
from ..serializers.activity_serializer import ActivitySerializer
from ..models.activity import Activity


class ActivityTypeSerializer(NestedCreateMixin, NestedUpdateMixin):
    activity_set = ActivitySerializer(many=True)

    class Meta:
        model = ActivityType
        fields = ['id', 'activity_type_name', 'business_unit', 'activity_set']
        read_only_fields = ['id']
        nested_fields = {'activity_set': 'activity'}


# class ActivityTypeSerializer(serializers.ModelSerializer):
#     activity_set = ActivitySerializer(many = True)
#     class Meta:
#         model = ActivityType
#         fields = ['id','activity_type_name','business_unit','activity_set']
#         read_only_fields = ['id']
#
#
#     def create(self, validated_data):
#
#         activityData = validated_data.pop('activity_set')
#         activityType = ActivityType.objects.create(
#                 activity_type_name = validated_data['activity_type_name']
#                 )
#         activityType.business_unit.set(validated_data['business_unit'])
#         for act_data in activityData:
#             Activity.objects.create(
#                 activity_name=act_data.get('activity_name'),
#                 activity_type=activityType,
#
#             )
#
#         return activityType
#
#     def update(self, instance, validated_data):
#         activityData = validated_data.pop('activity_set')
#         instance = super().update(instance, validated_data)
#
#         if activityData:
#             for item in activityData:
#                 Activity.objects.update_or_create(
#                         activity_name = item['activity_name'],
#                         activity_type = instance
#                         )
#         else:
#             activity_to_delete = Activity.objects.filter(
#                     activity_type = instance
#                     )
#             for item in activity_to_delete:
#                 item.delete()
#         return instance
#
#
#
