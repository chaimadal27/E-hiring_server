# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import JobCategory, Job
from .job_serialiser import JobSerializer


class JobCategorySerialiser(serializers.ModelSerializer):
    job_set = JobSerializer(many=True)

    class Meta:
        model = JobCategory
        fields = [
            'name_fr',
            'name_ar',
            'description_fr',
            'description_ar',
            'is_active',
            'job_set',
            'id'
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        jobs_data = validated_data.pop('job_set')
        validated_data['created_by'] = current_user
        category = JobCategory.objects.create(**validated_data)
        for job in jobs_data:
            Job.objects.create(category=category, **job)
        return category

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        jobs_data = validated_data.pop('job_set')
        jobs = instance.job_set.all()
        jobs = list(jobs)
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        instance = super().update(instance, validated_data)
        for job_data in jobs_data:
            if jobs:
                job = jobs.pop(0)
                job.name_fr = job_data.get('name_fr')
                job.name_ar = job_data.get('name_ar')
                job.save()
            else:
                Job.objects.create(category=instance, **job_data)
        return instance
