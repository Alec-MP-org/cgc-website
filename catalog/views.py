from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from catalog.models import FlightsheetDetails, FlightsheetHeader
from catalog.forms import SearchFlightSheets, SearchFlights, FlightStats

from datetime import datetime, date, time
import json
import calendar

# functions for views
def searchquery(queryset, field, search):
    if queryset and field and search:
        fieldfilter = field + '__icontains'
        newqueryset = queryset.filter(**{fieldfilter: search})
        return newqueryset
    else:
        return queryset

def daterangequery(queryset, startdate, enddate, datefieldstr):
    ffrange = datefieldstr + '__range'
    ffgte = datefieldstr + '__gte'
    fflte = datefieldstr + '__lte'
    if queryset:
        if startdate and enddate:
            queryset = queryset.filter(**{ffrange: [startdate, enddate]})
        elif startdate and not enddate:
            queryset = queryset.filter(**{ffgte: startdate})
        elif not startdate and enddate:
            queryset = queryset.filter(**{fflte: enddate})
    return queryset

# Create your views here.
@login_required
def flightsheetsearch(request):
    flightsheetheaders = FlightsheetHeader.objects.all()
    if request.GET & SearchFlightSheets.base_fields.keys():
        form = SearchFlightSheets(request.GET)
    else:
        form = SearchFlightSheets(initial={'resultsperpage': 15})

    perpage = 15

    if form.is_valid():
        flightsheetheaders = daterangequery(flightsheetheaders, form.cleaned_data['start_date'], form.cleaned_data['end_date'], 'flight_date')
        if form.cleaned_data['search_duty_instructor'] and form.cleaned_data['search_duty_instructor'] != 'All':
            flightsheetheaders = searchquery(flightsheetheaders, 'duty_instructor', form.cleaned_data['search_duty_instructor'])
        if form.cleaned_data['search_instructor'] and form.cleaned_data['search_instructor'] != 'All':
            flightsheetheaders = searchquery(flightsheetheaders, 'instructor', form.cleaned_data['search_instructor'])
        if form.cleaned_data['search_aei'] and form.cleaned_data['search_aei'] != 'All':
            flightsheetheaders = searchquery(flightsheetheaders, 'air_experience_instructor', form.cleaned_data['search_aei'])
        if form.cleaned_data['search_duty_pilot'] and form.cleaned_data['search_duty_pilot'] != 'All':
            flightsheetheaders = searchquery(flightsheetheaders, 'duty_pilot', form.cleaned_data['search_duty_pilot'])
        if form.cleaned_data['search_tug'] and form.cleaned_data['search_tug'] != 'All':
            flightsheetheaders = searchquery(flightsheetheaders, 'tug_pilot1', form.cleaned_data['search_tug'])
        if form.cleaned_data['resultsperpage']:
            perpage = form.cleaned_data['resultsperpage']

    count = flightsheetheaders.count()
    paginator = Paginator(flightsheetheaders, perpage)
    page = request.GET.get('page')
    flightsheetheaders_paginated = paginator.get_page(page)
    
    context = {
        'flightsheetheaders': flightsheetheaders_paginated,
        'resultcount': count,
        'form': form,
    }

    return render(request, 'flightsheetsearch.html', context=context)

@login_required
def flightsearch(request):
    flights = FlightsheetDetails.objects.all()
    if request.GET & SearchFlights.base_fields.keys():
        form = SearchFlights(request.GET)
    else:
        form = SearchFlights(initial={'resultsperpage': 15})

    perpage = 15

    if form.is_valid():
        flights = daterangequery(flights, form.cleaned_data['start_date'], form.cleaned_data['end_date'], 'flight_date')
        if form.cleaned_data['search_glider'] and form.cleaned_data['search_glider'] != 'All':
            flights = searchquery(flights, 'glider', form.cleaned_data['search_glider'])
        if form.cleaned_data['search_pilot'] and form.cleaned_data['search_pilot'] != 'All':
            flights = searchquery(flights, 'pilot1', form.cleaned_data['search_pilot']) | searchquery(flights, 'pilot2', form.cleaned_data['search_pilot'])
        if form.cleaned_data['search_billing_code'] and form.cleaned_data['search_billing_code'] != 'All':
            flights = searchquery(flights, 'billing_code', form.cleaned_data['search_billing_code'])
        if form.cleaned_data['resultsperpage']:
            perpage = form.cleaned_data['resultsperpage']

    count = flights.count()
    paginator = Paginator(flights, perpage)
    page = request.GET.get('page')
    flights_paginated = paginator.get_page(page)
    
    context = {
        'flights': flights_paginated,
        'resultcount': count,
        'form': form,
    }

    return render(request, 'flightsearch.html', context=context)

@login_required
def flightstats(request):
    form = FlightStats(request.GET)
    context = {
        "form": form,
    }
    
    return render(request, 'flightstats.html', context=context)

