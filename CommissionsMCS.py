#monte carlo simulation to estimate money for comission sales
#comission rate is based on percent to target
#Modified from https://pbpython.com/monte-carlo.html

import pandas as pd
import numpy as np
#import seaborn as sns
#sns.set_style('whitegrid')

class CommissionsMCS:
  #defaults
  num_reps=300 #employees that have a commission
  num_simulations=500

  #percent to target distribution: normal distribution with a mean of 100% and standard deviation of 10% 
  avg=1
  std_dev=0.1
  #historical sales target distribution: right skewewd
  #setting lower probabilities to higher targets
  sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
  sales_target_prob = [.3, .3, .2, .1, .05, .05]


  def setRepsAndSimulations(self, num_reps, num_simulations):
    self.num_reps=500
    self.num_simulations=num_simulations

  #returns a df with the spec num of reps containing the calculated commision amounts
  def createReps(self):
    #generating values from distributions
    pct_to_target=np.random.normal(self.avg,self.std_dev,self.num_reps).round(2)
    sales_target = np.random.choice(self.sales_target_values, self.num_reps, p=self.sales_target_prob)

    #dataframe
    df = pd.DataFrame(index=range(self.num_reps), data={'Pct_To_Target': pct_to_target,'Sales_Target': sales_target})
    df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']
    #calculating commision rate adn amount columns
    df['Commission_Rate'] = df['Pct_To_Target'].apply(CommissionsMCS.calc_commission_rate)
    df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']

    return df
  
  def calc_commission_rate( x):
    #return predef commision rates: 0-90%=2%, 91-99%=3%, >=100%=4%
    if x<=0.9:
      return 0.02
    if x<=0.99:
      return 0.03
    else:
      return 0.04


  def run_simulations(self):
    # Define a list to keep all the results from each simulation that we want to analyze
    all_stats = []

    # Loop through many simulations
    for i in range(self.num_simulations):
      # track sales,commission amounts and sales targets over all the simulations
      df=self.createReps()
      all_stats.append([df['Sales'].sum().round(0),df['Commission_Amount'].sum().round(0), df['Sales_Target'].sum().round(0)])

    results_df = pd.DataFrame.from_records(all_stats, columns=['Sales','Commission_Amount', 'Sales_Target'])

    print(results_df.describe())


        
  
