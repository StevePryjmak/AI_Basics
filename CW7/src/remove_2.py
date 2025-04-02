import csv

def remove_columns(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        
        for row in rows:
            del row[:1]

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


input_file = 'generated_data.csv'
output_file = 'output.csv'
remove_columns(input_file, output_file)