@login_required
def flightdata(request):
    dataset = FlightsheetDetails.objects.all()
    if request.GET.get('p'):
        pilot = request.GET.get('p')
        if pilot != 'All':
            dataset = searchquery(dataset, 'pilot1', pilot) | searchquery(dataset, 'pilot2', pilot)
    if request.GET.get('b'):
        billing_code = request.GET.get('b')
        if billing_code != 'All':
            dataset = searchquery(dataset, 'billing_code', billing_code)
    if request.GET.get('t'):
        display_type = request.GET.get('t')
    else:
        display_type = 'month'
    dataset = daterangequery(dataset, request.GET.get('sdate'), request.GET.get('edate'), 'flight_date')

    gliders = set()
    months = set()
    for flight in dataset:
        gliders.add(flight.glider)
        months.add((flight.flight_date.month, flight.flight_date.year))
    gliders = list(gliders)
    months = list(months)

    chart = {}
    chart_title = ''
    yaxis_title = ''
    
    categories = []
    flight_times = []
    
    flights_data_dict = {}
    flights_data = []
    flights_series = []
    glider_series = {}

    if display_type == 'total':
        for glider in gliders:
            flights_data_dict[glider] = {'glider': glider, 'flight_time': 0}

        for flight in dataset:
            flights_data_dict[flight.glider]['flight_time'] += float((datetime.combine(date.min, flight.duration_time) - datetime.min).total_seconds()) / 60

        for glider in flights_data_dict:
            flights_data.append(flights_data_dict[glider])

        for entry in flights_data:
            categories.append(entry['glider'])
            flight_times.append(entry['flight_time'])
    
        flights_series = [{
            'name': 'Flight Time',
            'data': flight_times,
            'color': 'grey'
            }]

        chart_title = 'Total Flight Time per Glider'
        yaxis_title = 'Flight Time (min)'


    elif display_type == 'totalcount':
        for glider in gliders:
            flights_data_dict[glider] = {'glider': glider, 'flight_count': 0}

        for flight in dataset:
            flights_data_dict[flight.glider]['flight_count'] += 1

        for glider in flights_data_dict:
            flights_data.append(flights_data_dict[glider])

        for entry in flights_data:
            categories.append(entry['glider'])
            flight_times.append(entry['flight_count'])
    
        flights_series = [{
            'name': 'Flight Count',
            'data': flight_times,
            'color': 'grey'
            }]

        chart_title = 'Total Flight Count per Glider'
        yaxis_title = 'Flight Count'

    elif display_type == 'monthcount':
        for month in months:
            flights_data_dict[month] = {}
            for glider in gliders:
                flights_data_dict[month][glider] = {'glider': glider, 'flight_count': 0}

        for flight in dataset:
            flights_data_dict[(flight.flight_date.month, flight.flight_date.year)][flight.glider]['flight_count'] += 1

        for glider in gliders:
                glider_series[glider] = {
                    'name': glider,
                    'data': [],
                    }
        
        for datekey in sorted(flights_data_dict.keys()):
            month_name = calendar.month_name[int(datekey[0])] + '-' + str(datekey[1])
            categories.append(month_name)
            for glider in gliders:
                glider_series[glider]['data'].append(flights_data_dict[datekey][glider]['flight_count'])

        for series in glider_series:
            flights_series.append(glider_series[series])

        chart_title = 'Monthly Flight Count per Glider'
        yaxis_title = 'Flight Count'

    else:
        for month in months:
            flights_data_dict[month] = {}
            for glider in gliders:
                flights_data_dict[month][glider] = {'glider': glider, 'flight_time': 0}

        for flight in dataset:
            flights_data_dict[(flight.flight_date.month, flight.flight_date.year)][flight.glider]['flight_time'] += float((datetime.combine(date.min, flight.duration_time) - datetime.min).total_seconds()) / 60

        for glider in gliders:
                glider_series[glider] = {
                    'name': glider,
                    'data': [],
                    }
        
        for datekey in sorted(flights_data_dict.keys()):
            month_name = calendar.month_name[int(datekey[0])] + '-' + str(datekey[1])
            categories.append(month_name)
            for glider in gliders:
                glider_series[glider]['data'].append(flights_data_dict[datekey][glider]['flight_time'])

        for series in glider_series:
            flights_series.append(glider_series[series])

        chart_title = 'Monthly Flight Time per Glider'
        yaxis_title = 'Flight Time (min)'

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': chart_title},
        'yAxis': {'title': {'text': yaxis_title, 'margin': 20}},
        'xAxis': {'categories': categories},
        'plotOptions': {'column': {'minPointLength': 2},'series': {'dataLabels': {'enabled': False}}},
        'series': flights_series
    }

    return JsonResponse(chart)
