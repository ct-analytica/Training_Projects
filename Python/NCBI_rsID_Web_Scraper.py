
import pandas as pd
from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


#The method of this tool is to provide population frequency data for rsID's,
# Information comes directly from NCBI 1000 Genomes Project data sets
# Imported data is processed to create a data table via pandas,
# and export that information as a CSV into a specified folder.
# CSV merger program can be used to consolidate all of these files into a single csv.
# Will possibly integrate that code into the future for time management

#-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-
def ask_rs(): #asks for the rsID
    root=tk.Tk()
    root.withdraw()
    rsid = simpledialog.askstring("rsID", "What is the rsID that you want population frequencies for? (Be sure to put 'rs' before the number)(ex. rs2906)", parent=root)
    return rsid



gather = r'https://www.ncbi.nlm.nih.gov/snp/' + ask_rs()     #This routes us to NCBI with the previously chosen rsID
page = requests.get(gather)                                  #Request
soup = BeautifulSoup(page.content, 'html.parser')            #Parsing
population_table = soup.find(id="popfreq_table")             #html Id of table layout on NCBI
sort = population_table.find_all(class_="stripe")            #html Class of table layout on NCBI
tags = population_table.select('.popfreq_table .stripe')     #Selections

#-=-=-=-=-=-=-=-=-=-=-=-

#It was easier to create a list of Population ID's, seeing as they are the same for every rsID
identification = [gather, '-','-','-','-' ,'-','-','-','-','-','-','-']
population = ['Total', 'European', 'African', 'African Others', 'African American', 'Asian', 'East Asian', 'Other Asian', 'Latin America 1', 'Latin America 2', 'South Asian', 'Other']

#-=-=-=-=-=-=-=-=-=-=-=-
#This section pulls the raw text data of the pull request
samp_size = [ss.get_text() for ss in population_table.select('.popfreq_table .samp_s')]
ref_all = [fa.get_text() for fa in population_table.select(".popfreq_ref_allele")]
alt_all = [aa.get_text() for aa in population_table.select(".popfreq_alt_allele")]
#-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-
#Creation of the pandas data frame
pop_freq = pd.DataFrame({
    "Retrieval Link": identification,
    "Population": population,
    "Sample Size": samp_size,
    "Reference Allele": ref_all,
    "Alternate Allele": alt_all,
})

print(pop_freq)

#Defining the Save Location
def save_loc(dataframe):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv"),
                                                        ("All Files", "*.*")])
    if file_path:
        dataframe.to_csv(file_path, index=False)
    root.destroy()


print("Where do you want to save this data?")
save_loc(dataframe=pop_freq)


###Created By Clark Thurston