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

    # if a date isn't present use the weather data from the previous day
    stored_daily_mean = 0
    stored_daily_low = 0
    stored_daily_high = 0

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
                weighted_daily_temps_table.append(weighted_daily_temps_entry) # daily entries are [date, mean, high, low]

                # thought below was the way to do it.. but it isn't.. should find the data from the table
                # we already made
            # if daily_mean_temp_avg == 0 and stored_daily_mean != 0:
            #     print("PROJECTED DATA!")
            #     weighted_daily_temps_entry.append(date)
            #     weighted_daily_temps_entry.append(daily_mean_temp_avg)
            #     weighted_daily_temps_entry.append(daily_high_temp_avg)
            #     weighted_daily_temps_entry.append(daily_low_temp_avg)

            weighted_daily_temps_entry = []
            locs_at_date = 1
            #print("date changed")
            date_count += 1

            stored_daily_mean = daily_mean_temp_avg
            stored_daily_high = daily_high_temp_avg
            stored_daily_low = daily_low_temp_avg


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
absent_dates = []  # this table will hold dates not listed in the .csv file. We project data to these dates by grabbing
# the daily averages from the previous date
while year_count <= 2021:
    day_count = 1
    my_date_present = False
    while month_count <= 12:
        while day_count <= 31:
            my_date = str(month_count) + "/" + str(day_count) + "/" + str(year_count)
            for i in weighted_daily_temps_table:
                #print(my_date, i[0])
                #print(month_count)
                if my_date in i[0]:
                    my_date_present = True
                    if month_count <= 12:
                        month_data[month_count - 1][4] += 1
                        month_data[month_count - 1][1] += i[1]
                        month_data[month_count - 1][2] += i[2]
                        month_data[month_count - 1][3] += i[3]
            #print(str(month_count) + "\\" + str(day_count) + "\\" + str(year_count))
            day_count += 1
            impossible_dates = ['2/31', '2/30', '2/29','4/31', '6/31', '9/31', '11/31'] #nice that the leap year 2/29 was included
            for i in impossible_dates:
                if i in my_date:
                    my_date_present = True
            if day_count >= 21 and month_count >= 4 and year_count >= 2021:
                my_date_present = True
            if month_count > 4 and year_count >= 2021:
                my_date_present = True
            if my_date_present is False:
                absent_dates.append(my_date)
                #print("MISSED DATE! "+ my_date)
            my_date_present = False
        month_count += 1
        #print(month_data)
        day_count = 1
    year_count += 1
    month_count = 1



# print(absent_dates)
# Projected data handling below
# GENERATE LIST OF DATES TO GRAB PROJECTIONS
# not going to do this programatically.. it's part of the problem but it's not a big part and once again
#  there's an easier solution... which is BELOW in the list projection_dates
# for i in absent_dates:
#     print(len(i))
#     if len(i) == 8:
#         new_day = int(i[2]) - 1
#         x = i[0:2] +str(new_day) + i[3:8]
#         #projection_dates.append(x)  # BE SURE TO UNCOMMENT!
#     # if len(i) == 9 and i[3] != 0 and i[2] != '/' and i[4] != 0:
#     #     new_day = int(i[3]) - 1
#     #     x = i[0:2] +str(new_day) + i[3:9]
#     #     projection_dates.append(x)

projection_dates = ['3/6/2015', '10/30/2015', '3/11/2016', '11/4/2016', '3/10/2017', '9/14/2017', '11/3/2017', '3/9/2018',
                    '11/2/2018', '3/8/2019', '11/1/2019', '3/6/2020', '10/30/2020', '3/12/2021']
# manually entered list of dates from which we need to grab temperature data and add to our graph
#  then later make info about
count = 1
projected_data = []
for i in weighted_daily_temps_table:
    #print(i[0])
    for d in projection_dates:
        if d in i[0]:
            #print(i)
            if count < len(projection_dates):
                date_entry = projection_dates[len(projection_dates) - count]
                #print(projection_dates[len(projection_dates) - count])
                project_data_entry = []
                project_data_entry.append(date_entry)
                project_data_entry.append(i[1])
                project_data_entry.append(i[2])
                project_data_entry.append(i[3])
                #print(project_data_entry)
                #print(project_data_entry)
                weighted_daily_temps_table.append(project_data_entry)
                projected_data.append(project_data_entry)
            if count == len(projection_dates):
                date_entry = projection_dates[0]
                #print(projection_dates[len(projection_dates) - count])
                project_data_entry = []
                project_data_entry.append(date_entry)
                project_data_entry.append(i[1])
                project_data_entry.append(i[2])
                project_data_entry.append(i[3])
                #print(project_data_entry)
                # print(project_data_entry)
                weighted_daily_temps_table.append(project_data_entry)
                projected_data.append(project_data_entry)

            count += 1


print(projected_data)

#print(month_data)
for i in month_data:
    i[1] = i[1] / i[4]
    i[2] = i[2] / i[4]
    i[3] = i[3] / i[4]
#print(month_data)
mean_temps = []
high_temps = []
low_temps = []
count = 0
for i in month_data:
    mean_temps.append(month_data[count][1])
    high_temps.append(month_data[count][2])
    low_temps.append(month_data[count][3])
    count += 1
#print(mean_temps)

X = np.arange(12)

plt.title("Monthly Avgs/Highs/Lows")
plt.xlabel("Months")
plt.xticks(np.arange(12), months, rotation=45)
plt.ylabel("Temperature (*C)")

plt.bar(X + .5, high_temps, width=.25, color='red', label="High")
plt.bar(X + .25, mean_temps, width=.25, color='black', label="Mean")
plt.bar(months, low_temps, width=.25, color='blue', label="Low")
plt.legend(loc=1)
plt.show()

# Projected data graph
dates = []
mean_temps = []
high_temps = []
low_temps = []
for i in projected_data:
    dates.append(i[0])
    mean_temps.append(i[1])
    high_temps.append(i[2])
    low_temps.append(i[3])

X = np.arange(len(dates))
plt.title("Projected Data Summary")
plt.xlabel("Dates")
plt.xticks(np.arange(len(dates)), dates, rotation=45)
plt.ylabel("Temperature (*C)")

plt.bar(X + .5, high_temps, width=.25, color='red', label="High")
plt.bar(X + .25, mean_temps, width=.25, color='black', label="Mean")
plt.bar(X, low_temps, width=.25, color='blue', label="Low")
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

