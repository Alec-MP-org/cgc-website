from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from catalog.models import FlightsheetDetails, FlightsheetHeader

class SearchFlightSheets(forms.Form):
    headers = FlightsheetHeader.objects.all()
    duty_instructors = set()
    instructors = set()
    aeis = set()
    duty_pilots = set()
    tugs = set()
    for header in headers:
        if header.duty_instructor:
            duty_instructors.add(header.duty_instructor)
        if header.instructor:
            instructors.add(header.instructor)
        if header.air_experience_instructor:
            aeis.add(header.air_experience_instructor)
        if header.duty_pilot:
            duty_pilots.add(header.duty_pilot)
        if header.tug_pilot1:
            tugs.add(header.tug_pilot1)
    duty_instructors = list(duty_instructors)
    instructors = list(instructors)
    aeis = list(aeis)
    duty_pilots = list(duty_pilots)
    tugs = list(tugs)
    duty_instructors.sort(key=str.lower)
    instructors.sort(key=str.lower)
    aeis.sort(key=str.lower)
    duty_pilots.sort(key=str.lower)
    tugs.sort(key=str.lower)
    duty_instructors.insert(0, 'All')
    instructors.insert(0, 'All')
    aeis.insert(0, 'All')
    duty_pilots.insert(0, 'All')
    tugs.insert(0, 'All')
    duty_instructors_fortuples = []
    instructors_fortuples = []
    aeis_fortuples = []
    duty_pilots_fortuples = []
    tugs_fortuples = []
    for i in duty_instructors:
        duty_instructors_fortuples.append(tuple([i, i]))
    for i in instructors:
        instructors_fortuples.append(tuple([i, i]))
    for i in aeis:
        aeis_fortuples.append(tuple([i, i]))
    for i in duty_pilots:
        duty_pilots_fortuples.append(tuple([i, i]))
    for i in tugs:
        tugs_fortuples.append(tuple([i, i]))
    duty_instructors = tuple(duty_instructors_fortuples)
    instructors = tuple(instructors_fortuples)
    aeis = tuple(aeis_fortuples)
    duty_pilots = tuple(duty_pilots_fortuples)
    tugs = tuple(tugs_fortuples)

    start_date = forms.DateField(required=False, widget=DatePickerInput(), help_text='Start of date range filter',label='Start Date')
    end_date = forms.DateField(required=False, widget=DatePickerInput(), help_text='End of date range filter', label='End Date')
    search_duty_instructor = forms.ChoiceField(required=False, choices=duty_instructors, help_text="Filter by Duty Instructor", label="Duty Instructor")
    search_instructor = forms.ChoiceField(required=False, choices=instructors, help_text="Filter by Instructor", label="Instructor")
    search_aei = forms.ChoiceField(required=False, choices=aeis, help_text="Filter by AEI", label="AEI")
    search_duty_pilot = forms.ChoiceField(required=False, choices=duty_pilots, help_text="Filter by Duty Pilot", label="Duty Pilot")
    search_tug = forms.ChoiceField(required=False, choices=tugs, help_text="Filter by Tug Pilot", label="Tug Pilot")
    resultsperpage = forms.IntegerField(initial=15, min_value=5)

    def clean_data(self):
        data = {
            "start_date": self.cleaned_data['start_date'],
            "end_date": self.cleaned_data['end_date'],
            "search_duty_instructor": self.cleaned_data['search_duty_instructor'],
            "search_instructor": self.cleaned_data['search_instructor'],
            "search_aei": self.cleaned_data['search_aei'],
            "search_duty_pilot": self.cleaned_data['search_duty_pilot'],
            "search_tug": self.cleaned_data['search_tug'],
            "resultsperpage": self.cleaned_data['resultsperpage'],
        }
        
        return data

