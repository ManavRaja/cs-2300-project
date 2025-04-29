from django.db import models
from django.core.validators import MinValueValidator
import uuid

# Create your models here.


class Recipe(models.Model):
    recipe_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='recipes/', null=True, blank=True)
    protein = models.PositiveIntegerField(null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    fat = models.PositiveIntegerField(null=True, blank=True)
    carbohydrates = models.PositiveIntegerField(null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    cook_time = models.FloatField(
        validators=[MinValueValidator(0.0)],
        null=True, blank=True
        )
    cuisine = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.recipe_id})'



    

# from django.db import models

# # Create your models here.
# # models.py

# import uuid
# from django.db import models

# # Import Django's built-in User model
# from django.contrib.auth.models import User

# # Import ArrayField if using PostgreSQL
# from django.contrib.postgres.fields import ArrayField
# from django.core.validators import MinValueValidator
# from django.core.exceptions import ValidationError

# # --- User Profile Models (Extending the built-in User) ---
# # These models use OneToOneField to add extra information to the built-in User model.


# class PersonalAcc(models.Model):
#     """
#     Profile details for a personal user account. Links one-to-one with the built-in User.
#     """

#     # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # Using settings.AUTH_USER_MODEL is best practice for reusable apps,
#     # but importing User directly works fine for project-specific models.
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # Add any other personal account specific fields here if needed
#     # Example: date_of_birth = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"Personal Account for {self.user.username}"


# # --- Recipe Models ---

# class Recipe(models.Model):
#     """
#     Represents a recipe with instructions, ingredients, and nutritional info.
#     """

#     recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, null=False, blank=False)
#     description = models.CharField(max_length=500, null=False, blank=False)
#     # Use ArrayField for PostgreSQL. For other DBs, consider JSONField or separate model
#     instructions = ArrayField(models.TextField(), null=False, blank=False)
#     picture = models.TextField(null=True, blank=True)  # TEXT allows NULL
#     protein = models.PositiveSmallIntegerField(null=False)  # CHECK >= 0 handled
#     calories = models.PositiveSmallIntegerField(null=False)  # CHECK >= 0 handled
#     fat = models.PositiveSmallIntegerField(null=False)  # CHECK >= 0 handled
#     carbohydrates = models.PositiveSmallIntegerField(null=False)  # CHECK >= 0 handled
#     # Use ArrayField for PostgreSQL.
#     ingredients = ArrayField(
#         models.CharField(max_length=100),
#         null=False,
#         blank=False,
#         # TODO: The CHECK (ingredients > 0) constraint (array not empty) needs custom validation
#     )
#     cook_time = models.FloatField(
#         null=False,
#         validators=[MinValueValidator(0.00001)],  # Enforces CHECK (cook_time > 0)
#     )
#     cuisine = models.CharField(max_length=50, null=False, blank=False)

#     # TODO: Rewrite validation outside of SQL
#     def clean(self):
#         # Custom validation for non-empty ingredients array
#         super().clean()
#         if not self.ingredients:  # Check if the list is empty
#             raise ValidationError({"ingredients": "Ingredients list cannot be empty."})
#         # You could add more validation here if needed

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name


# class PremadeRecipe(models.Model):
#     """
#     Identifies a Recipe as being 'premade'. Links one-to-one with Recipe.
#     """

#     recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, primary_key=True)

#     def __str__(self):
#         return f"Premade: {self.recipe.name}"


# class CustomRecipe(models.Model):
#     """
#     Links a User (built-in) to a Recipe they have customized or created.
#     Uses unique_together to simulate the composite primary key (user_id, recipe_id).
#     """

#     custom_recipe_pk = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE
#     )  # Now points to built-in User
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("user", "recipe")

#     def __str__(self):
#         return f"Custom recipe '{self.recipe.name}' by {self.user.username}"


# # --- Meal Plan Model ---


# class WeeklyMealPlan(models.Model):
#     """
#     Represents a user's (built-in User) meal plan for a week starting on a specific date.
#     Uses ManyToManyField for recipes.
#     Uses unique_together for (user, start_date) to allow multiple plans per user.
#     """

#     meal_plan_id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE
#     )  # Now points to built-in User
#     start_date = models.DateField(null=False)
#     # ManyToManyField is the standard way to represent a list of related objects.
#     # The size constraint [21] needs to be enforced in application logic (forms/views/save method).
#     recipes = models.ManyToManyField(Recipe, related_name="weekly_meal_plans")

#     class Meta:
#         unique_together = ("user", "start_date")
#         ordering = ["user", "start_date"]

#     def __str__(self):
#         return f"Meal Plan for {self.user.username} starting {self.start_date}"
