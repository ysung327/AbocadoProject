from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vacations.models import Vacation, Detail, VacationInfo
from vacations.serializers import VacationSerializer, DetailSerializer, VacationInfoSerializer

class VacationList(APIView):
    """
    List all Vacation, add Vacation
    """
    def get(self, request, format=None):  #휴가 데이터 가져오기
        vacations = Vacation.objects.order_by('start_date')
        serializer = VacationSerializer(vacations, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None): # + btn -> 새로운 휴가 추가하기
        if(request.data["addPressed"]==1):
            vacation = Vacation.objects.create()
            updateInfo()
            serializer = VacationSerializer(vacation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class VacationInfoList(APIView):
    """
    List VacationInfo
    """
    def get(self, request, format=None):  #휴가요약 데이터 가져오기
        vacationInfo = VacationInfo.objects.all()[0] #filter 해당 user로 교체
        serializer = VacationInfoSerializer(vacationInfo)
        return Response(serializer.data)

class VacationDetail(APIView):
    """
    Retrieve, update or delete a vacation instance.
    """
    def get_object(self, pk):
        try:
            return Vacation.objects.get(pk=pk)
        except Vacation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None): 
        vacation = self.get_object(pk)
        serializer = VacationSerializer(vacation)
        return Response(serializer.data)

    def put(self, request, pk, format=None): # edit btn -> 휴가 데이터 수정하기
        vacation = self.get_object(pk)
        serializer = VacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            updateInfo()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None): #휴가 데이터 지우기
        vacation = self.get_object(pk)
        vacation.delete()
        updateInfo()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailList(APIView):

    def put(self, request, format=None): # 디테일 데이터 가져오기
        vacation = Vacation.objects.get(pk=request.data["vacation"])
        details = Detail.objects.filter(vacation=vacation)
        serializer = DetailSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request, format=None): # 디테일 데이터를 vacation과 연결
        return Response(status=status.HTTP_204_NO_CONTENT)

class TypeList(APIView):

    def put(self, request, format=None): # 타입 데이터 가져오기
        _type = Detail.objects.filter(type_of_detail=request.data["type_of_detail"])
        serializer = DetailSerializer(_type, many=True)
        return Response(serializer.data)

    def post(self, request, format=None): # 새로운 디테일 추가하기
        detail = Detail.objects.create()
        serializer = DetailSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailDetail(APIView):

    def get_object(self, pk):
        try:
            return Detail.objects.get(pk=pk)
        except Detail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        detail = self.get_object(pk)
        serializer = DetailSerializer(detail)
        return Response(serializer.data)

    def put(self, request, pk, format=None): # edit btn -> 디테일 데이터 수정하기
        detail = self.get_object(pk)
        serializer = DetailSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None): #디테일 데이터 지우기
        detail = self.get_object(pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def updateInfo():
    info = VacationInfo.objects.all() #filter 해당 user로 교체
    info = info[0]
    info.total = info.calculateTotal()
    info.gone = info.calculateGone()
    info.left = info.total - info.gone
    info.save()