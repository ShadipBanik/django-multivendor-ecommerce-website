
from django import forms
from ..models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [ "rating", "review"]
        widgets = {
            "rating": forms.HiddenInput(),  # hide rating input
            "review": forms.Textarea(attrs={ "class":"comment-input comment-textarea", "placeholder": "Write your review..."}),
        }