import csv
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import re

weather = 'Temperature Data.csv'
population = 'Population Data.csv'


city_pop_weight_table = []
city_pop_entry = []
city = ''
pop_weight = 0
# need population weight assignment table
# this part works
# table which calculates and stores the population weight of each city listed in weather
#  (city's population / 20142145)
with open(population) as p:
    count = 0
    csv_reader = csv.reader(p, delimiter=',')
    for row in csv_reader:
        if count != 0:
            city = row[0]
            pop_weight = row[5]
            city_pop_entry = [city, pop_weight]
            city_pop_weight_table.append(city_pop_entry)
        if count == 0:
            count += 1



# temperatures by date.
with open(weather) as w:
    csv_reader = csv.reader(w, delimiter=',')
    count = 0  #keeps track of rows in file (not really necessary)
    date_count = 1 # keeps track of how many different dates are listed
    locs_at_date = 0  # keeps track of how many data points for each day
    stored_date = '' # tracker to watch for date changing and trigger daily information dump
    no_temp_data = 0 # keeps track of rows which don't have temp data
    daily_population = 0  # wrote code to compute; but daily_pop is actually just always 20142145, so cheated

    weighted_daily_temps_table = []
    weighted_daily_temps_entry = []

    # to tally daily temperatures
    mean_temp_tally = 0
    low_temp_tally = 0
    high_temp_tally = 0

    mean_temp_weighted_tally = 0
    low_temp_weighted_tally = 0
    high_temp_weighted_tally = 0

    daily_mean_temp_avg = 0
    daily_low_temp_avg = 0
    daily_high_temp_avg = 0


    date = ''
    for row in csv_reader:
        date = row[5]


        if stored_date != date:
            try:
                # previously was dividing by loc_at_date.. incorrect as weighted averaged already account for # of locations
                daily_mean_temp_avg = mean_temp_weighted_tally
                daily_low_temp_avg = low_temp_weighted_tally
                daily_high_temp_avg = high_temp_weighted_tally
            except:
                pass

            weighted_daily_temps_entry.append(date)
            weighted_daily_temps_entry.append(daily_mean_temp_avg)
            weighted_daily_temps_entry.append(daily_high_temp_avg)
            weighted_daily_temps_entry.append(daily_low_temp_avg)
            if daily_mean_temp_avg != 0:
                weighted_daily_temps_table.append(weighted_daily_temps_entry)

            weighted_daily_temps_entry = []
            locs_at_date = 1
            #print("date changed")
            date_count += 1

            # to tally daily temperatures
            mean_temp_weighted_tally = 0
            low_temp_weighted_tally = 0
            high_temp_weighted_tally = 0

            daily_mean_temp_avg = 0
            daily_low_temp_avg = 0
            daily_high_temp_avg = 0

            daily_population = 0

        stored_date = date
        try:
            for i in city_pop_weight_table:
                # if row[0] == i[0]:
                #     #print("MATCHED!")
                #     daily_population += float(i[1])

                #print(row[0], i[0])
                if row[0] == i[0]:
                    #print("MATCHED!")
                    #print(float(row[6]) * float(i[1]))

                    mean_temp_weighted_tally += (float(row[6]) * float(i[1]))
                    low_temp_weighted_tally += (float(row[7]) * float(i[1]))
                    high_temp_weighted_tally += (float(row[8]) * float(i[1]))
        except:
            no_temp_data += 1


        count += 1
        locs_at_date += 1
    print("row count: "+str(count))
    print("number of dates: " + str(date_count))
    print("rows with no temp data: " + str(no_temp_data))


# graph temps
dates = []
mean_temps = []
high_temps = []
low_temps = []
for i in weighted_daily_temps_table:
    dates.append(i[0])
    mean_temps.append(i[1])
    high_temps.append(i[2])
    low_temps.append(i[3])

new_ticks = []
for n,i in enumerate(dates):
    if n%90 == 0:
        new_ticks.append(i)
    else:
        new_ticks.append('')


plt.xticks(np.arange(2287),new_ticks, rotation='vertical')

plt.title("Population Weighted Temperatures")
plt.xlabel("Date")
plt.ylabel("Temperature (*C)")
plt.plot(dates,mean_temps, color='black', linewidth=.5, label="Daily Mean")
plt.plot(dates,high_temps, color='red', linewidth=.5, label="Daily High")
plt.plot(dates,low_temps, color='blue', linewidth=.5, label="Daily Low")
plt.legend(loc=1)
plt.show()


#monthly highs and lows graph
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_data = []
for month in months:
    month_data.append([month, 0, 0, 0, 0]) # [name of month, mean temp, high temp, low temp, # of temps counter]


year_count = 2015
month_count = 1
while year_count <= 2021:
    day_count = 1
    while month_count <= 12:
        while day_count <= 31:
            my_date = str(month_count) + "/" + str(day_count) + "/" + str(year_count)
            for i in weighted_daily_temps_table:
                #print(my_date, i[0])
                #print(month_count)
                if my_date in i[0]:
                    if month_count <= 12:
                        month_data[month_count - 1][4] += 1
                        month_data[month_count - 1][1] += i[1]
                        month_data[month_count - 1][2] += i[2]
                        month_data[month_count - 1][3] += i[3]
            #print(str(month_count) + "\\" + str(day_count) + "\\" + str(year_count))
            day_count += 1
        month_count += 1
        #print(month_data)
        day_count = 1
    year_count += 1
    month_count = 1

print(month_data)
for i in month_data:
    i[1] = i[1] / i[4]
    i[2] = i[2] / i[4]
    i[3] = i[3] / i[4]
print(month_data)
mean_temps = []
high_temps = []
low_temps = []
count = 0
for i in month_data:
    mean_temps.append(month_data[count][1])
    high_temps.append(month_data[count][2])
    low_temps.append(month_data[count][3])
    count += 1
print(mean_temps)

X = np.arange(12)

plt.title("Monthly Avgs/Highs/Lows")
plt.xlabel("Months")
plt.xticks(np.arange(12), months, rotation=45)
plt.ylabel("Temperature (*C)")

plt.bar(X + .5, high_temps, width=.25, color='red', label="High")
plt.bar(X + .25, mean_temps, width=.25, color='black', label="Median")
plt.bar(months, low_temps, width=.25, color='blue', label="Low")
plt.legend(loc=1)
plt.show()


# temp = pd.read_csv('Temperature Data.csv')
# pd.set_option('display.max_columns', None)
# #print(temp.head(5))
#
#
# pop = pd.read_csv('Population Data.csv')
# pd.set_option('display.max_columns', None)
# #print(pop.head(5))

