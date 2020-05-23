# Filename: eval.py
# Author: Dharmesh Tarapore <dharmesh@bu.edu>
# Description: Eval file. This is for Dharmesh to run experiments.
#              It serves no production prupose. It is not in 
#              .gitignore because it may help others come up with 
#              ideas. Nothing here is stable code! 
import pandas as pd
from wit import Wit
import secrets

spreadsheet = './data/full_listings_misclassified_2018.xlsx'
#spreadsheet = './data/full_listings.csv'
# Open up file
df = pd.read_excel(spreadsheet, sheet_name='Flagging_misclassifications')
#df = pd.read_csv(spreadsheet)
# Let's see what's in there.