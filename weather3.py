import csv
import matplotlib.pyplot as plt
import numpy as np

# csv files of concern
weather = 'Temperature Data.csv'
population = 'Population Data.csv'

# build table which calculates and stores the population weight of each city listed in weather
#  (city's population / 20239623)
city_pop_weight_table = []
city_pop_entry = []
city = ''
pop_weight = 0

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

def population_computer():
    global weather
    global city_pop_weight_table
    daily_population = 0
    my_pseudo_city = ''
    stored_date = ''
    count = 0

    def airport_pseudonym_converter(my_row):
        """
        converts airport names to common names to match in weighted city population table
        :param my_row: location in row where city/airport name is stored. In this case always row[0]
        :return: a pseudonym for weather data gathered at and referenced by the city's airport
        """
        global my_pseudo_city
        airports = ['Detroit/Wayne', 'Wash DC/Dulles', 'NYC/LaGuardia', "Chicago O'Hare",
                    'Phoenix/Sky HRBR', 'Raleigh/Durham', 'Sacramento/Execu', 'St Louis/Lambert']
        if my_row in airports:
            my_pseudo_city = ""
            if "Detroit" in my_row:
                my_pseudo_city = ("Detroit")
            if "Dulles" in my_row:
                my_pseudo_city = ("Washington")
            if "NYC" in my_row:
                my_pseudo_city = ("New York")
            if "Hare" in my_row:
                my_pseudo_city = ("Chicago")
            if "HRBR" in my_row:
                my_pseudo_city = ("Phoenix")
            if "Durham" in my_row:
                my_pseudo_city = ("Raleigh")
            if "Execu" in my_row:
                my_pseudo_city = ("Sacramento")
            if "Lambert" in my_row:
                my_pseudo_city = ("St. Louis")
        else:
            my_pseudo_city = my_row
        return my_pseudo_city

    with open(weather) as w:
        csv_reader = csv.reader(w, delimiter= ',')
        for row in csv_reader:
            if count == 1:
                date = row[5]
                airport_pseudonym_converter(row[0])
                for x in city_pop_weight_table:
                    if row[0] == my_pseudo_city:
                        daily_population += int(x[2])
                stored_date = date
            if count > 1:
                date = row[5]
                #print(date, stored_date)
                if stored_date != date:
                    #print(stored_date, daily_population)
                    daily_population = 0
                my_pseudo_city = airport_pseudonym_converter(row[0])
                for x in city_pop_weight_table:
                    #print(x[0]), my_pseudo_city
                    if x[0] == my_pseudo_city:
                        daily_population += int(x[2])
                stored_date = date
            #print(count)
            count += 1
    #print(daily_population)
    # w.close()

population_computer()



