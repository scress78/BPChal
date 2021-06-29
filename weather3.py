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
            population = row[2]
            city_pop_entry = [city, pop_weight, population]
            city_pop_weight_table.append(city_pop_entry)
        if count == 0:
            count += 1

# temperatures by date.
with open(weather) as w:
    csv_reader = csv.reader(w, delimiter=',')
    # bullshit
    count = 0  # keeps track of rows in file (not really necessary)
    date_count = 1  # keeps track of how many different dates are listed
    locs_at_date = 0  # keeps track of how many data points for each day
    no_temp_data = 0  # keeps track of rows which don't have temp data
    daily_population = 0  # wrote code to compute; but daily_pop is actually just always 20142145, so cheated
    #  new population WITH ALBANY 20239623

    # not bullshit
    stored_date = ''  # tracker to watch for date changing and trigger daily information dump

    city_list = ['Albany', 'Atlanta', 'Windsor Locks', 'Nashville', 'Boise', 'Boston', 'Buffalo', 'Burbank',
                 'Baltimore', 'Columbus', 'Los Angeles', 'Covington', 'Washington', 'Denver', 'Dallas', 'Detroit',
                 'Fresno', 'Spokane', 'Washington', 'Houston', 'Las Vegas', 'New York', 'Little Rock', 'Memphis',
                 'Minneapolis', 'New Orleans', "Chicago", 'Portland', 'Philadelphia', 'Phoenix', 'Pittsburgh',
                 'Portland', 'Raleigh', 'Richmond', 'Sacramento', 'Seattle', 'San Francisco', 'Salt Lake City',
                 'St. Louis']
    cities_present = []
    city_checklist = []

    weighted_daily_temps_table = []
    weighted_daily_temps_entry = []

    projected_data = []  # table for all projected data

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

    stored_date = ''
    date = ''
    first_row = True
    cities_checklist = []

    for row in csv_reader:
        if count == 0:
            pass
        if count != 0:
            # print(row)
            date = row[5]

            if date == '9/17/2015':
                print(row[0], mean_temp_weighted_tally, high_temp_weighted_tally, low_temp_weighted_tally)
            if date == '9/16/2015':
                print(row[0], stored_daily_mean, stored_daily_high, stored_daily_low)
                print(cities_checklist)

            # !! issue with stored daily temp! need to record each time it is registered
            # if stored_daily_high > 40:
            #     print(check_list_date, stored_date)

            # if stored_date == "7/23/2020":
            #     print(stored_date, mean_temp_weighted_tally, high_temp_weighted_tally, low_temp_weighted_tally)

            # check to see if there's a checklist.. always try to clear the checklist and store data FIRST!
            if len(cities_checklist) != 0:
                if row[0] not in cities_checklist:
                    airports = ['Detroit/Wayne', 'Wash DC/Dulles', 'NYC/LaGuardia', "Chicago O'Hare",
                                'Phoenix/Sky HRBR', 'Raleigh/Durham', 'Sacramento/Execu', 'St Louis/Lambert']
                    if row[0] in airports:
                        my_pseudo_city = ""
                        if "Detroit" in row[0]:
                            my_pseudo_city = ("Detroit")
                            # print("Detroit succesful!")
                        if "Dulles" in row[0]:
                            my_pseudo_city = ("Washington")
                            # print("DC WORKED!")
                        if "NYC" in row[0]:
                            my_pseudo_city = ("New York")
                        if "Hare" in row[0]:
                            my_pseudo_city = ("Chicago")
                        if "HRBR" in row[0]:
                            my_pseudo_city = ("Phoenix")
                        if "Durham" in row[0]:
                            my_pseudo_city = ("Raleigh")
                        if "Execu" in row[0]:
                            my_pseudo_city = ("Sacramento")
                        if "Lambert" in row[0]:
                            my_pseudo_city = ("St. Louis")

                        for x in city_pop_weight_table:

                            if my_pseudo_city == x[0]:
                                try:
                                    if date == '9/16/2015':
                                        print("GOT HERE!")
                                    # print("FOUND!!")
                                    # print(row[0], x[0])

                                    # stored_daily_mean += (float(row[6]) * float(x[1]))
                                    # stored_daily_low += (float(row[7]) * float(x[1]))
                                    # stored_daily_high += (float(row[8]) * float(x[1]))

                                    #error is not here (error was here ;)  )

                                    # if check_list_date == '9/17/2015':
                                    #     #pass
                                    #     print("FIRST RUN!")
                                    #     print(date, str(count))
                                    #     print(stored_daily_mean, stored_daily_high, stored_daily_low)
                                    #     print(len(cities_checklist))
                                    #     print(cities_checklist)
                                    #
                                    # if stored_date == "9/16/2015":
                                    #     #pass
                                    #     print(stored_daily_mean, stored_daily_high, stored_daily_low)
                                    #     print(len(cities_checklist))


                                    # if stored_daily_high > 40:
                                    #     print(check_list_date)
                                    #     print("Line 151")

                                    # record that you projected weather
                                    projected_data_entry = []  # stored as [date, mean, high, low, city]
                                    projected_data_entry.append(check_list_date)  # append date
                                    projected_data_entry.append((float(row[6]) * float(x[1])))  # append mean
                                    projected_data_entry.append((float(row[8]) * float(x[1])))  # append high
                                    projected_data_entry.append((float(row[7]) * float(x[1])))  # append low
                                    projected_data_entry.append(my_pseudo_city)  # append city

                                    projected_data.append(projected_data_entry)
                                    # remove the city from the checklist
                                    cities_checklist.remove(my_pseudo_city)

                                    # at the end check to see if cities checklist is NOW empty.. then add to table
                                    if len(cities_checklist) == 0:
                                        weighted_daily_temps_entry = []  # [date, mean, high, low]
                                        weighted_daily_temps_entry.append(check_list_date)
                                        weighted_daily_temps_entry.append(stored_daily_mean)
                                        weighted_daily_temps_entry.append(stored_daily_high)
                                        weighted_daily_temps_entry.append(stored_daily_low)
                                        weighted_daily_temps_table.append(weighted_daily_temps_entry)

                                        # reset everything
                                        stored_daily_mean = 0
                                        stored_daily_low = 0
                                        stored_daily_high = 0

                                except:
                                    pass
        # END HERE !!!

                # if check_list_date == '9/17/2015':
                #     print(row[0])
                #     print(cities_checklist)
            if row[0] in cities_checklist:
                if check_list_date == '9/17/2015':
                    print(row[0])
                    print(cities_checklist)

                for x in city_pop_weight_table:



                    if row[0] == x[0]:
                        # if check_list_date == '9/16/2015':
                        #     print(x, row[0])
                        #     print(city_checklist)

                        try:
                            # print("FOUND!!")
                            # print(row[0], x[0])
                            stored_daily_mean += (float(row[6]) * float(x[1]))
                            stored_daily_low += (float(row[7]) * float(x[1]))
                            stored_daily_high += (float(row[8]) * float(x[1]))

                            if check_list_date == '9/17/2015':
                                pass
                                # print("SECOND RUN!")
                                # print(stored_daily_mean, stored_daily_high, stored_daily_low)
                                # print(len(cities_checklist))

                            if stored_date == "9/16/2015":
                                pass
                                # print(stored_daily_mean, stored_daily_high, stored_daily_low)
                                # print(len(cities_checklist))

                            # if stored_daily_high > 40:
                            #     print(check_list_date)
                            #     print("Line 213")

                            # record that you projected weather
                            projected_data_entry = []  # stored as [date, mean, high, low, city]
                            projected_data_entry.append(check_list_date)  # append date
                            projected_data_entry.append((float(row[6]) * float(x[1])))  # append mean
                            projected_data_entry.append((float(row[8]) * float(x[1])))  # append high
                            projected_data_entry.append((float(row[7]) * float(x[1])))  # append low

                            projected_data_entry.append(row[0])  # append city
                            projected_data.append(projected_data_entry)
                            # remove the city from the checklist
                            cities_checklist.remove(row[0])
                            # print("After removal")
                            # print(cities_checklist)
                        except:
                            pass

                # at the end check to see if cities checklist is NOW empty.. then add to table
                if len(cities_checklist) == 0:
                    # print("USED BACKUP METHOD!")
                    # print(check_list_date)
                    weighted_daily_temps_entry = []  # [date, mean, high, low]
                    weighted_daily_temps_entry.append(check_list_date)
                    weighted_daily_temps_entry.append(stored_daily_mean)
                    weighted_daily_temps_entry.append(stored_daily_high)
                    weighted_daily_temps_entry.append(stored_daily_low)
                    if stored_daily_high > 40:
                        print(check_list_date)
                        print("248")
                    if check_list_date == '9/17/2015':
                        print("STORED HERE!")
                        print(date)
                        print(row[0])
                    weighted_daily_temps_table.append(weighted_daily_temps_entry)

                    # reset everything
                    stored_daily_mean = 0
                    stored_daily_low = 0
                    stored_daily_high = 0


            # end of a day marker
            if stored_date != date and count != 1:
                # if the date isn't the same you need to first check to see whether your table is complete
                # print(stored_date)

                if len(cities_present) != 39:
                    cities_checklist = city_list.copy()
                    # print(date, len(cities_present))
                    # print(len(cities_checklist))
                    for i in cities_present:
                        if i in cities_checklist:
                            cities_checklist.remove(i)
                    if stored_date == '9/17/2015':
                        print(cities_checklist)
                if len(cities_checklist) != 0:
                    # if there's a checklist store your running data
                    #  then every day check to see if you can complete the data table
                    stored_daily_mean = mean_temp_weighted_tally
                    stored_daily_high = high_temp_weighted_tally
                    stored_daily_low = low_temp_weighted_tally
                    check_list_date = stored_date

                    # reset everything
                    mean_temp_weighted_tally = 0
                    low_temp_weighted_tally = 0
                    high_temp_weighted_tally = 0

                    # print(cities_checklist)
                if len(cities_checklist) == 0:
                    # print("STORING DATA!")
                    # if there's complete data go ahead and store it right away
                    weighted_daily_temps_entry = []  # [date, mean, low, high]
                    weighted_daily_temps_entry.append(stored_date)
                    weighted_daily_temps_entry.append(mean_temp_weighted_tally)
                    weighted_daily_temps_entry.append(high_temp_weighted_tally)
                    weighted_daily_temps_entry.append(low_temp_weighted_tally)
                    if stored_date == '9/17/2015':
                        print("STORED HERE NOT!")

                    if high_temp_tally > 40:
                        print(stored_date)
                        print("293")
                    weighted_daily_temps_table.append(weighted_daily_temps_entry)

                    # reset everything
                    mean_temp_weighted_tally = 0
                    low_temp_weighted_tally = 0
                    high_temp_weighted_tally = 0

                # reset cities present before starting a new day
                cities_present = []

            # build your weighted weather report on a normal day
            for x in city_pop_weight_table:
                if row[0] == x[0]:
                    mean_temp_weighted_tally += (float(row[6]) * float(x[1]))
                    low_temp_weighted_tally += (float(row[7]) * float(x[1]))
                    high_temp_weighted_tally += (float(row[8]) * float(x[1]))

            airports = ['Detroit/Wayne', 'Wash DC/Dulles', 'NYC/LaGuardia', "Chicago O'Hare", 'Phoenix/Sky HRBR',
                        'Raleigh/Durham', 'Sacramento/Execu', 'St Louis/Lambert']
            # build your list of cities accounted for (normal day)
            if row[0] not in airports:
                cities_present.append(row[0])
            if row[0] in airports:
                # print("IN AIRPORTS!")
                if "Detroit" in row[0]:
                    cities_present.append("Detroit")
                    # print("Detroit succesful!")
                if "Dulles" in row[0]:
                    cities_present.append("Washington")
                    # print("DC WORKED!")
                if "NYC" in row[0]:
                    cities_present.append("New York")
                if "Hare" in row[0]:
                    cities_present.append("Chicago")
                if "HRBR" in row[0]:
                    cities_present.append("Phoenix")
                if "Durham" in row[0]:
                    cities_present.append("Raleigh")
                if "Execu" in row[0]:
                    cities_present.append("Sacramento")
                if "Lambert" in row[0]:
                    cities_present.append("St. Louis")

            # count how many weather's you've stored today (actually is done with cities_present)

            # end of day mark which day you ended on
            stored_date = date
        count += 1

    print("row count: " + str(count))
    print("number of dates: " + str(date_count))
    print("rows with no temp data: " + str(no_temp_data))

    # print(projected_data)

    # weight daily temps table is NOW being populated correctly.. spike in graphs are not from
    #   this table being improperly generated
    #print(weighted_daily_temps_table)
    # print(cities_checklist)

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

