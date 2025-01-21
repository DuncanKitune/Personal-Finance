from django.db import models
# Create your models here.

import json


class Simulation(models.Model):  # using a common super-type Simulation name rather then Cow Simulation/ Chicken Simulation to be cleaner
    SIMULATION_TYPES = [
          ('herd', 'Cow Herd'), #used when requesting to generate data. Used with name. ex request.POST.get("simulation_type", None); can retrieve values from
         ('chicken', 'Chicken Farm'),
         ('goat', 'Goat Farm'),
      ]

    simulation_type = models.CharField(max_length=10, choices=SIMULATION_TYPES) # which application model the view represents for specific types. Makes easy way to filter data output on different tabs using views with request for simulation model parameters type
    initial_count = models.IntegerField(default=10)  # Changed name
    simulation_months = models.IntegerField(default=60)  #Changed to general param
    average_per_cycle = models.IntegerField(default=2)  # Common param. Some might have specific egg and birth rates for respective types for models.  Using `average_per_cycle` to set proper value that corresponds to a new generated count for the cycle for all the simulations to reduce code overlap
    simulation_results = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
# 1. cow simulator model logic with single generic simulate function
    def simulate(self):

        if self.simulation_type == "herd":
          return self._simulate_herd()
        if self.simulation_type =="chicken":
              return self._simulate_chickens();
        if self.simulation_type == "goat":
             return self._simulate_goats();


    def _simulate_herd(self):
          # Constants
            pregnancy_months = 9
            lactation_months = 14

            # Initial state
            mothers = self.initial_count
            young = 0
            total_cows = mothers
            results = {0: {"mothers": mothers, "young": young, "total": total_cows, "births":0 }}
            mothers_pregnancy_timer = {}
            young_pregnancy_timer ={}
        
            for i in range(1, self.simulation_months + 1):
           
                #Update pregnancy status
                births = 0
                 #Check for mothers giving birth
                mothers_to_birth= []
                for key, value in mothers_pregnancy_timer.items():
                    if value + pregnancy_months == i:
                          mothers_to_birth.append(key)
                          births +=1
                for item in mothers_to_birth:
                     del mothers_pregnancy_timer[item]

                young_to_birth = []
                for key, value in young_pregnancy_timer.items():
                       if value + pregnancy_months ==i:
                          young_to_birth.append(key)
                          births +=1
                for item in young_to_birth:
                     del young_pregnancy_timer[item]


                  #New pregnancies for mothers
                for j in range (1, mothers+1):
                    if (i-1)%23 == 0 :
                        mothers_pregnancy_timer[j] = i-1


                # Check for young cows to start becoming mothers
                new_mothers = 0
                for j in range(1, young+1):
                    if (i-33) == 0 and (i-33)> 0:
                          new_mothers +=1

                #New pregnancies for young cows
                for j in range (1, young+1):
                   if (i-33)%23 == 0 and (i-33) >= 0:
                       young_pregnancy_timer[j] = i-1


                  # Update herd counts
                mothers += new_mothers
                young += births
                total_cows = mothers + young

                #Save results
                results[i] = {"mothers": mothers, "young": young, "total": total_cows, "births": births}
            self.simulation_results= results
            self.save();
        
# 2.  Chicken Simulator with shared logic across with one class Simulation using a dispatch

    def _simulate_chickens(self):
                # Constants
              laying_days = 20
              incubation_days = 21
              nursing_months = 2
              maturity_months = 6
              month_in_days= 30.42
        
            # initial_state
              laying_mothers = self.initial_count;
              matured_hens =0
              chicks = 0

              results = {0: {"laying": laying_mothers,"mature": matured_hens,"chicks": chicks, 'new_laying': 0}}

              chick_timer ={}
             
             # Track for laying hens
              laying_timers = {}
              for j in range (1, laying_mothers+1):
                   laying_timers[j] = 0
         

              for month in range(1,self.simulation_months + 1):
                  days_passed=month*month_in_days

                  laying = 0;
                  matured = 0;
                  hatch = 0


             #New mature chicks, which increases mothers
                  matures = [];
                  for k,v in chick_timer.items():
                    if v<= days_passed:
                          matures.append(k);
                  for item in matures:
                        del chick_timer[item];

                  matured_hens += len(matures);


                #laying cycle check
                  new_laying = 0
                  laying_to_birth = {}
                  for k,v in laying_timers.items():
                      if v >= days_passed-laying_days - incubation_days-nursing_months*month_in_days: #if enough time has passed, allow the chick to give birth again
                            if (days_passed >v +laying_days + incubation_days):
                                laying += 1;
                                laying_to_birth[k]=days_passed
                                new_laying += self.average_per_cycle # get egg number of chicks as average cycle
                  for item, value in laying_to_birth.items():
                        laying_timers[item]= value;

                  hatch = int(new_laying)

              #new hatch adds as new immature chicks. They are added once and won't repeat to ensure that future chicks
              #won't create more chicks.  New chick time before maturity tracked by chicks array with unique ID.
                  chicks += hatch;
                  for i in range(1,hatch+1):
                      chick_timer[len(chick_timer) + 1] =  days_passed + month_in_days * maturity_months;

              #record at the end
                  results[month] = {"laying": matured_hens + laying_mothers, "mature": matured_hens, "chicks": chicks, 'new_laying': new_laying}
                  self.simulation_results = results
                  self.save()
            # self.simulation_results = results;
            # self.save();

