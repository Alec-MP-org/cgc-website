from rest_framework import serializers
from catalog.models import FlightsheetDetails, FlightsheetHeader


class FlightsheetDetailsSerializer(serializers.Serializer):
    flight_date = serializers.DateField()
    flight_number = serializers.IntegerField()
    glider = serializers.CharField(max_length=45)
    pilot1 = serializers.CharField(max_length=45)
    pilot2 = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    launch_time = serializers.TimeField()
    landing_time = serializers.TimeField()
    duration_time = serializers.TimeField()
    height = serializers.IntegerField(required=False, allow_null=True)
    billing_code = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    receipt_voucher = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    gfa_number = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    notes = serializers.CharField(max_length=120, required=False, allow_null=True, allow_blank=True)
    tow_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    glider_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    pilot1_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    pilot2_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    cgc_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    flight_key = serializers.CharField(max_length=16)
    def create(self, validated_data):
        """
        Create and return a new `FlightsheetDetails` instance, given the validated data.
        """
        return FlightsheetDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `FlightsheetDetails` instance, given the validated data.
        """
        instance.flight_date = validated_data.get('flight_date', instance.flight_date)
        instance.flight_number = validated_data.get('flight_number', instance.flight_number)
        instance.glider = validated_data.get('glider', instance.glider)
        instance.pilot1 = validated_data.get('pilot1', instance.pilot1)
        instance.pilot2 = validated_data.get('pilot2', instance.pilot2)
        instance.launch_time = validated_data.get('launch_time', instance.launch_time)
        instance.landing_time = validated_data.get('landing_time', instance.landing_time)
        instance.duration_time = validated_data.get('duration_time', instance.duration_time)
        instance.height = validated_data.get('height', instance.height)
        instance.billing_code = validated_data.get('billing_code', instance.billing_code)
        instance.receipt_voucher = validated_data.get('receipt_voucher', instance.receipt_voucher)
        instance.gfa_number = validated_data.get('gfa_number', instance.gfa_number)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.tow_cost = validated_data.get('tow_cost', instance.tow_cost)
        instance.glider_cost = validated_data.get('glider_cost', instance.glider_cost)
        instance.pilot1_cost = validated_data.get('pilot1_cost', instance.pilot1_cost)
        instance.pilot2_cost = validated_data.get('pilot2_cost', instance.pilot2_cost)
        instance.cgc_cost = validated_data.get('cgc_cost', instance.cgc_cost)
        instance.flight_key = validated_data.get('flight_key', instance.flight_key)
        instance.save()
        return instance
'''
    class meta:
        model = FlightsheetDetails
        fields = ['flight_date', 'glider', 'pilot1', 'pilot2', 'launch_time', 'landing_time', 'duration_time', 'height', 'billing_code',
        'receipt_voucher', 'gfa_number', 'notes', 'tow_cost', 'glider_cost', 'pilot1_cost', 'pilot2_cost', 'cgc_cost', 'flight_key']

'''

class FlightsheetHeaderSerializer(serializers.Serializer):
    flight_date = serializers.DateField()
    duty_instructor = serializers.CharField(max_length=45)
    instructor = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    air_experience_instructor = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    duty_pilot = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    tug_pilot1 = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    tug_pilot2 = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)
    runway = serializers.CharField(max_length=45, required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `FlightsheetHeader` instance, given the validated data.
        """
        return FlightsheetHeader.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `FlightsheetHeader` instance, given the validated data.
        """
        instance.flight_date = validated_data.get('flight_date', instance.flight_date)
        instance.duty_instructor = validated_data.get('duty_instructor', instance.duty_instructor)
        instance.instructor = validated_data.get('instructor', instance.instructor)
        instance.air_experience_instructor = validated_data.get('air_experience_instructor', instance.air_experience_instructor)
        instance.duty_pilot = validated_data.get('duty_pilot', instance.duty_pilot)
        instance.tug_pilot1 = validated_data.get('tug_pilot1', instance.tug_pilot1)
        instance.tug_pilot2 = validated_data.get('tug_pilot2', instance.tug_pilot2)
        instance.runway = validated_data.get('runway', instance.runway)
        instance.save()
        return instance

'''
    class meta:
        model = FlightsheetHeader
        fields = ['flight_date', 'duty_instructor', 'air_experience_instructor', 'duty_pilot', 'tug_pilot1', 'tug_pilot2', 'runway']
'''