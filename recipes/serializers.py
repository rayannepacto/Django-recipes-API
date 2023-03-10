from rest_framework import serializers
from authors.validators import AuthorRecipeValidator
from .models import Category, Recipe
from django.contrib.auth.models import User
from .models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'author', 'category_name', 'tags', 'public', 'preparation',
                  'tag_objects', 'tag_links', 'preparation_time', 'preparation_time_unit', 'servings',
                  'servings_unit',
                  'preparation_steps', 'cover']

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name'
    )
    category_name = serializers.StringRelatedField(source='category')
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(many=True, source='tags', view_name='recipes:recipes_api_v2_tag',
                                                    read_only=True)

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError, )
        return super_validate
