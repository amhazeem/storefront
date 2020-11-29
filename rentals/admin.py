from django import forms
from django.contrib import admin

from rentals.models import Rental, Customer, RentalLine


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','created_at')

class InlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        book_ids = []
        errors = []
        for form in self.forms:
            book = form.cleaned_data.get('book', None)
            if not book:
                raise forms.ValidationError(
                    'Please select a valid book')
            try:
                if form.cleaned_data['quantity'] < 1:
                    raise forms.ValidationError(
                        'Quantity must be greater than 1')
                stock_quantity = book.in_stock
                if stock_quantity < form.cleaned_data['quantity']:
                    if stock_quantity == 0:
                        errors.append(f'{book.title} is out of stock')
                    else:
                        errors.append(f'{book.title} has only {stock_quantity} left')
                book_ids.append(book.pk)
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        # Used set to know if duplicates exist
        ids_set = list(set(book_ids))
        if ids_set != book_ids:
            raise forms.ValidationError(
                'Cannot have duplicate books in an order, Add to the quantity')
        if errors:
            string = ",".join([_str for _str in errors])
            raise forms.ValidationError(string)

class LineItemInline(admin.TabularInline):
    model = RentalLine
    verbose_name = "Books Rented"
    verbose_name_plural = "Books Rented"
    formset = InlineFormset
    extra = 0

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('customer','books','rented_on','amount_due')
    inlines = (LineItemInline,)

    def books(self, obj):
        books = ",".join([book.__str__() for book in obj.lines.all()])
        return books

    def rented_on(self, obj):
        return obj.created_at

    def amount_due(self, obj):
        return obj.price


