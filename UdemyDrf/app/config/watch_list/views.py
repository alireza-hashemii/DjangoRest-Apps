from .models import Review, WatchList , StreamingPlatform
from rest_framework.response import Response
from rest_framework import status
from . permissions import *
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView , CreateAPIView
from .serializers import MovieSerializer, ReviewSerialzer , StreamingPlatformSerializer

# Create your views here.
class MovieWatchList(APIView):
    def get(self , request):
        movies = WatchList.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"note":"You sent bad request"},status=status.HTTP_400_BAD_REQUEST)
        
class MovieWatchDetail(APIView):
    def get(self,request,pk):
        try:
            one_movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
             return Response({"Error":"Item Does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(one_movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = WatchList.objects.get(pk = pk)
        serializer = MovieSerializer(movie,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk = pk)
        movie.delete()
        return Response({"status":"deleted item"},status=status.HTTP_400_BAD_REQUES)
        
        


# @api_view(["GET","POST"])
# def movies_list(request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
# #! Example for de-serializing
# #! data_with_json_format = something
# #! instance = io.BytesIO(data_with_json_format)
# #! JSONParser().parse(instance)
        
        
# @api_view(["GET","PUT","DELETE"])
# def one_movie(request,pk):
#     if request.method == "GET":
#         try:
#             one_movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:
#             return Response({"Error":"Item Does not found"},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(one_movie)
#         json = JSONRenderer().render(serializer.data)
#         return Response(json)
#     elif request.method == "PUT":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(JSONRenderer().render(serializer.data))
#         else:
#             return Response(serializer.errors)
#     elif request.method == "DELETE":
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response({"status":"deleted item"},status=status.HTTP_400_BAD_REQUES)
        
class Stream_Platform(APIView):
    def get(self,request):
        try:
            streamingplatform =  StreamingPlatform.objects.all()
        except Exception:
            return Response({"Error":"Object Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamingPlatformSerializer(streamingplatform,many=True,context={'request': request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            single_Streamplatform = StreamingPlatform.objects.get(pk = pk)
        except:
            return Response({"Error":"Object Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(single_Streamplatform)
        return Response(serializer.data) 
    
class Single_Stream_Platform(APIView):
    permission_classes = [SuperUserOrReadOnly]
    def get(self,request,pk):
        try:
            one_stream = StreamingPlatform.objects.get(pk = pk)
        except Exception:
            return Response({"Error":"Item Does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(one_stream,context={'request': request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        single_stream_platform = StreamingPlatform.objects.get(pk = pk)
        serializer = StreamingPlatformSerializer(single_stream_platform,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self,request,pk):
        single_stream_platform = StreamingPlatform.objects.get(pk = pk)
        single_stream_platform.delete()
        return Response({"status":"deleted item"},status=status.HTTP_400_BAD_REQUES)
        
        
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerialzer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerialzer
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        query = Review.objects.filter(movie__id = pk )
        return (query)
    
class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    permission_classes = [IsOwnerOrReadOnly]
    

class CreateMovieReview(CreateAPIView):
    serializer_class = ReviewSerialzer
    
    def get_queryset(self,pk):
        pk = self.kwargs["pk"]
        movie = WatchList.objects.filter(pk = pk)
        user = self.request.user
        query_user  = Review.objects.filter(movie__id = movie.id, review_author = user)
        if query_user.exists():
            raise ValidationError("You have already reviewd this movie!")      
        elif query_user == None:
            movie = WatchList.objects.filter(pk = pk)
            new_review = Review(review_author=self.request.user.id,
                                rating = self.request.rating,
                                description = self.request.description,
                                active = self.request.active,
                                movie = movie,
                                )
            new_review.save()
            return (new_review)
    
            
