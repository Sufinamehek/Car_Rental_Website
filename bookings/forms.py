from django import forms
from datetime import datetime
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            'start_location',
            'end_location',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'total_km'
        ]

        widgets = {
            'start_location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_start_location',
                'placeholder': 'Pickup location'
            }),
            'end_location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_end_location',
                'placeholder': 'Drop location'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'total_km': forms.HiddenInput()
        }

    # Booking validation and business rules
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        start_time = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_date")
        end_time = cleaned_data.get("end_time")
        total_km = cleaned_data.get("total_km")

        # Check required values
        if not all([start_date, start_time, end_date, end_time]):
            return cleaned_data

        start_dt = datetime.combine(start_date, start_time)
        end_dt = datetime.combine(end_date, end_time)

        # Validation: Drop time must be after pickup
        if end_dt <= start_dt:
            raise forms.ValidationError(
                "Drop time must be after pickup time."
            )

        # Calculate total booking hours
        hours = (end_dt - start_dt).total_seconds() / 3600

        # Convert hours into days (minimum 1 day)
        total_days = max(1, int(hours // 24) + (1 if hours % 24 else 0))

        # Distance rule: 800 km per day allowed
        if total_km:
            allowed_km = total_days * 400
            if total_km > allowed_km:
                raise forms.ValidationError(
                    f"Maximum allowed distance is {allowed_km} km for {total_days} day(s)."
                )

        return cleaned_data
