from django import forms
from store.models import Product, Category
from account.models import UserBase
from account.models import Seller
from django.db.models import Q

class SellerRegistrationForm(forms.ModelForm):    
    class Meta:
        model = Seller
        fields = ('verification_document', )

class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)

        # all fields except in stock are required
        for key in self.fields:
            self.fields[key].required = True
        
        self.fields['in_stock'].required = False

    class Meta:
        model = Product
        fields = ['title', 'category', 'image', 'image_alternate', 'price', 'in_stock']

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        r = Category.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Category already exists")
        return name