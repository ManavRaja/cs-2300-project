from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
import uuid

# Create your models here.

# Recipe Table
class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
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
        null=True, blank=True)
    cuisine = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() during save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Recipe: {self.name} Primary Key: {self.pk}'
    

# Premade_Recipe Table
class PremadeRecipe(Recipe):

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() during save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Premade Recipe: {self.name}'
    

# Custom_Recipe Table
class CustomRecipe(Recipe):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_recipes')

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() during save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Custom Recipe: {self.name} by {self.user.username}'


# Weekly_Meal_Plan Table
class WeeklyMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    start_date = models.DateField(null=False, blank=False)
    recipes = models.ManyToManyField(CustomRecipe, null=True, blank=True, related_name='meal_plans')
    
    class Meta:
        unique_together = (("user", "start_date"),)

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() during save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Weekly Meal Plan for {self.user.username} starting {self.start_date}'





























# # Premade_Recipe Table
# class PremadeRecipe(models.Model):
#     premade_recipe_id = models.OneToOneField(Recipe, 
#                                   on_delete=models.CASCADE,
#                                   primary_key=True)
    
#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f'Premade Recipe: {self.recipe_id.name} ({self.recipe_id.recipe_id})'

# # User Table
# class User(models.Model):
#     user_id = models.UUIDField(
#         primary_key=True, 
#         default=uuid.uuid4, 
#         editable=False)
#     username = models.CharField(max_length=150, unique=True, null=False, blank=False)
#     password = models.CharField(max_length=128, null=False, blank=False)
#     # NOT INCLUDING EMAIL YET; WASN'T IN ORIGINAL DESIGN
#     # email = models.EmailField(unique=True)
#     account_type = models.CharField(
#         max_length=50,
#         choices=[
#             ('personal', 'Personal'),
#             ('culinary_expert', 'Culinary Expert'),
#         ],
#         null=False,
#         blank=False)
    
#     def __str__(self):
#         return f'Username: {self.username}, Account Type: {self.account_type} ({self.user_id})'


# # Custom_Recipe Table
# class CustomRecipe(models.Model):
#     pk = models.CompositePrimaryKey('recipe_id', 'user_id')
#     recipe_id = models.OneToOneField(Recipe, 
#                                     on_delete=models.CASCADE,
#                                     null=False,
#                                     blank=False)
#     user_id = models.OneToOneField(User, 
#                                     on_delete=models.CASCADE,
#                                     null=False,
#                                     blank=False)

    
#     def __str__(self):
#         return f'Custom Recipe: {self.recipe_id.name} by {self.user_id.username} ({self.user_id.user_id})'


# # Personal_Account Table
# class PersonalAccount(models.Model):
#     user_id = models.OneToOneField(User, 
#                                     on_delete=models.CASCADE,
#                                     null=False,
#                                     blank=False,
#                                     primary_key=True)


# # NOTE: Not adding admin_acc table; will figure it out later
# # b/c django doesn't really need admin_acc table


# # Culinary_Expert Table
# class CulinaryExpert(models.Model):
#     user_id = models.OneToOneField(User, 
#                                 on_delete=models.CASCADE,
#                                 null=False,
#                                 blank=False,
#                                 primary_key=True)
#     cuisine_specialty = models.CharField(max_length=100, null=False, blank=False)
#     num_recipes_added = models.PositiveIntegerField(default=0, null=False, blank=False)

#     def __str__(self):
#         return f'Username: {self.user_id.username} Cuisine Speciality: {self.cuisine_specialty}'


# # Weekly_Meal_Plan Table
# class WeeklyMealPlan(models.Model):
#     pk = models.CompositePrimaryKey('user_id', 'start_date')
#     user_id = models.OneToOneField(User, 
#                                  on_delete=models.CASCADE,
#                                  null=False,
#                                  blank=False)
#     start_date = models.DateField(null=False, blank=False)

#     # recipe1_id = models.ForeignKey(PremadeRecipe,
#     #                                on_delete=models.CASCADE,
#     #                                null=True,
#     #                                blank=True)

#     def __str__(self):
#         return f'Weekly Meal Plan for {self.user_id.username} starting {self.start_date}'


# # Weekly_Meal_Plan_Recipe Table
# class WeeklyMealPlanRecipe(models.Model):
#     pk = models.CompositePrimaryKey('meal_plan_id', 'recipe_id')
#     meal_plan_id = models.OneToOneField(WeeklyMealPlan, 
#                                       on_delete=models.CASCADE,
#                                       null=False,
#                                       blank=False)
#     recipe_id = models.OneToOneField(PremadeRecipe, 
#                                   on_delete=models.CASCADE,
#                                   null=False,
#                                   blank=False)
#     recipe_number = models.PositiveIntegerField(
#                                 null=False,
#                                 blank=False,
#                                 validators=[MinValueValidator(1)])

#     def __str__(self):
#         return f'Meal Plan ID: {self.meal_plan_id} Recipe ID: {self.recipe_id}'
    






















# Manav's code below

# from django.db import models
# from django.core.validators import MinValueValidator

# import uuid
# from django.db import models

# # Import Django's built-in User model
# from django.contrib.auth.models import User

# # Import ArrayField if using PostgreSQL
# # from django.contrib.postgres.fields import ArrayField
# # from django.core.validators import MinValueValidator
# # from django.core.exceptions import ValidationError

# # --- User Profile Models (Extending the built-in User) ---
# # These models use OneToOneField to add extra information to the built-in User model.


# class PersonalAcc(models.Model):
#     """
#     Profile details for a personal user account. Links one-to-one with the built-in User.
#     """