count = 0
for d in dates:
    if d == '9/17/2015':
        print(count)
    else:
        count += 1

print(mean_temps[2042], high_temps[2042], low_temps[2042])


new_ticks = []
for n, i in enumerate(dates):
    if n % 90 == 0:
        new_ticks.append(i)
    else:
        new_ticks.append('')

plt.xticks(np.arange(2301), new_ticks, rotation='vertical')

plt.title("Population Weighted Temperatures")
plt.xlabel("Date")
plt.ylabel("Temperature (*C)")
plt.plot(dates, mean_temps, color='black', linewidth=.5, label="Daily Mean")
plt.plot(dates, high_temps, color='red', linewidth=.5, label="Daily High")
plt.plot(dates, low_temps, color='blue', linewidth=.5, label="Daily Low")
plt.legend(loc=1)
plt.show()

# monthly highs and lows graph
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
month_data = []
for month in months:
    month_data.append([month, 0, 0, 0, 0])  # [name of month, mean temp, high temp, low temp, # of temps counter]

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
                # print(my_date, i[0])
                # print(month_count)
                if my_date in i[0]:
                    my_date_present = True
                    if month_count <= 12:
                        month_data[month_count - 1][4] += 1
                        month_data[month_count - 1][1] += i[1]
                        month_data[month_count - 1][2] += i[2]
                        month_data[month_count - 1][3] += i[3]
            # print(str(month_count) + "\\" + str(day_count) + "\\" + str(year_count))
            day_count += 1
            impossible_dates = ['2/31', '2/30', '2/29', '4/31', '6/31', '9/31',
                                '11/31']  # nice that the leap year 2/29 was included
            for i in impossible_dates:
                if i in my_date:
                    my_date_present = True
            if day_count >= 21 and month_count >= 4 and year_count >= 2021:
                my_date_present = True
            if month_count > 4 and year_count >= 2021:
                my_date_present = True
            if my_date_present is False:
                absent_dates.append(my_date)
                # print("MISSED DATE! "+ my_date)
            my_date_present = False
        month_count += 1
        # print(month_data)
        day_count = 1
    year_count += 1
    month_count = 1

