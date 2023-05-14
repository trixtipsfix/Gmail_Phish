import csv

def write_data(name, email):
    with open('data.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email])

def write_pass(name, email):
    with open('creds.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email])
