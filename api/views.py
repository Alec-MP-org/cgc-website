from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalog.models import FlightsheetDetails, FlightsheetHeader
from api.serializers import FlightsheetDetailsSerializer, FlightsheetHeaderSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class FlightsheetDetails_create(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        details = FlightsheetDetails.objects.all()
        serializer = FlightsheetDetailsSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = FlightsheetDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightsheetDetails_edit(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return FlightsheetDetails.objects.get(flight_key=pk)
        except FlightsheetDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        detail = self.get_object(pk=pk)
        serializer = FlightsheetDetailsSerializer(detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        detail = self.get_object(pk=pk)
        serializer = FlightsheetDetailsSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        detail = self.get_object(pk=pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FlightsheetDetails_edit_many(APIView):
    permission_classes = (IsAuthenticated,)

    def get_objects(self, pk):
        try:
            all_details = FlightsheetDetails.objects.all()
            return all_details.filter(flight_date=pk)
        except FlightsheetDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        details = FlightsheetDetails.objects.all().filter(flight_date=pk)
        serializer = FlightsheetDetailsSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        details = FlightsheetDetails.objects.all().filter(flight_date=pk)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FlightsheetHeader_create(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        headers = FlightsheetHeader.objects.all()
        serializer = FlightsheetHeaderSerializer(headers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlightsheetHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightsheetHeader_edit(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return FlightsheetHeader.objects.get(flight_date=pk)
        except FlightsheetHeader.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        header = self.get_object(pk=pk)
        serializer = FlightsheetHeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        header = self.get_object(pk=pk)
        serializer = FlightsheetHeaderSerializer(header, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        header = self.get_object(pk=pk)
        header.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
