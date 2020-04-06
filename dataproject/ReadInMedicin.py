
#Packages
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# Directory
import os

assert os.path.isdir('data/')
assert os.path.isfile('data/medicinpriser_2.xlsx')

os.listdir('data/')

############################################################
# Read in of datasets
############################################################
# Load data
filename    = 'data/medicinpriser_2.xlsx'       
filename2   = 'data/substitutiongroups.csv'    
prices      = pd.read_excel(filename)
groups      = pd.read_csv(filename2, names=['Varenummer','Substitution'])

# Merge to group medicine by substitutiongroups
medicine = pd.merge(prices,groups,on='Varenummer',how='left')

# Rearrange order
Substitution = medicine['Substitution']
medicine.drop(labels=['Substitution'], axis=1,inplace = True)
medicine.insert(3, 'Substitution', Substitution)

############################################################
# Data cleaning and structuring
############################################################

# Add prefix to date variables (date variables begins after the first 9) (useful for wide to long)
new_names = [(i,'Pris'+str(i)) for i in medicine.iloc[:, 9:].columns.values]
medicine.rename(columns = dict(new_names), inplace=True)
medicine
# Keep only Ibruprofen, Paracetamol and Aspirin 
pain = medicine.ATC.str.contains('N02BE01') # Mark observations were ATC = N02BE01 (Paracetamol)
pain |= medicine.ATC.str.contains('M01AE01') # Mark observations were ATC = M01AE01 (Ibuprofen)

medicine.loc[pain, :]
medicine = medicine.loc[pain == True] # Set medicin equal to painkillers / Drop everything else

# Keep only tablets 
tablet = medicine.Form.str.contains('suppositorier') 
tablet |= medicine.Form.str.contains('infusionsvæske, opløsning') 
medicine.loc[tablet, :]
medicine = medicine.loc[tablet == False] # Keep only tablets

# Keep only register price per daily dose - AUP_pr_DDD 
aup_ddd = medicine.Indikator.str.contains('AUP_pr_DDD') 
medicine.loc[aup_ddd, :]
medicine = medicine.loc[aup_ddd == True] # Keep only price per daily dose

# Inspection (Run each line of code individually)
medicine
medicine['ATC'].value_counts()
medicine['Lægemiddel'].value_counts()
medicine['Form'].value_counts()
medicine['Substitution'].value_counts()
medicine['Pakning'].value_counts()
medicine['Styrke'].value_counts()
medicine['Firma'].value_counts()
medicine['Indikator'].value_counts()

# Wide to long format
medicine_l = pd.wide_to_long(medicine, stubnames='Pris', i='Varenummer', j='Dato')
medicine_l = medicine_l.reset_index()
medicine_l = medicine_l.sort_values(['Varenummer','Dato'])

# Drop missing
medicine_l = medicine_l.dropna(subset=['Pris'])
medicine_l.Pris.isnull().mean()

# Relative change in prices
medicine_l['pct_change'] = medicine_l.groupby(['Varenummer'])['Pris'].pct_change()
medicine_l

# Take mean prices of the register price of daily dose for Ibuprofen and Paracetamol
paracetamol_m=medicine_l.loc[medicine_l['ATC']=='N02BE01', ['Dato','Pris']]
paracetamol_m=paracetamol_m.groupby(paracetamol_m['Dato']).mean()
paracetamol_m= paracetamol_m.reset_index()

ibuprofen_m=medicine_l.loc[medicine_l['ATC']=='M01AE01', ['Dato','Pris']]
ibuprofen_m=ibuprofen_m.groupby(ibuprofen_m['Dato']).mean()
ibuprofen_m = ibuprofen_m.reset_index()

# Relative change in prices
medicine_l = medicine_l.dropna(subset=['pct_change'])
medicine_l = medicine_l[(medicine_l != 0).all(1)]

paracetamol_change=medicine_l.loc[medicine_l['ATC']=='N02BE01', ['Dato','pct_change']]
paracetamol_change=paracetamol_change.groupby(paracetamol_change['Dato']).mean()
paracetamol_change= paracetamol_change.reset_index()
paracetamol_change

ibuprofen_change=medicine_l.loc[medicine_l['ATC']=='N02BE01', ['Dato','pct_change']]
ibuprofen_change=ibuprofen_change.groupby(ibuprofen_change['Dato']).mean()
ibuprofen_change= ibuprofen_change.reset_index()
ibuprofen_change

############################################################
# Figures
############################################################

# Mean prices of pain killers
ax = plt.gca()
ibuprofen_m.plot(x ='Dato', y='Pris', kind = 'line',ax=ax, label='Ibuprofen avg. price')
paracetamol_m.plot(x ='Dato', y='Pris', kind = 'line',ax=ax, color='red', label='Paracetamol avg. price')

ax.set_xlabel('År')
ax.set_ylabel('Price of daily dose (DKK)')

plt.show()

# Mean of pct. changes in painkillers
ax = plt.gca()
ibuprofen_change.plot(x ='Dato', y='pct_change', kind = 'line',ax=ax, label='Ibuprofen avg. relative change in price')

ax.set_xlabel('År')
ax.set_ylabel('Average change in daily price (%)')

plt.show()

ax = plt.gca()
paracetamol_change.plot(x ='Dato', y='pct_change', kind = 'line',ax=ax, color='red', label='Paracetamol avg. relative change in price')

ax.set_xlabel('År')
ax.set_ylabel('Average change in daily price (%)')

plt.show()


