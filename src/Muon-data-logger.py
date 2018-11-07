import csv
import time
import epics

epics.ca.HAS_NUMPY = True


with open(r'C:\scripts\muon_results_log.txt', 'a', 0) as f:
    f.write('Logging Data logger errors\n')

    with open(r"C:\scripts\muon_results.csv", "a") as csvfile:
        writer = csv.writer(csvfile)

        while True:
            try:
                value = epics.caget("TE:NDW1801:SEPRTR_01:DAQ:VOLT:_RAW")
                writer.writerow([time.time()] + value.tolist())
                time.sleep(0.05)
            except Exception as ex:
                f.write("Error thrown: " + str(ex) + "\n")
            