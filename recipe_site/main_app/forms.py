from django import forms
from .models import CustomRecipe, User, Recipe 

# Renamed form to match user's code and updated fields/widgets
class RecipeForm(forms.ModelForm):
    """
    A ModelForm for creating and updating CustomRecipe instances.
    It automatically handles the unique_together constraint validation
    by checking against the user provided during instantiation.
    """
    class Meta:
        model = CustomRecipe
        # Updated fields list based on user's form
        fields = [
            'name', 'cuisine', 'description', 'ingredients',
            'instructions', 'cook_time', 'calories', 'protein',
            'fat', 'carbohydrates', 'picture'
        ]
        # Added widgets from user's form
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'ingredients': forms.Textarea(attrs={'rows': 6}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }
        # Note: 'user' field is intentionally excluded from 'fields' list.
        # It is assigned in the view/form logic.

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and expects 'user' to be passed in kwargs
        when creating or editing a CustomRecipe.
        """
        # Get the user from the view kwargs if passed, otherwise None
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Override clean() for custom validation beyond model validation.
        ModelForm already handles unique_together based on the instance's user.
        """
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        """
        Override save to assign the user before saving the instance.
        """
        # Create the instance but don't save to DB yet
        instance = super().save(commit=False)

        # Assign the user obtained during form initialization
        if self.user:
            instance.user = self.user
        elif not instance.pk:
            raise ValueError("User must be provided to save a new CustomRecipe.")

        # Now, save the instance to the database if commit=True
        if commit:
            # The unique_together constraint ('user', 'name') validation
            # happened during form.is_valid(). If that failed, we wouldn't reach here.
            # The instance.save() call might still raise an IntegrityError if
            # there's a race condition or if validation was bypassed, but the form
            # is the primary guard.
            instance.save()
            # If you have ManyToMany fields defined in the 'fields' list, save them
            self.save_m2m()

        return instance