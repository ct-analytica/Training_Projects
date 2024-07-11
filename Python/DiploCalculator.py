###Creating the function so that the csv will be converted accordingly (Alleletyper)
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

"""This program was created to calculate the diplotype of an individual after a Genotyping run.
 It uses the tables provided by CPIC to give them"""


def ask_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfile(defaultextension=".csv",
                                  filetypes=[("csv files", '*.csv'),
                                             ('all files', '*.*')])  # shows dialog box and return the path
    return path



# Load the AlleleTyper Export CSV file into a pandas DataFrame
allele_cols = ['sample ID', 'CYP2D6', 'CYP2C9']
df = pd.read_csv(ask_path(), skiprows=10, usecols=allele_cols)
allele_df = df

# Load the CPIC table CSV file into another pandas DataFrame
cpic_data = f'genotyping-cpic-2d6-2d9/2d6_2d9_joined.csv'
cpic_df = pd.read_csv(cpic_data)

# Merge the two DataFrames based on the common columns CYP2D6 and CYP2C9
merged_df = pd.merge(allele_df, cpic_df, on=['CYP2D6', 'CYP2C9'])

# Create two new columns to store the Metabolizer Status and Activity Score
merged_df['Metabolizer Status'] = ''
merged_df['Activity Score'] = ''

# Create two dictionaries to store the metabolizer status and activity score for each call
d6_status_dict = dict(zip(cpic_df['CYP2D6'], cpic_df['Metabolizer Status']))
d9_status_dict = dict(zip(cpic_df['CYP2C9'], cpic_df['Metabolizer Status']))
d6_activity_dict = dict(zip(cpic_df['CYP2D6'], cpic_df['Activity Score']))
d9_activity_dict = dict(zip(cpic_df['CYP2C9'], cpic_df['Activity Score']))

# Create two new columns to store the Metabolizer Status and Activity Score
allele_df['Metabolizer Status'] = ''
allele_df['Activity Score'] = ''

# Iterate over each row of the allele DataFrame
for index, row in allele_df.iterrows():
    # Get the cyp2d6 and cyp2c9 calls for the current sample ID
    cyp2d6_call = row['CYP2D6']
    cyp2c9_call = row['CYP2C9']

    # Use the dictionaries to get the metabolizer status and activity score for the current calls
    cyp2d6_status = d6_status_dict.get(cyp2d6_call, 'UND')
    cyp2c9_status = d9_status_dict.get(cyp2c9_call, 'UND')
    cyp2d6_activity = d6_activity_dict.get(cyp2d6_call, 'UND')
    cyp2c9_activity = d9_activity_dict.get(cyp2c9_call, 'UND')

    # Use the comparison results to populate the Metabolizer Status and Activity Score columns of the allele DataFrame
    allele_df.loc[index, 'Metabolizer Status'] = f'2D6: {cyp2d6_status} ||| 2C9: {cyp2c9_status}'
    allele_df.loc[index, 'Activity Score'] = f'{cyp2d6_activity}, {cyp2c9_activity}'

# Export the modified DataFrame to a new CSV file
allele_df.to_csv('modified_dataframe.csv', index=False)

print(allele_df)

def onClick(msg):
    tkinter.messagebox.showinfo("Precision Genetics", msg)

onClick('Please Choose Where You Would Like To Store This Data')

def save_loc(dataframe):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel Files", "*.xlsx"),
                                                        ("CSV Files", "*.csv"),
                                                        ("All Files", "*.*")])
    if file_path:
        try:
            dataframe.to_excel(file_path, index=False, encoding='utf-8-sig')
            onClick('File saved successfully')
        except Exception as e:
            onClick('An error occurred while saving the file: ' + str(e))
    root.destroy()


save_loc(allele_df)


input('Press ENTER to exit')