import requests
import csv
from concurrent.futures import ThreadPoolExecutor
from time import sleep

"""This script uses PubChem's API to pull all of the synonyms available based on the 'common' drug name"""


def get_synonyms_for_drug(drug_name, max_retries=3, retry_delay=2):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/synonyms/TXT'

    for _ in range(max_retries):
        response = requests.get(url)

        if response.status_code == 200:
            synonyms_text = response.text
            synonyms = [synonym.strip() for synonym in synonyms_text.split('\n') if synonym.strip()]
            return drug_name, synonyms
        elif response.status_code == 503:
            print(f"Retrying for drug {drug_name} after status code 503...")
            sleep(retry_delay)
        else:
            print(f"Error getting synonyms for drug {drug_name}. Status code: {response.status_code}")
            return drug_name, []

    print(f"Max retries reached for drug {drug_name}. Unable to retrieve synonyms.")
    return drug_name, []

def retrieve_synonyms_for_drugs(drug_list, max_workers=3):
    drug_synonyms = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(get_synonyms_for_drug, drug_name) for drug_name in drug_list]

        for future in futures:
            drug_name, synonyms = future.result()
            drug_synonyms[drug_name] = synonyms
            print(f"Processed drug: {drug_name}, Synonyms: {synonyms}")

    return drug_synonyms


def read_drug_list_from_csv(csv_file, encoding='utf-8'):
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        drug_list = [row[0] for row in reader if row]  # Drugs in the first column of csv
    return drug_list

def export_results_to_csv(drug_synonyms, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Drug', 'Synonyms'])

        for drug, synonyms in drug_synonyms.items():
            writer.writerow([drug, ', '.join(synonyms)])

# Using the thing
if __name__ == "__main__":
    input_csv = r'Numbers.csv'
    output_csv = r'DRUG_SYN_0_9.csv'
    max_workers = 2

    drug_list = read_drug_list_from_csv(input_csv, encoding='utf-8')
    drug_synonyms = retrieve_synonyms_for_drugs(drug_list)
    export_results_to_csv(drug_synonyms, output_csv)

    for drug, synonyms in drug_synonyms.items():
        print(f"Drug: {drug}, Synonyms: {synonyms}")
