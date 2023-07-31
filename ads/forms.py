from .models import Ad, Make, Car
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from .humanize import natural_size


class AdForm(forms.ModelForm):
    """Main form for adding info about ads."""

    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = natural_size(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.ImageField(
        required=False,
        label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Ad
        fields = [
            'country', 'city',
            'price', 'price_per',
            'text', 'tags', 'picture'
        ]

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            err_msg = "File must be < " + self.max_upload_limit_text + " bytes"
            self.add_error('picture', err_msg)

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        ad = super(AdForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        img_file = ad.picture  # Make a copy
        # Extract data from the form to the model
        if isinstance(img_file,
                      InMemoryUploadedFile):
            byte_arr = img_file.read()
            ad.content_type = img_file.content_type
            ad.picture = byte_arr  # Overwrite with the actual image data

        if commit:
            ad.save()
            self.save_m2m()

        return ad


class MakeForm(forms.ModelForm):
    """Car make form."""

    class Meta:
        model = Make
        fields = 'name',


class CarForm(forms.ModelForm):
    """Car form for adding info about car owner."""

    class Meta:
        model = Car
        fields = [
            'model_name',
            'transmission',
            'passenger_numbers',
            'year',
            'hp'
        ]
        labels = {
            'model_name': 'name of the car model',
            'passenger_numbers': 'maximum number of passengers in the car',
            'year': 'year of the car',
            'hp': 'horse powers'
        }


class CommentForm(forms.Form):
    """Form for adding comments to an ads."""

    comment = forms.CharField(
        required=True,
        max_length=500,
        min_length=3,
        strip=True
    )