class SearchFlights(forms.Form):
    flights = FlightsheetDetails.objects.all()
    pilot = set()
    billingcodes = set()
    gliders = set()
    for flight in flights:
        if flight.pilot1:
            pilot.add(flight.pilot1)
        if flight.pilot2:
            pilot.add(flight.pilot2)
        if flight.billing_code:
            billingcodes.add(flight.billing_code)
        if flight.glider:
            gliders.add(flight.glider)
    pilot=list(pilot)
    billingcodes=list(billingcodes)
    gliders=list(gliders)
    pilot.sort(key=str.lower)
    billingcodes.sort(key=str.lower)
    gliders.sort(key=str.lower)
    pilot.insert(0, 'All')
    billingcodes.insert(0, 'All')
    gliders.insert(0, 'All')
    pilotfortuples = []
    codesfortuples = []
    glidersfortuples = []
    for pilot in pilot:
        pilotfortuples.append(tuple([pilot, pilot]))
    for code in billingcodes:
        codesfortuples.append(tuple([code, code]))
    for glider in gliders:
        glidersfortuples.append(tuple([glider, glider]))
    pilot = tuple(pilotfortuples)
    billingcodes = tuple(codesfortuples)
    gliders = tuple(glidersfortuples)

    start_date = forms.DateField(required=False, widget=DatePickerInput(), help_text='Start of date range filter',label='Start Date')
    end_date = forms.DateField(required=False, widget=DatePickerInput(), help_text='End of date range filter', label='End Date')
    search_glider = forms.ChoiceField(required=False, choices=gliders, help_text="Filter by Glider", label="Glider")
    search_pilot = forms.ChoiceField(required=False, choices=pilot, help_text="Filter by Pilot (P1 or P2)", label="Pilot")
    search_billing_code = forms.ChoiceField(required=False, choices=billingcodes, help_text="Filter by Billing Code", label="Billing Code")
    resultsperpage = forms.IntegerField(initial=15, min_value=5)

    def clean_data(self):
        data = {
            "start_date": self.cleaned_data['start_date'],
            "end_date": self.cleaned_data['end_date'],
            "search_glider": self.cleaned_data['search_glider'],
            "search_pilot": self.cleaned_data['search_pilot'],
            "search_billing_code": self.cleaned_data['search_billing_code'],
            "resultsperpage": self.cleaned_data['resultsperpage'],
        }
        return data

class FlightStats(forms.Form):
    flights = FlightsheetDetails.objects.all()
    pilots = set()
    billingcodes = set()
    for flight in flights:
        if flight.pilot1:
            pilots.add(flight.pilot1)
        if flight.pilot2:
            pilots.add(flight.pilot2)
        if flight.billing_code:
            billingcodes.add(flight.billing_code)
    pilots=list(pilots)
    billingcodes=list(billingcodes)
    pilots.sort(key=str.lower)
    billingcodes.sort(key=str.lower)
    pilots.insert(0, 'All')
    billingcodes.insert(0, 'All')
    pilotsfortuples = []
    codesfortuples = []
    for pilot in pilots:
        pilotsfortuples.append(tuple([pilot, pilot]))
    for code in billingcodes:
        codesfortuples.append(tuple([code, code]))
    pilots = tuple(pilotsfortuples)
    billingcodes = tuple(codesfortuples)

    displaytypes = (
        ('month', 'Monthly Flight Time'),
        ('total', 'Total Flight Time'),
        ('totalcount', 'Total Flight Count'),
        ('monthcount', 'Monthly Flight Count'),
        )
    
    pilot = forms.ChoiceField(choices=pilots, required=False, label="Pilot (P1 or P2)")
    billing_code = forms.ChoiceField(choices=billingcodes, required=False, label="Billing Code")
    display_type = forms.ChoiceField(choices=displaytypes, required=False, label="Display Type")
    start_date = forms.DateField(required=False, widget=DatePickerInput(options={'format': 'YYYY-MM-DD'}), label='Start Date')
    end_date = forms.DateField(required=False, widget=DatePickerInput(options={'format': 'YYYY-MM-DD'}), label='End Date')

    def clean_data(self):
        data = {
            'pilot': self.cleaned_data['pilot'],
            'billing_code': self.cleaned_data['billing_code'],
        }
        return data
