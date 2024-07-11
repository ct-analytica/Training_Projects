import pandas as pd
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import numpy as np
from scipy.stats import chi2_contingency



#File Upload window.
def ask_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfile(defaultextension=".csv",
                                  filetypes=[("csv files", '*.csv'),
                                             ('all files', '*.*')]) # shows dialog box and return the path
    return path


#Pop Up Window Naming
def onClick(msg):
    tkinter.messagebox.showinfo("Precision Genetics", msg)

#Prompt & Load the patient's genetic data into a pandas dataframe
pat_columns = ['Gene Symbol', 'NCBI SNP Reference', 'Call']
onClick('Upload Patient Files First')
patient_data = pd.read_csv(ask_path(), skiprows=17, usecols=pat_columns)


onClick('Upload Population Frequency Data Next')
pop_columns = ['NCBI SNP Reference', 'DomNucl', 'RecNucl', 'DomAllele', 'RecessiveAllele']
pop_ref_data = pd.read_csv(ask_path())

# Merge the two data frames using the rsID column
merged_data = pd.merge(patient_data, pop_ref_data, on="NCBI SNP Reference")


# Will need to define/create a patient based dictionary for rsID's and Call
# Creation of patient dictionary
def patient_dict(patient_data):
        patient_data_dict = {}
        for _, row in patient_data.iterrows():
            pt_dict = {}
            rsID = row['NCBI SNP Reference']
            pt_call = row['Call']
            pt_dict[rsID] = pt_call

            patient_data_dict[rsID] = pt_dict
        return patient_data_dict



#Creating a dictionary of the population reference data
def pop_dict(pop_ref_data):
    pop_ref_dict = {}
    for _, row in pop_ref_data.iterrows():
        variant_data ={}
        rsID = row['NCBI SNP Reference']
        dominant_nucleotide = row['DomNucl']
        recessive_nucleotide = row['RecNucl']
        dominant_freq = row['DomAllele']
        recessive_freq = row['RecessiveAllele']

        variant_data[dominant_nucleotide] = dominant_freq
        variant_data[recessive_nucleotide] = recessive_freq

        pop_ref_dict[rsID] = variant_data
    return pop_ref_dict

# Might not have to re-merge
merged_data = pd.merge(patient_data, pop_ref_data, on='NCBI SNP Reference')


pop_ref_row = pop_ref_data
pat_call_row = patient_data
rsID = ['NCBI SNP Reference']
for rsid in rsID:
    patient_call = pat_call_row[rsid],[pat_call_row[rsid]]
    dominant_nucleotide = pop_ref_row[rsid],[pop_ref_row[rsid]]
    recessive_nucleotide = pop_ref_row[rsid],[pop_ref_row[rsid]]
    dominant_freq = pop_ref_row[rsid],[dominant_nucleotide]
    recessive_freq = pop_ref_row[rsid],[recessive_nucleotide]



def convert_nucleotide(nucleotide):
    nucleotide = 'A', 'T', 'C', 'G'
    if nucleotide == dominant_nucleotide:
        return 1
    elif nucleotide == recessive_nucleotide:
        return 0
    else:
        return np.nan


# Define significance level
alpha = 0.05

# Loop over each row in the merged data frame
for _, row in merged_data.iterrows():
    # Get patient call and population nucleotides
    patient_call = convert_nucleotide(row['Call'])
    dominant_nucleotide = row['DomNucl']
    recessive_nucleotide = row['RecNucl']

    # Get expected frequencies based on population reference data
    expected_counts = [pop_ref_dict[row['NCBI SNP Reference']][dominant_nucleotide],
                       pop_ref_dict[row['NCBI SNP Reference']][recessive_nucleotide]]

    # Use chi-squared test to compare patient call with expected frequencies
    observed_counts = [sum([patient_call == 1]), sum([patient_call == 0])]
    _, p, _, _ = chi2_contingency([observed_counts, expected_counts])

    # Add flag column indicating if patient call is significantly different from expected frequencies
    if p < alpha:
        merged_data.loc[_, 'Flag'] = 'Significant'
    else:
        merged_data.loc[_, 'Flag'] = 'Not significant'


#
#More convient way to store the merged data
onClick('Please Choose Where You Would Like To Store This Data')
def save_loc(dataframe):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv"),
                                                        ("All Files", "*.*")])
    if file_path:
        dataframe.to_csv(file_path, index=False)
    root.destroy()
save_loc(merged_data)