# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlightsheetDetails(models.Model):
    flight_date = models.DateField()
    flight_number = models.IntegerField()
    glider = models.CharField(max_length=45)
    pilot1 = models.CharField(max_length=45)
    pilot2 = models.CharField(max_length=45, blank=True, null=True)
    launch_time = models.TimeField()
    landing_time = models.TimeField()
    duration_time = models.TimeField()
    height = models.IntegerField(blank=True, null=True)
    billing_code = models.CharField(max_length=45, blank=True, null=True)
    receipt_voucher = models.CharField(max_length=45, blank=True, null=True)
    gfa_number = models.CharField(max_length=45, blank=True, null=True)
    notes = models.CharField(max_length=120, blank=True, null=True)
    tow_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    glider_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pilot1_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pilot2_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cgc_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    flight_key = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.flight_key

    class Meta:
        managed = True
        db_table = 'flightsheet_details'
        ordering = ['flight_date', 'flight_number']


class FlightsheetHeader(models.Model):
    flight_date = models.DateField(primary_key=True)
    duty_instructor = models.CharField(max_length=45)
    instructor = models.CharField(max_length=45, blank=True, null=True)
    air_experience_instructor = models.CharField(max_length=45, blank=True, null=True)
    duty_pilot = models.CharField(max_length=45, blank=True, null=True)
    tug_pilot1 = models.CharField(max_length=45, blank=True, null=True)
    tug_pilot2 = models.CharField(max_length=45, blank=True, null=True)
    runway = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return str(self.flight_date)

    class Meta:
        managed = True
        db_table = 'flightsheet_header'
        ordering = ['flight_date']