#     # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # Using settings.AUTH_USER_MODEL is best practice for reusable apps,
#     # but importing User directly works fine for project-specific models.
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     personal_acc_username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='username')
#     personal_acc_password = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password')
#     account_type = models.CharField(
#         max_length=50,
#         choices=[
#             ('personal', 'Personal'),
#             ('culinary_expert', 'Culinary Expert'),
#         ],
#         null=False,
#         blank=False
#         )

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Personal Account for {self.user_id.username}"
    

# class CulinaryExpert(models.Model):
#     """
#     Profile details for a culinary expert user account. Links one-to-one with the built-in User.
#     """

#     user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     cuisine_specialty = models.CharField(max_length=100, null=False, blank=False)
#     num_recipes_added = models.PositiveIntegerField(default=0, null=False, blank=False)

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Culinary Expert: {self.user_id.username}, Specialty: {self.cuisine_specialty}"


# # --- Recipe Models ---

# class Recipe(models.Model):
#     """
#     Represents a recipe with instructions, ingredients, and nutritional info.
#     """

#     recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, null=False, blank=False)
#     description = models.CharField(max_length=500, null=False, blank=False)
#     # NOT RIGHT NOW Use ArrayField for PostgreSQL. For other DBs, consider JSONField or separate model
#     instructions = models.TextField(null=True, blank=True)
#     picture = models.ImageField(upload_to='recipes/', null=True, blank=True)
#     protein = models.PositiveSmallIntegerField(null=True, blank=True)  # CHECK >= 0 handled
#     calories = models.PositiveSmallIntegerField(null=True, blank=True)  # CHECK >= 0 handled
#     fat = models.PositiveSmallIntegerField(null=True, blank=True)  # CHECK >= 0 handled
#     carbohydrates = models.PositiveSmallIntegerField(null=True, blank=True)  # CHECK >= 0 handled
#     # Use ArrayField for PostgreSQL. NOT USING IT RIGHT NOW
#     # ingredients = ArrayField(
#     #     models.CharField(max_length=100),
#     #     null=False,
#     #     blank=False,
#     #     # TODO: The CHECK (ingredients > 0) constraint (array not empty) needs custom validation
#     # )
#     ingredients = models.TextField(null=True, blank=True)
#     cook_time = models.FloatField(
#             validators=[MinValueValidator(0.0)],
#             null=True, blank=True)
#     cuisine = models.CharField(max_length=100, null=True, blank=True)
#     # NOTE: `is_custom` WAS NOT in original relational schema
#     is_custom = models.BooleanField(default=True)

#     # dont know what this does yet, so not including it
#     # # TODO: Rewrite validation outside of SQL
#     # def clean(self):
#     #     # Custom validation for non-empty ingredients array
#     #     super().clean()
#     #     if not self.ingredients:  # Check if the list is empty
#     #         raise ValidationError({"ingredients": "Ingredients list cannot be empty."})
#     #     # You could add more validation here if needed

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.name} ({self.recipe_id})'


# class PremadeRecipe(models.Model):
#     """
#     Identifies a Recipe as being 'premade'. Links one-to-one with Recipe.
#     """

#     premade_recipe_id = models.OneToOneField(Recipe, on_delete=models.CASCADE, primary_key=True)

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Premade: {self.premade_recipe_id.name}"


# class CustomRecipe(models.Model):
#     """
#     Links a User (built-in) to a Recipe they have customized or created.
#     Uses unique_together to simulate the composite primary key (user_id, recipe_id).
#     """

#     # custom_recipe_pk = models.UUIDField(
#     #     primary_key=True, default=uuid.uuid4, editable=False
#     # )
#     class Meta:
#         unique_together = (("user_id", "custom_recipe_id"),)

#     # Now points to built-in User
#     user_id = models.OneToOneField(User, 
#                                 on_delete=models.CASCADE)  
#     custom_recipe_id = models.OneToOneField(Recipe, 
#                                   on_delete=models.CASCADE,
#                                   null=False,
#                                   blank=False)

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Custom recipe '{self.custom_recipe_id.name}' by {self.user_id.username}"


# class WeeklyMealPlan(models.Model):
#     """
#     Represents a user's (built-in User) meal plan for a week starting on a specific date.
#     Uses ManyToManyField for recipes.
#     Uses unique_together for (user, start_date) to allow multiple plans per user.
#     """
#     class Meta:
#         unique_together = (("user_id", "start_date"),)

#     # meal_plan_id = models.UUIDField(
#     #     primary_key=True, default=uuid.uuid4, editable=False
#     # )

#     user_id = models.OneToOneField(
#         User, on_delete=models.CASCADE
#     )  # Now points to built-in User
#     start_date = models.DateField(null=False, blank=False)

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Meal Plan for {self.user_id.username} starting {self.start_date}"


# class WeeklyMealPlanRecipe(models.Model):
#     """
#     Represents a recipe in a user's meal plan. Uses ManyToManyField for recipes.
#     """

#     # weekly_meal_plan_recipe_id = models.UUIDField(
#     #     primary_key=True, default=uuid.uuid4, editable=False
#     # )

#     meal_plan_id = models.OneToOneField(WeeklyMealPlan, on_delete=models.CASCADE)
#     recipe_id = models.OneToOneField(PremadeRecipe, on_delete=models.CASCADE)
#     recipe_number = models.PositiveIntegerField(
#         null=False,
#         blank=False,
#         validators=[MinValueValidator(1)]
#     )

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Call clean() during save
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Recipe {self.recipe_id} in Meal Plan {self.meal_plan_id}"