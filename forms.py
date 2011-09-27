from django import forms
from django.forms import ModelForm, TextInput, Field
from django.forms.models import modelformset_factory #,inlineformset_factory
from django.contrib.auth.models import User
from motorfleet.models import *


class FleetForm(ModelForm):
    class Meta:
        model = Fleet


class MotorfleetProfileForm(ModelForm):
    class Meta:
        model = MotorfleetProfile


class PolicyForm(ModelForm):
    class Meta:
        model = Policy


class ClaimForm(ModelForm):
    class Meta:
        model = Claim

ClaimFormSetBase = modelformset_factory(
        Claim,
        form=ClaimForm,
        extra=5
)

class ClaimFormSet(ClaimFormSetBase):
    def add_fields(self, form, index):
        super(ClaimFormSet, self).add_fields(form, index)


class ConvictionForm(ModelForm):
    class Meta:
        model = Conviction

ConvictionFormSetBase = modelformset_factory(
        Conviction,
        form=ConvictionForm,
        extra=5
)

class ConvictionFormSet(ConvictionFormSetBase):
    def add_fields(self, form, index):
        super(ConvictionFormSet, self).add_fields(form, index)


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle

VehicleFormSetBase = modelformset_factory(
        Vehicle,
        form=VehicleForm,
        extra=1
)

class VehicleFormSet(VehicleFormSetBase):
    def add_fields(self, form, index):
        super(VehicleFormSet, self).add_fields(form, index)