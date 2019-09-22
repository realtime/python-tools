import re
import pandas as pd
import os
import sys

logfilename = sys.argv[1]
csvfilename = os.path.splitext(logfilename)[0] + '.csv'

step = 0
data = [];

logfile = open(logfilename,'r')

def match_step(line):
    return re.match(r'\.step (.*)', line)

# find first .step definition
for line in logfile:    
    match = match_step(line)
    if match:
        break

# iterate through all steps with parameters
while match:
    step += 1
    row = { 'step': int(step) }

    parameters = match.group(1).split()
    for p in parameters:
        [key, value] = p.split('=')
        row[key] = float(value)
    
    data.append(row)
    match = match_step(next(logfile))

# iterate through measurement definitions
for line in logfile:    
    match = re.match(r'Measurement: (.*)', line)
    if match:  
        name = match.group(1)
        next(logfile) # skip row with column details

        # iterate through measurement results for each step
        while True:
            measurement = next(logfile).split()
            if not measurement:
                break
            row = { 'step': int(measurement[0]), name: float(measurement[1]) }
            data.append(row)

logfile.close()

frame = pd.DataFrame(data).set_index('step').groupby('step').first()
frame.to_csv(csvfilename)
