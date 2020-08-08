import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) 
    city = input("\nWould you like to filter the data for Chicago, New York, or Washington?\n").lower()
    # request the user input for city again if the first input was not valid
    while city not in CITY_DATA.keys():
        city = input("\nInvalid city. Please choose Chicago, New York, or Washington.\n").lower()
    
    # get user input for how to filter the data
    filter_mode = input("\nWould you like to filter the data by month, day, both or not at all? Type \"none\" for no time filter.\n").lower()
    # create a list with the valid filters
    available_filters = ['month', 'day', 'both', 'none']
    # request the user input again if the first input was not valid
    while filter_mode not in available_filters:
        filter_mode = input("\nInvalid filter. Please the filter by month, day, both or not at all (type \"none\" for no time filter).\n").lower()
    
    # get user input for month (all, january, february, ... , june)
    if filter_mode == 'month' or filter_mode == 'both':
        # create a list from january to june using the calendar library and list comprehension to compare with the user input
        available_months = [x for x in list(calendar.month_name)[1:7]]
        month = input("\nWhich month? January, February, March, April, May, or June?\n").capitalize()
        ## request the user input again if the first input was not valid
        while month not in available_months:
            month = input("\nInvalid month. Please choose January, February, March, April, May, or June?\n").capitalize()
    else:
        month = 'all'

    # get user input for day of the week (all, monday, tuesday, ... sunday)
    if filter_mode == 'day' or filter_mode == 'both':
        # creates a list that contain the name of the days from Sunday to Saturday
        day_name = [calendar.day_name[x] for x in calendar.Calendar(firstweekday=6).iterweekdays()]
        select_day = int(input("\nWhich day? Please type your response as an integer (e.g., 1=Sunday).\n"))
        # request the user input again if the first input was not valid
        while select_day not in list(range(1, 8)):
            select_day = int(input("\nInvalid day. Please choose a day as an integer (e.g., 1=Sunday).\n"))
        day = day_name[(select_day - 1)]
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe acording to the city
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract the month from the Start Time column to create an Month Name column
    df['Month Name'] = df['Start Time'].dt.month_name()
    # extract the day from the Start Time column to create an Weekday name column
    df['Weekday'] = df['Start Time'].dt.weekday_name
    # extract hour from the Start Time column to create an hour column
    df['Start Hour'] = df['Start Time'].dt.hour
    # applies a filter to the data based on the month
    if month != 'all':
        df = df[df['Month Name'] == month]
    # applies a filter to the data based on the day of the week
    if day != 'all':
        df[df['Weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month: {}'.format(df['Month Name'].mode()[0]))

    # display the most common day
    print('\nMost Common Day of Week: {}'.format(df['Weekday'].mode()[0]))

    # display the most common start hour
    print('\nMost Common Start Hour: {}'.format(df['Start Hour'].mode()[0]))

    # display the most common day part as start hour
    star_hour_cnt = df['Start Hour'].count()
    morning, afternoon, evening, night = 0, 0, 0, 0
    for hour, cnt in df.groupby(['Start Hour'])['Start Hour'].count().iteritems():
        if (hour > 6 and hour <= 12):
            morning += cnt
        elif (hour > 12 and hour <= 17):
            afternoon += cnt
        elif (hour > 17 and hour <= 20):
            evening  += cnt
        else:
            night += cnt
    print('\nMost Common Day Part as Start Hour:\n - Morning: {:.2%}\n - Afternoon: {:.2%}\n - Evening: {:.2%}\n - Night: {:.2%}'.format(morning/star_hour_cnt, afternoon/star_hour_cnt, evening/star_hour_cnt, night/star_hour_cnt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly Used Start Station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nMost Commonly Used End Station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    station_trip = '- START STATION: ' + df['Start Station'] + ' / ' + 'END STATION: ' + df['End Station']
    print('\nMost Frequent Combination of Start Station and End Station:\n {}'.format(station_trip.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, day):
    """Displays statistics on the total and average trip duration.
    
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day (if applicable)
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display the total of travel time
    print('Total Travel Time: {:,}'.format(df['Trip Duration'].sum()))

    # display the mean of the travel time
    print('\nMean Travel Time: {:.2f}'.format(df['Trip Duration'].mean()))

    # display the total of travel time by day of the week
    if day == 'all':
        print('\nAccording the day, Total Travel Time are divided into:')
        for day, total in df.groupby(['Weekday'])['Trip Duration'].sum().sort_values(ascending=False).iteritems():
            print(' - {}: {:,} ({:.2%})'.format(day, total, total / df['Trip Duration'].sum()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day (if applicable)
        (str) city - name of the city to analyze
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types if the information was available
    if 'User Type' in df.columns:
        print('According to the type, users are divided into:')
        for user_type, cnt in df['User Type'].value_counts().iteritems():
            print(' - {}: {:,} ({:.2%})'.format(user_type, cnt, cnt / df['User Type'].count()))
    else:
        print('User Type statistics are not available for {}!'.format(city.capitalize()))

    # Display counts of gender if the information was available
    if 'Gender' in df.columns:
        print('\nAccording to the gender, users are divided into:')
        for user_gender, cnt in df['Gender'].value_counts().iteritems():
            print(' - {}: {:,} ({:.2%})'.format(user_gender, cnt, cnt / df['Gender'].count()))
    else:
        print('\nGender statistics are not available for {}!'.format(city.capitalize()))

    # Display the birth year statistics if the information was available
    if 'Birth Year' in df.columns:
        print('\nBirth Year statistics:')
        # Display the earliest year of birth
        print(' - Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        # Display the most recent year of birth
        print(' - Most Recent year of birth: {}'.format(int(df['Birth Year'].max())))
        # Display the most common year of birth
        print(' - Most Common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('\nBirth Year statistics are not available for {}!'.format(city.capitalize()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays the raw data.
    
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day (if applicable)
    """
    rows = 0
    # while the user input was 'yes', displays five rows from the last row displayed
    while True:
        display = input('\nDo you want to see the raw data? Enter yes or no.\n').lower()
        if display == 'yes':
            add_rows = df.iloc[rows:rows+5]
            print(add_rows)
            rows += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, day)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
