from .models import CustomUser, CustomPermission
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    custom_permission = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'given_name', 'family_name',
                  'date_joined', 'is_staff', 'is_active', 'custom_permission')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomPermissionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())

    class Meta:
        model = CustomPermission
        fields = ('user', 'permission_type', 'granted_date')