# temperatures by date.
with open(weather) as w:
    csv_reader = csv.reader(w, delimiter=',')
    # bullshit
    count = 0  # keeps track of rows in file (not really necessary)
    daily_population = 0  # wrote code to compute; but daily_pop is actually just always 20142145, so cheated
    # mess up here,, population was computed without converting airports to city names.. daily population 35218414

    # not bullshit
    stored_date = ''  # tracker to watch for date changing and trigger daily information dump

    city_list = ['Albany', 'Atlanta', 'Windsor Locks', 'Nashville', 'Boise', 'Boston', 'Buffalo', 'Burbank',
                 'Baltimore', 'Columbus', 'Los Angeles', 'Covington', 'Washington', 'Denver', 'Dallas', 'Detroit',
                 'Fresno', 'Spokane', 'Washington', 'Houston', 'Las Vegas', 'New York', 'Little Rock', 'Memphis',
                 'Minneapolis', 'New Orleans', "Chicago", 'Philadelphia', 'Phoenix', 'Pittsburgh',
                 'Portland', 'Raleigh', 'Richmond', 'Sacramento', 'Seattle', 'San Francisco', 'Salt Lake City',
                 'St. Louis']

    #print(len(city_list))
    cities_present = []
    city_checklist = []

    weighted_daily_temps_table = []
    weighted_daily_temps_entry = []

    projected_data = []  # table for all projected data

    mean_temp_weighted_tally = 0
    low_temp_weighted_tally = 0
    high_temp_weighted_tally = 0

    # if a date isn't present use the weather data from the previous day
    stored_daily_mean = 0
    stored_daily_low = 0
    stored_daily_high = 0

    stored_date = ''
    check_list_date = ''
    date = ''
    first_row = True
    cities_checklist = []
    my_pseudo_city = ''
    ninesixteen_tracker = []

    duplicates = ['Rochester', 'Columbus', 'Columbia', 'Pasadena', 'Richmond', 'Aurora', 'Springfield',
                  'Peoria', 'Kansas City', 'Glendale']  # some locations in Population Data.csv are the same name for two different cities. This list helps to prevent duplicate data from being entered.
    daily_duplicates = []

    def weighted_daily_check_entry():
        global check_list_date
        global stored_daily_mean
        global stored_daily_high
        global stored_daily_low
        global weighted_daily_temps_table
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
        return check_list_date, stored_daily_mean, stored_daily_high, stored_daily_low, weighted_daily_temps_table

    def weight_daily_stored_entry():
        global stored_date
        global mean_temp_weighted_tally
        global high_temp_weighted_tally
        global low_temp_weighted_tally
        global weighted_daily_temps_table
        # if there's complete data go ahead and store it right away
        weighted_daily_temps_entry = []  # [date, mean, low, high]
        weighted_daily_temps_entry.append(stored_date)
        weighted_daily_temps_entry.append(mean_temp_weighted_tally)
        weighted_daily_temps_entry.append(high_temp_weighted_tally)
        weighted_daily_temps_entry.append(low_temp_weighted_tally)
        weighted_daily_temps_table.append(weighted_daily_temps_entry)

        # reset everything
        mean_temp_weighted_tally = 0
        low_temp_weighted_tally = 0
        high_temp_weighted_tally = 0
        return stored_date, mean_temp_weighted_tally, high_temp_weighted_tally, low_temp_weighted_tally, weighted_daily_temps_table

    def weight_daily_stored_entry_debug():
        global stored_date
        global mean_temp_weighted_tally
        global high_temp_weighted_tally
        global low_temp_weighted_tally
        global weighted_daily_temps_table
        global stored_daily_high
        global check_list_date
        # if there's complete data go ahead and store it right away
        weighted_daily_temps_entry = []  # [date, mean, low, high]
        weighted_daily_temps_entry.append(stored_date)
        weighted_daily_temps_entry.append(mean_temp_weighted_tally)
        weighted_daily_temps_entry.append(high_temp_weighted_tally)
        weighted_daily_temps_entry.append(low_temp_weighted_tally)
        weighted_daily_temps_table.append(weighted_daily_temps_entry)

        if stored_daily_high > 40:
            print(check_list_date)
            print("248")
        if check_list_date == '9/17/2015':
            print("STORED HERE!")
            print(date)
            print(row[0])

        # reset everything
        mean_temp_weighted_tally = 0
        low_temp_weighted_tally = 0
        high_temp_weighted_tally = 0
        return stored_date, mean_temp_weighted_tally, high_temp_weighted_tally, low_temp_weighted_tally, weighted_daily_temps_table

    def transfer_to_daily():
        """
        When a day does not have complete data builds variables to store that data moving forward to next day
        to complete the day with projections based on the next days weather data from missing locations.
        :return:
        """
        global stored_daily_mean
        global stored_daily_high
        global stored_daily_low
        global mean_temp_weighted_tally
        global high_temp_weighted_tally
        global low_temp_weighted_tally
        global check_list_date
        stored_daily_mean = mean_temp_weighted_tally
        stored_daily_high = high_temp_weighted_tally
        stored_daily_low = low_temp_weighted_tally
        check_list_date = stored_date

        # reset everything
        mean_temp_weighted_tally = 0
        low_temp_weighted_tally = 0
        high_temp_weighted_tally = 0
        return stored_daily_mean, stored_daily_high, stored_daily_low, mean_temp_weighted_tally, high_temp_weighted_tally, low_temp_weighted_tally, check_list_date
    
    def daily_location_adder(my_row):
        """
        # Argument my row will always be the city name found at row[0]
        Converts airport names to their more common city names for processing
        :return: adds common names to cities present list to determine whether info is complete for the day.
        """
        global cities_present
        airports = ['Detroit/Wayne', 'Wash DC/Dulles', 'NYC/LaGuardia', "Chicago O'Hare", 'Phoenix/Sky HRBR',
                    'Raleigh/Durham', 'Sacramento/Execu', 'St Louis/Lambert']
        # build your list of cities accounted for (normal day)
        if my_row not in airports:
            cities_present.append(my_row)
        if my_row in airports:
            # print("IN AIRPORTS!")
            if "Detroit" in my_row:
                cities_present.append("Detroit")
                # print("Detroit succesful!")
            if "Dulles" in my_row:
                cities_present.append("Washington")
                # print("DC WORKED!")
            if "NYC" in my_row:
                cities_present.append("New York")
            if "Hare" in my_row:
                cities_present.append("Chicago")
            if "HRBR" in my_row:
                cities_present.append("Phoenix")
            if "Durham" in my_row:
                cities_present.append("Raleigh")
            if "Execu" in my_row:
                cities_present.append("Sacramento")
            if "Lambert" in my_row:
                cities_present.append("St. Louis")
        return cities_present
    
    def airport_pseudonym_converter(my_row):
        """
        converts airport names to common names to match in weighted city population table
        :param my_row: location in row where city/airport name is stored. In this case always row[0]
        :return: a pseudonym for weather data gathered at and referenced by the city's airport
        """
        global my_pseudo_city
        airports = ['Detroit/Wayne', 'Wash DC/Dulles', 'NYC/LaGuardia', "Chicago O'Hare",
                    'Phoenix/Sky HRBR', 'Raleigh/Durham', 'Sacramento/Execu', 'St Louis/Lambert']
        if my_row in airports:
            my_pseudo_city = ""
            if "Detroit" in my_row:
                my_pseudo_city = ("Detroit")
            if "Dulles" in my_row:
                my_pseudo_city = ("Washington")
            if "NYC" in my_row:
                my_pseudo_city = ("New York")
            if "Hare" in my_row:
                my_pseudo_city = ("Chicago")
            if "HRBR" in my_row:
                my_pseudo_city = ("Phoenix")
            if "Durham" in my_row:
                my_pseudo_city = ("Raleigh")
            if "Execu" in my_row:
                my_pseudo_city = ("Sacramento")
            if "Lambert" in my_row:
                my_pseudo_city = ("St. Louis")
        else:
            my_pseudo_city = my_row
        return my_pseudo_city
        

    for row in csv_reader:
        if count == 0:
            pass
        if count != 0:
            date = row[5]
            # check to see if there's a checklist of cities which require projections for the day..
            #      always try to clear the checklist and store projection data FIRST!
            if len(cities_checklist) != 0:
                if row[0] not in cities_checklist:
                    airport_pseudonym_converter(row[0])
                    for x in city_pop_weight_table:
                        if my_pseudo_city == x[0]:
                            try:
                                # record that you projected weather
                                projected_data_entry = []  # stored as [date, mean, high, low, city]
                                projected_data_entry.append(check_list_date)  # append date
                                projected_data_entry.append((float(row[6]) * float(x[1])))  # append mean
                                projected_data_entry.append((float(row[8]) * float(x[1])))  # append high
                                projected_data_entry.append((float(row[7]) * float(x[1])))  # append low
                                projected_data_entry.append(my_pseudo_city)  # append city

                                projected_data.append(projected_data_entry)
                                dates = ['9/15/2017', '9/16/2017', '9/17/2017', '9/14/2017']
                                if date in dates:
                                    projected_data_entry.append(date)
                                    ninesixteen_tracker.append(projected_data_entry)
                                # if date == '9/15/2017':
                                #     print("PROJECTED DATA ENTRY 9/15")
                                #     print(projected_data_entry)
                                # remove the city from the checklist
                                cities_checklist.remove(my_pseudo_city)

                                # at the end check to see if cities checklist is NOW empty.. then add to table
                                if len(cities_checklist) == 0:
                                    weighted_daily_check_entry()
                            except:
                                pass

            if row[0] in cities_checklist:
                for x in city_pop_weight_table:
                    if row[0] == x[0] and row[0] not in daily_duplicates:
                        if row[0] in duplicates:
                            daily_duplicates.append(row[0])
                        try:
                            stored_daily_mean += (float(row[6]) * float(x[1]))
                            stored_daily_low += (float(row[7]) * float(x[1]))
                            stored_daily_high += (float(row[8]) * float(x[1]))

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
                        except:
                            pass

                # at the end check to see if cities checklist is NOW empty.. then add to table
                if len(cities_checklist) == 0:
                    weighted_daily_check_entry()

            # end of a day marker
            if stored_date != date and count != 1:
                daily_duplicates = []
                # if the date isn't the same you need to first check to see whether your table is complete
                if len(cities_present) != 38:
                    cities_checklist = city_list.copy()
                    for i in cities_present:
                        if i in cities_checklist:
                            cities_checklist.remove(i)
                    if stored_date == '9/17/2015':
                        print(cities_checklist)
                        
                if len(cities_checklist) != 0:
                    # if there's a checklist store your running data
                    transfer_to_daily()

                if len(cities_checklist) == 0:
                    # if there's complete data go ahead and store it right away
                    weight_daily_stored_entry()

                # reset cities present before starting a new day
                cities_present = []

            # build your weighted weather report on a normal day
            for x in city_pop_weight_table:
                my_pseudo_city = airport_pseudonym_converter(row[0])
                if my_pseudo_city == x[0] and my_pseudo_city not in daily_duplicates:
                    if my_pseudo_city in duplicates:
                        daily_duplicates.append(row[0])
                    mean_temp_weighted_tally += (float(row[6]) * float(x[1]))
                    low_temp_weighted_tally += (float(row[7]) * float(x[1]))
                    high_temp_weighted_tally += (float(row[8]) * float(x[1]))

            daily_location_adder(row[0])  # add current row location to cities present list for current day
                    
            stored_date = date  # at the end of day marks which day you ended on. allows for accounting when day changes.
        count += 1

    print("row count: " + str(count))

    #print(projected_data)
    #print(ninesixteen_tracker)
    # for i in ninesixteen_tracker:
    #     print(i[4])
    # print(weighted_daily_temps_table)
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

#print(mean_temps[2042], high_temps[2042], low_temps[2042])

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


# build housing for monthly data. First to verify continuity in weight_daily_temps_table and then to build monthly grouped data graph
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
month_data = []
for month in months:
    month_data.append([month, 0, 0, 0, 0])  # [name of month, mean temp, high temp, low temp, # of temps counter]


# verifies that all dates of interest are listed in our weighted_daily_temps_table
year_count = 2015
month_count = 1
absent_dates = []  # this list will hold dates not listed in the .csv file.
while year_count <= 2021:
    day_count = 1
    my_date_present = False
    while month_count <= 12:
        while day_count <= 31:
            my_date = str(month_count) + "/" + str(day_count) + "/" + str(year_count)
            for i in weighted_daily_temps_table:
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

# monthly grouped data graph
for i in month_data:
    i[1] = i[1] / i[4]
    i[2] = i[2] / i[4]
    i[3] = i[3] / i[4]

mean_temps = []
high_temps = []
low_temps = []
count = 0
for i in month_data:
    mean_temps.append(month_data[count][1])
    high_temps.append(month_data[count][2])
    low_temps.append(month_data[count][3])
    count += 1

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
