from rest_framework import serializers
from .models import Category, Recipe
from django.contrib.auth.models import User
from .models import Tag



class TagSerializer(serializers.Serializer):
    id= serializers.IntegerField()
    name= serializers.CharField(max_length=255)
    slug=serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe 
        fields = ['id', 'title', 'description', 'author', 'category_name', 'tags', 'public', 'preparation', 'tag_objects', 'tag_links']
    
    public = serializers.BooleanField(source='is_published',read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name'
    )   
    category_name = serializers.StringRelatedField(source='category')    
    tag_objects= TagSerializer(many=True, source='tags')
    tag_links = serializers.HyperlinkedRelatedField(many=True, source='tags',view_name='recipes:recipes_api_v2_tag', read_only=True)





    def any_method_name(self,recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
