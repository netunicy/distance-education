
from django import forms

from .models import TopicsVideo, SchoolVideo


class TopicsVideoAdminForm(forms.ModelForm):

    cloudflare_upload_uid = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    class Meta:
        model = TopicsVideo
        fields = "__all__"


class VideoAdminForm(forms.ModelForm):

    cloudflare_upload_uid = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    class Meta:
        model = SchoolVideo
        fields = "__all__"
