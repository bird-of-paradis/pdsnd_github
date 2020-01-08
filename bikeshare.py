import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data from chicago, New york city or Washington ? \n")
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? Choose between all, january, february, march, april, may or june \n")
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may' , 'june'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Choose between all, monday, tuesday, wednesday, thursday, friday, saturday or sunday \n")
        if day.lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Not an appropriate choice.")
        else:
            break

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print('Most common month :', months[common_month-1].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week :', common_day)  

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common Start Hour :', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station :', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common End Station :', common_end_station)

    # display most frequent combination of start station and end station trip
    common_start_end_station = (df['Start Station'] + ' => ' + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip :', common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    day = total_time // (24 * 3600)
    total_time = total_time % (24 * 3600)
    hour = total_time // 3600
    total_time %= 3600
    minutes = total_time // 60
    total_time %= 60
    seconds = total_time
    print('Total travel time : %d days, %d hours, %d minutes and %d seconds' % (day, hour, minutes, seconds))

    # display mean travel time
    total_mean_time = df['Trip Duration'].mean()
    day = total_mean_time // (24 * 3600)
    total_mean_time = total_mean_time % (24 * 3600)
    hour = total_mean_time // 3600
    total_mean_time %= 3600
    minutes = total_mean_time // 60
    total_mean_time %= 60
    seconds = total_mean_time
    print('Mean travel time : %d days, %d hours, %d minutes and %d seconds' % (day, hour, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types :\n', user_types)

    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print('Counts of gender :\n', genders)
    except Exception:
        print("Gender doesn't exists")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print('Earliest year of birth : ', earliest_year)
        print('Most recent year of birth : ', recent_year)
        print('Most common year of birth : ', common_year)
    except Exception:
        print("Birth Year doesn't exists")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print("Welcome to this awesome project !!!")
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        v = False
        i = 0
        while True:
            if v:
                show = input('Would you like to view the next 05 lignes of raw data? Enter yes or no.\n')
            else:
                show = input('Would you like to view 05 lignes of raw data? Enter yes or no.\n')
            if show.lower() == 'no':
                break
            elif show.lower() == 'yes':
                print(df.iloc[i:(5+i)])
                i += 5
                v = True
            else:
                print("Not an appropriate choice.")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Good bye dear user. Take care of yourself !!!")
            break


if __name__ == "__main__":
	main()
