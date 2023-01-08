from django.shortcuts import render
from django.http import JsonResponse
from django.views import templates
from django.core import serializers
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import datetime
import json
from sapp.models import Ranking
from sapp.api.sudokus import Sudoku
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    context = {}
    return render(request, 'sapp/index.html',context)

def ranking(request):
    context = {}
    return render(request, 'sapp/ranking.html',context)

def get_ranking_list(request):
    ranking_list = Ranking.objects.order_by('elapsed_time')[:100]
    ranking_data = serializers.serialize("json",ranking_list, fields=('name','elapsed_time'))
    ranking_data = json.loads(ranking_data)
    ranking_data = [{**item['fields'],**{"pk" : item['pk']}} for item in ranking_data]
    ranking_data = {
        "data" : ranking_data
    }
    return JsonResponse(ranking_data)

def register_ranking(request):
    if 'elapsed_time' not in request.session:
        return JsonResponse({'status' : 'failed'})

    data = json.loads(request.body)
    name = data['name']
    elapsed_time = request.session['elapsed_time']

    datetime_args = elapsed_time//3600,(elapsed_time%3600)//60,elapsed_time%60
    d = datetime.time(datetime_args[0], datetime_args[1], datetime_args[2]) 

    ranking = Ranking(name = name, elapsed_time = d)
    ranking.save()

    return JsonResponse({'status' : 'success'})

def check_sudoku(request):
    sudoku_api = Sudoku()

    req_data = json.loads(request.body)

    puzzle = req_data['puzzle']
    elapsed_time = req_data['elapsed_time']

    result = sudoku_api.sudoku_check(puzzle)
    data = {}
    if result == True:
        data['status'] = "clear"
        request.session['status'] = "clear"
        request.session['elapsed_time'] = elapsed_time
    else:
        data['status'] = "fail"

    return JsonResponse(data)

def make_sudoku(request):
    sudoku_api = Sudoku()
    board = sudoku_api.generate_sudoku()
    result = {
        'board' : board
    }

    return JsonResponse(result)
