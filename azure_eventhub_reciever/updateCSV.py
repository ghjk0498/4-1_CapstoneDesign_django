import csv

with open('Anomaly Simulation with tzinfo.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    ls = []
    for row in reader:
        ls.append(row)
    ls[0] += ['anomaly_boolean']
    for i in range(1, len(ls)):
        ls[i] += [False]

    with open('Anomaly Simulation with tzinfo - add boolean.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in ls:
            writer.writerow(row)