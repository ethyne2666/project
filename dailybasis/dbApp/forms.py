
from django import forms
from datetime import timedelta

TIME_SLOTS = [
    ('9:00-12:00', '9:00 AM - 12:00 PM'),
    ('18:00-21:00', '6:00 PM - 9:00 PM'),
]

class ScheduleForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    delivery_time = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            # Rule 1: End date cannot be earlier than start date
            if end_date < start_date:
                self.add_error("end_date", "End date cannot be earlier than start date.")

            # Rule 2: End date cannot exceed 1 year from start date
            if end_date > start_date + timedelta(days=365):
                self.add_error("end_date", "End date cannot be more than 1 year from start date.")

        return cleaned_data