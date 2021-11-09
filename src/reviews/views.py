from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from reviews.service import ReviewService
from reviews.serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewView(GenericAPIView):
    serializer_class = ReviewSerializer
    update_serializer_class = ReviewUpdateSerializer
    service = ReviewService()

    def post(self, request):
        response_ok()

    def put(self, request):
        response_ok()

    def delete(self, request):
        response_ok()


class ReviewListView(GenericAPIView):
    serializer_class = ReviewSerializer
    service = ReviewService()

    def get(self, request):
        response_ok()


class CommentView(GenericAPIView):
    serializer_class = CommentSerializer
    service = ReviewService()

    def post(self, request):
        response_ok()

