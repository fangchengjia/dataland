from django import forms


class UploadFileForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    photo = forms.FileField()
    lat = forms.CharField()
    lon = forms.CharField()