#3.  Goat Simulator code logic. With single shared logic with main Simulate logic method

    def _simulate_goats(self):
              # Constants
            pregnancy_days = 155
            lactation_months = 8
            maturity_months = 15
            month_in_days= 30.42

         #Initial state
            mothers = self.initial_count
            kids= 0;

            results = {0: {"mothers": mothers,"kids": kids,"new_kids":0}}
        
           
            pregnancy_timers = {}
             
            for j in range(1, mothers+1):
               pregnancy_timers[j] = 0;
           
            kid_timer={}

            for month in range(1,self.simulation_months+1):
                days_passed = month*month_in_days
               
                new_births = 0
                new_matures=[]
                for key,value in kid_timer.items():
                    if value<= days_passed:
                         new_matures.append(key);
                  
                for key in new_matures:
                      del kid_timer[key];


                mothers +=len(new_matures);


                  #check existing mature doe for new birts
                new_birthing = {}
                  
                for k,v in pregnancy_timers.items():
                       if v <= days_passed :
                           new_birthing[k]= days_passed;
                           new_births+=self.average_per_cycle


                for key,value in new_birthing.items():
                   pregnancy_timers[key] = value;

        
                for i in range (1,new_births+1):
                    kid_timer[len(kid_timer)+1] = days_passed + (month_in_days *maturity_months);
                kids+= new_births

           
                results[month] = {"mothers": mothers, "kids":kids,"new_kids": new_births};

            self.simulation_results = results;
            self.save();

class GoatSimulation(models.Model):
    initial_goats = models.IntegerField(default=10)  # Initial number of does (female goats)
    simulation_months = models.IntegerField(default=60) # time frame of simulation
    average_kids_per_birth = models.IntegerField(default=2)
    simulation_results = models.JSONField(default=dict) # tracks population through all periods
    created_at = models.DateTimeField(auto_now_add=True)

    def simulate_goats(self):
          # Constants
        pregnancy_days = 155
        lactation_months = 8
        maturity_months = 15
        month_in_days= 30.42
        
        #Initial state
        mothers = self.initial_goats # tracking current and mature goats ready for births. They are all goats capable of getting pregnant.
        kids= 0 # new goat at start

        results = {0: {"mothers": mothers,"kids": kids,"new_kids":0}}

        pregnancy_timers = {}# how much time a mom is preg
        
        for j in range(1, mothers+1):
            pregnancy_timers[j] = 0;
        kid_timer={}# track kids timer

        for month in range(1,self.simulation_months+1):

              days_passed = month*month_in_days
              #record at start
              new_births = 0

            #  Check new kid to maturity. New ones must also start their timer for mating as new mother.
              new_matures=[]
              for key,value in kid_timer.items():
                 if value<= days_passed:
                        new_matures.append(key);

              for key in new_matures:
                   del kid_timer[key]


              mothers +=len(new_matures);# Add all the new ones as they reach maturity

             #check existing mature doe for new birts
              new_birthing = {}

              for k,v in pregnancy_timers.items():
                   if v <= (days_passed):
                     new_birthing[k]= days_passed;
                     new_births+=self.average_kids_per_birth

              for key,value in new_birthing.items():
                    pregnancy_timers[key] = value;
               
            # Create and initialize new birthing to start timer in kid timer as the first birth to mature for that time
              for i in range (1,new_births+1):
                 kid_timer[len(kid_timer)+1] = days_passed + (month_in_days *maturity_months);
              kids+= new_births


              results[month] = {"mothers": mothers, "kids":kids,"new_kids": new_births};
        self.simulation_results=results;
        self.save();

