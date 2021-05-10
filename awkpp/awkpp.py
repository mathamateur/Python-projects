from zipfile import ZipFile
import csv
from io import TextIOWrapper
from tqdm import tqdm
from os.path import splitext
from ntpath import basename
import math
import random
import statistics


def aggregate(filename):
    with open(filename, 'r') as f:
        csv_file = splitext(f.readline().rstrip())
        with ZipFile(''.join(csv_file)) as zf:
            with zf.open(basename(''.join(csv_file[:-1])), 'r') as infile:
                with open('output.csv', 'w') as wf:
                    reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))
                    writer = csv.DictWriter(wf, reader.fieldnames)
                    writer.writeheader()
                    commands = f.read().strip().split('\n')
                    try:
                        for row in tqdm(reader):
                            if all(map(eval, commands)):
                                writer.writerow(row)
                    except SyntaxError as e:
                        print(f'Command \'{e.text}\' is incorrect!')
