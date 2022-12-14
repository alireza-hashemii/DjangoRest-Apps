from rest_framework import serializers
from .models import  Review, StreamingPlatform, WatchList
from . models import WatchList
   
class ReviewSerialzer(serializers.ModelSerializer):
    review_author = serializers.StringRelatedField(read_only=True)
     
    class Meta:
        model = Review
        fields = "__all__"
        
 #! Write custom validator
# def tit_validator(title):
#         if len(title) < 3:
#             raise serializers.ValidationError("Length of field title can't be less than 3")
#         return title  
    
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=60,validators=[tit_validator])
#     description = serializers.CharField(max_length=100)
#     published = serializers.BooleanField()
    
#     def create(self, validated_data):
#         new_movie = Movie.objects.create(**validated_data)
#         return new_movie
    
#     def update(self,instance,validate_data):
#         instance.title = validate_data.get("title",instance.title)
#         instance.description = validate_data.get("description",instance.description)
#         instance.published = validate_data.get("published",instance.published)
#         instance.save()
#         return (instance)
    
#! Field-level validation
    # def validate_title(self,value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name is too short")
    #     else: 
    #         return value
    
 #! Object-level validation
    # def validate(self,data):
    #     if data["title"] == data["description"]:
    #         raise serializers.ValidationError("Value for field description and data should't be same")
    #     return data
    
class MovieSerializer(serializers.ModelSerializer):
    len_title = serializers.SerializerMethodField()
    reviews = ReviewSerialzer(many=True,read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"
        
    def get_len_title(self,object):
        length = len(object.title)
        return (f"{length}")
             
             
class StreamingPlatformSerializer(serializers.ModelSerializer):
    #? watchlist = MovieSerializer(read_only=True,many=True)
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name= "watch_list:one_movie"
    )
    class Meta:
        model = StreamingPlatform
        fields = "__all__"
        
        