print(absent_dates)

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

# projection_dates = ['3/6/2015', '10/30/2015', '3/11/2016', '11/4/2016', '3/10/2017', '9/14/2017', '11/3/2017', '3/9/2018',
#                     '11/2/2018', '3/8/2019', '11/1/2019', '3/6/2020', '10/30/2020', '3/12/2021']
# # manually entered list of dates from which we need to grab temperature data and add to our graph
# #  then later make info about
# count = 1
# projected_data = []
# for i in weighted_daily_temps_table:
#     #print(i[0])
#     for d in projection_dates:
#         if d in i[0]:
#             #print(i)
#             if count < len(absent_dates):
#                 date_entry = absent_dates[len(absent_dates) - count]
#                 #print(projection_dates[len(projection_dates) - count])
#                 project_data_entry = []
#                 project_data_entry.append(date_entry)
#                 project_data_entry.append(i[1])
#                 project_data_entry.append(i[2])
#                 project_data_entry.append(i[3])
#                 #print(project_data_entry)
#                 #print(project_data_entry)
#                 weighted_daily_temps_table.append(project_data_entry)
#                 projected_data.append(project_data_entry)
#             if count == len(absent_dates):
#                 date_entry = absent_dates[0]
#                 #print(projection_dates[len(projection_dates) - count])
#                 project_data_entry = []
#                 project_data_entry.append(date_entry)
#                 project_data_entry.append(i[1])
#                 project_data_entry.append(i[2])
#                 project_data_entry.append(i[3])
#                 #print(project_data_entry)
#                 #print(project_data_entry)
#                 weighted_daily_temps_table.append(project_data_entry)
#                 projected_data.append(project_data_entry)
#             count += 1
#
#
# print(projected_data)

# print(month_data)
for i in month_data:
    i[1] = i[1] / i[4]
    i[2] = i[2] / i[4]
    i[3] = i[3] / i[4]
# print(month_data)
mean_temps = []
high_temps = []
low_temps = []
count = 0
for i in month_data:
    mean_temps.append(month_data[count][1])
    high_temps.append(month_data[count][2])
    low_temps.append(month_data[count][3])
    count += 1
# print(mean_temps)

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
    if i[0] not in dates:
        dates.append(i[0])
        mean_temps.append(i[1])
        high_temps.append(i[2])
        low_temps.append(i[3])
    if i[0] in dates:
        count = 0
        for d in dates:
            if i[0] == d:
                mean_temps[count] += i[1]
                high_temps[count] += i[2]
                low_temps[count] += i[3]
            else:
                count += 1

X = np.arange(len(dates))
plt.title("Projected Data Summary")
plt.xlabel("Dates")
plt.xticks(np.arange(len(dates)), dates, rotation="vertical")
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
