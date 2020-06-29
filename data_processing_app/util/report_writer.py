import csv


class ReportWriter():
    def __init__(self, file_name):
        self.filename = file_name
        self.csv_file = csv_file = open(f'report/{file_name}', mode='w+')
        self.csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    
    def write(self, *args):
         self.csv_writer.writerow(list(args))

    
    def close(self):
        self.csv_file.close()