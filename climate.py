import sys  # Needed for sys.argv
from typing import List, Dict, Set
from statistics import mean
import collections
import csv

def get_climate(in_filename: str, out_filename: str) -> None:
    """Read historical weather from in_filename, write climate to out_filename.

    Parameters
    ----------
    in_filename :  name of the input file
    out_filename : name of the output file
    """
    in_file = open(in_filename, 'r')

    """
    What you should do:
    1. Read each line of in_file
    2. Skip the first (header) line
    3. Split each line on commas
    4. Get the year, month, and day
    5. Update the statistics (total precip, total low temp, etc)
    6. When done, open the output file.
    7. for each day of the year:
    8. Compute the climate for the day, write to output file.
    """

    next(in_file)   # Skips header row

    total_precip = {}
    total_tempmin = {}
    total_tempmax = {}
    record_tempmin = {}
    record_tempmax = {}
    total_tempmin_year = {}
    total_tempmax_year = {}

    century = 1900
    previous_year = 0

    for line in in_file.readlines():
        line = line.rstrip('\r\n')
        date, precip, tempmax, tempmin = line.split(",")
        # Controls for bad data, such as no entry
        if not date or not precip or not tempmax or not tempmin:
            continue
        # Converts ISO dates
        if "-" in date:
            year, month, day = date.split("-")
            year = int(year)
        # Converts US dates
        if "/" in date:
            month, day, year = date.split("/")
            year = int(year)
            if year < 100 and year < previous_year:
                year += century
            if year == 1999:
                century = 2000
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
        month_day = month + "/" + day
        # Skips leap years
        if month_day == "02/29":
            continue

        date_in_year = month + "/" + day + "/" + str(year)

        # Used to keep track of when to increment century due to
        # inconsistent date formatting.
        previous_year = year

        # Converts string data into floats.
        # Needed for finding maximum, average, minimum.
        precip = float(precip)
        tempmax = float(tempmax)
        tempmin = float(tempmin)

        total_precip.setdefault(month_day, []).append(precip)
        total_tempmin.setdefault(month_day, []).append(tempmin)
        total_tempmax.setdefault(month_day, []).append(tempmax)
        total_tempmin_year.setdefault(year, []).append(tempmin)
        total_tempmax_year.setdefault(year, []).append(tempmax)


    # Unsorted, but will be sorted as per assignment requirement.
    avg_precip = {month_day: round(mean(precip), 1) for month_day, precip in total_precip.items()}
    avg_tempmin = {month_day: round(mean(tempmin), 1) for month_day, tempmin in total_tempmin.items()}
    avg_tempmax = {month_day: round(mean(tempmax), 1) for month_day, tempmax in total_tempmax.items()}
    record_tempmin = {month_day: min(tempmin) for month_day, tempmin in total_tempmin.items()}
    record_tempmax = {month_day: max(tempmax) for month_day, tempmax in total_tempmax.items()}
    record_tempmin_year = {year: min(tempmin) for year, tempmin in total_tempmin_year.items()}
    record_tempmax_year = {year: max(tempmax) for year, tempmax in total_tempmax_year.items()}

    # Sorts dictionary keys, so that January 1st is first, and December 31st is last.
    sorted_avg_precip = {k: avg_precip[k] for k in sorted(avg_precip)}
    sorted_avg_tempmin = {k: avg_tempmin[k] for k in sorted(avg_tempmin)}
    sorted_avg_tempmax = {k: avg_tempmax[k] for k in sorted(avg_tempmax)}
    sorted_record_tempmin = {k: record_tempmin[k] for k in sorted(record_tempmin)}
    sorted_record_tempmax = {k: record_tempmax[k] for k in sorted(record_tempmax)}
    sorted_record_tempmin_year = {k: record_tempmin_year[k] for k in sorted(record_tempmin_year)}
    sorted_record_tempmax_year = {k: record_tempmax_year[k] for k in sorted(record_tempmax_year)}

    out_handle = open(out_filename, 'w')
    out_handle.write("Day,Avg precip,Avg low,Avg high,Min low,Max high,Min low year,Max high year\n")
    out_handle.write("{},{},{},{},{},{},{},{}\n".format(date_in_year, sorted_avg_precip, sorted_avg_tempmin, sorted_avg_tempmax,
        sorted_record_tempmin, sorted_record_tempmax, sorted_record_tempmin_year, sorted_record_tempmax_year))
    out_handle.close()

def usage():
    """Complain that the user ran the program incorrectly."""
    sys.stderr.write('Usage:\n')
    sys.stderr.write('  python climate.py <input-file.csv> <output-file.csv>\n')
    sys.exit()

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit()

    in_filename: str = sys.argv[1]
    out_filename: str = sys.argv[2]

    get_climate(in_filename, out_filename)

if __name__ == '__main__':
    main()

