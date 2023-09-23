# python lib
import datetime

# django lib
from rest_framework import serializers
from ..exceptions import DuplicateValuesException
from .option_serializer import OptionSerializer

# custom lib
from ..models import List,Option

class ListSerialiser(serializers.ModelSerializer):
    unique_values=serializers.SerializerMethodField()
    unique_name = serializers.SerializerMethodField()
    option_set = OptionSerializer(many=True)

    class Meta:
        model = List
        fields = [
            'name',
            'option_set',
            'id',
            'unique_values',
            'unique_name',
        ]

        read_only_fields = ['id','unique_values','unique_name']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        options_data = validated_data.pop('option_set')
        validated_data['created_by'] = current_user
        list = List.objects.create(**validated_data)
        for option in options_data:
            print(option)
            Option.objects.create(list=list, **option)
        return list

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        # return super().update(instance, validated_data)
        # instance.name = validated_data.get('name')
        # instance.values = validated_data.get('values')
        options_data = validated_data.pop('option_set')
        self.validate_data(options_data)
        options = instance.option_set.all()
        options = list(options)
        instance = super().update(instance, validated_data)
        rank=1
        if (len(options_data)>=len(options)):
            for option_data in options_data:
                if options:
                    option = options.pop(0)
                    option.rank = rank #option_data.get('rank')
                    option.value = option_data.get('value')
                    # print(option)
                    option.save()
                else:
                    Option.objects.create(list=instance,rank=rank,value=option_data.get('value'))
                rank+=1
        else:
            for option in options:
                if options_data:
                    option_data=options_data.pop(0)
                    # option.rank = option_data.get('rank')
                    option.value = option_data.get('value')
                    option.save()
                else:
                    Option.objects.filter(id=option.id).delete()
        return instance


    def validate_data(self,options_data):
        options=[]
        for option_data in options_data:
            if (option_data.get('value') != ''):
                options.append(option_data.get('value').lower())
            else:
                raise (DuplicateValuesException)
        print(options)
        check_duplicate = len(set(options)) != len(options)
        if (check_duplicate):
            raise (DuplicateValuesException)
        return True

    def get_unique_values (self,obj):
        options=[]
        for option in obj.option_set.all():
            options.append(option.value.lower())
        # print(options)
        # check_duplicate = len(set(options)) != len(options)
        # if (check_duplicate):
        #     raise (DuplicateValuesException)
        # check_duplicate=len(set(obj.values))!= len(obj.values)
        # if (check_duplicate):
        #     raise (DuplicateValuesException)
        return True

    def get_unique_name (self,obj):
        names=[]
        for option in List.objects.values('name'):
            names.append(option['name'].lower())
        print(names)
        # check_duplicate_name = (obj.name.lower() in set(names))
        # if (check_duplicate_name):
        #     raise (DuplicateValuesException)
        return True
