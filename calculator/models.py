from django.db import models

# Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# class Budget(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)   

#     income_items = models.JSONField(default=list)
#     total_income = models.DecimalField(max_digits=10, decimal_places=2)
#     expenses = models.JSONField(default=list)
#     total_expenses = models.DecimalField(max_digits=10, decimal_places=2)
#     category_percentages = models.JSONField(default=dict)

# class IncomeItem(models.Model):
#     budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
#     source = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

# class ExpenseItem(models.Model):
#     budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
#     category = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10,   
#  decimal_places=2)


# <!DOCTYPE html>
# <html>
# <head>
#     <title>Personal Budget</title>
#     <style>
#         /* Your CSS styles here */
#     </style>
# </head>
# <body>
#     <h1>Personal Budget</h1>
#     <form method="POST">
#         {% csrf_token %}
#         <h2>Income</h2>
#         <button type="button" class="add-income-btn">Add Income Source</button>
#         <div id="income-items">
#             {% for income_source, income_amount in income_items %}
#                 <div class="income-item">
#                     <label for="income_source_{{ forloop.counter }}">Income Source:</label>
#                     <input type="text" name="income_source_{{ forloop.counter }}" value="{{ income_source }}">
#                     <label for="income_amount_{{ forloop.counter }}">Amount:</label>
#                     <input type="number" name="income_amount_{{ forloop.counter }}" value="{{ income_amount }}">
#                     <button type="button" class="remove-income-btn">Remove</button>
#                 </div>
#             {% endfor %}
#         </div>
#         <br>
#         <h2>Expenses</h2>
#         {% for category, _ in EXPENSE_CATEGORIES %}
#             <h3>{{ category }}</h3>
#             <button type="button" class="add-expense-btn">Add Expense</button>
#             <div id="{{ category }}-expenses">
#                 {% for expense_description, expense_amount in category_expenses %}
#                     <div class="expense-item">
#                         <label for="{{ category }}_description_{{ forloop.counter }}">Description:</label>
#                         <input type="text" name="{{ category }}_description_{{ forloop.counter }}" value="{{ expense_description }}">
#                         <label for="{{ category }}_amount_{{ forloop.counter }}">Amount:</label>
#                         <input type="number" name="{{ category }}_amount_{{ forloop.counter }}" value="{{ expense_amount }}">
#                         <button type="button" class="remove-expense-btn">Remove</button>
#                     </div>
#                 {% endfor %}
#             </div>
#             <br>
#         {% endfor %}
#         <br>
#         <button type="submit">Calculate</button>
#     </form>

#     {% if income_items and expenses %}
#         <h2>Budget Summary</h2>
#         <p>Total Income: {{ total_income }}</p>
#         <h3>Expenses</h3>
#         <ul>
#             {% for category, category_expenses in expenses %}
#                 <li>{{ category }}:
#                     <ul>
#                         {% for expense_description, expense_amount in category_expenses %}
#                             <li>{{ expense_description }}: {{ expense_amount }}</li>
#                         {% endfor %}
#                     </ul>
#                 </li>
#             {% endfor %}
#         </ul>
#         <p><strong>Expense Percentages:</strong></p>
#         <ul>
#             {% for category, percentage in category_percentages.items %}
#                 <li>{{ category }}: {{ percentage:.2f}}%</li>
#             {% endfor %}
#         </ul>
#         {% for message in messages %}
#             <p style="color: red;">{{ message }}</p>
#         {% endfor %}
#     {% endif %}
# </body>
# </html>