class ChickenSimulation(models.Model):
    initial_chickens = models.IntegerField(default=20)
    simulation_months = models.IntegerField(default=12)
    average_eggs_per_laying = models.IntegerField(default=10)  # Average number of chicks hatching per laying cycle
    simulation_results = models.JSONField(default=dict)  # Store the simulation data

    created_at = models.DateTimeField(auto_now_add=True)

    def simulate_chickens(self):
        # Constants
        laying_days = 20
        incubation_days = 21
        nursing_months = 2
        maturity_months = 6
        month_in_days= 30.42
        
        # initial_state
        laying_mothers = self.initial_chickens
        matured_hens =0
        chicks = 0

        results = {0: {"laying": laying_mothers,"mature": matured_hens,"chicks": chicks, 'new_laying': 0}}
        
        chick_timer ={}  # how much time until chick can start laying again

        laying_timers = {}# Tracks each laying hen for lay cycles
        for j in range (1, laying_mothers+1):
             laying_timers[j] = 0; # at start no time passes to new chick can give birth
      

        for month in range(1,self.simulation_months + 1):
            days_passed=month*month_in_days
           
            laying = 0;
            matured = 0;
            hatch = 0

           
           #New mature chicks, which increases mothers
            matures = [];
            for k,v in chick_timer.items():
               if v<= days_passed:
                    matures.append(k);
            for item in matures:
                  del chick_timer[item];

            matured_hens += len(matures);
          

           #laying cycle check
            new_laying = 0
            laying_to_birth = {}
            for k,v in laying_timers.items():
                if v >= days_passed-laying_days - incubation_days-nursing_months*month_in_days: #if enough time has passed, allow the chick to give birth again
                 if (days_passed >v +laying_days + incubation_days): #check that laying timer must be older then period + incubating
                       laying += 1;
                       laying_to_birth[k]=days_passed #set a new birth day
                       new_laying += self.average_eggs_per_laying

            for item, value in laying_to_birth.items():
                   laying_timers[item]= value
        
            hatch = int(new_laying)
            #new hatch adds as new immature chicks. They are added once and won't repeat to ensure that future chicks
            #won't create more chicks.  New chick time before maturity tracked by chicks array with unique ID.
            chicks += hatch
            for i in range(1,hatch+1):
                  chick_timer[len(chick_timer) + 1] =  days_passed + month_in_days * maturity_months 


            #record at the end
            results[month] = {"laying": matured_hens + laying_mothers, "mature": matured_hens, "chicks": chicks, 'new_laying': new_laying}

        self.simulation_results = results
        self.save()

class HerdSimulation(models.Model):
    initial_mothers = models.IntegerField(default=10)
    simulation_months = models.IntegerField(default=120)
    simulation_results = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def simulate_herd(self):
         # Constants
        pregnancy_months = 9
        lactation_months = 14

        # Initial state
        mothers = self.initial_mothers
        young = 0
        total_cows = mothers
        results = {0: {"mothers": mothers, "young": young, "total": total_cows, "births":0 }}
        mothers_pregnancy_timer = {}
        young_pregnancy_timer ={}
        
        for i in range(1, self.simulation_months + 1):
           
            #Update pregnancy status
            births = 0
            #Check for mothers giving birth
            mothers_to_birth= []
            for key, value in mothers_pregnancy_timer.items():
                if value + pregnancy_months == i:
                     mothers_to_birth.append(key)
                     births +=1
            for item in mothers_to_birth:
               del mothers_pregnancy_timer[item]

            young_to_birth = []
            for key, value in young_pregnancy_timer.items():
                  if value + pregnancy_months ==i:
                      young_to_birth.append(key)
                      births +=1
            for item in young_to_birth:
                  del young_pregnancy_timer[item]


            #New pregnancies for mothers
            for j in range (1, mothers+1):
                if (i-1)%23 == 0 :
                   mothers_pregnancy_timer[j] = i-1


             # Check for young cows to start becoming mothers
            new_mothers = 0
            for j in range(1, young+1):
                  if (i-33) == 0 and (i-33)> 0:
                      new_mothers +=1

            #New pregnancies for young cows
            for j in range (1, young+1):
                if (i-33)%23 == 0 and (i-33) >= 0:
                  young_pregnancy_timer[j] = i-1


           # Update herd counts
            mothers += new_mothers
            young += births
            total_cows = mothers + young

            #Save results
            results[i] = {"mothers": mothers, "young": young, "total": total_cows, "births": births}


        self.simulation_results = results
        self.save()
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