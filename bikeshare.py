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
    print('Hi! Do you want to explore some US bikeshare data? Let\'s go!')
    # input for city (chicago, new york city, washington)
    while True:
        city = input("Do you want to see the data of Chicago, New York City or Washington?: ")
        if city.lower() in CITY_DATA:
            break
        else:
            print("Invalid input. Please select one of the three cities: ")

    while True:
       month = input("Which month would you like to filter by? Please enter 'all' if you do not want to filter by month: ")
       if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
           break
       else:
            print("Invalid input. Please enter a valid month or 'all' if you do not want to filter by month: ")

    while True:
       day = input("Which day of the week would you like to filter by? Please enter 'all' if you do not want to filter by day: ")
       if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
       else:
           print("Invalid input. Please enter a valid day of the week or 'all' if you do not want to filter by day: ")

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
    df = pd.read_csv(CITY_DATA[city])

    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    daysofweek = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday':6, 'sunday': 7}
    if month != 'all':
        df['month'] = pd.to_datetime(df['Start Time']).dt.month
        df = df[df['month'] == months[month]]

    if day != 'all':
        df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
        df = df[df['day_of_week'] == daysofweek[day]]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # most frequent combination of start station and end station trip
    comb_start_end = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('Most Frequent Combination of Start Station and End Station:', comb_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time:", total_travel_time)

    mean_travel_time = df["Trip Duration"].mean()
    print("Mean travel time:", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    print(df["User Type"].value_counts())

    # counts of gender
    if "Gender" in df.columns:
      print(df["Gender"].value_counts())
    else:
      print("Gender data is not available for the selected city and time period.")

    # earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
      birth_year = df["Birth Year"].dropna(axis=0)
      earliest_birth_year = int(df['Birth Year'].min())
      print("Earliest birth year: ", earliest_birth_year)

      most_recent_birth_year = int(df['Birth Year'].max())
      print("Most recent birth year:", most_recent_birth_year)

      most_common_birth_year = int(df['Birth Year'].mode()[0])
      print("Most common birth year:", most_common_birth_year)
    else:
      print("Birth year data is not available for the selected city and time period.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you want to see the next 5 rows of data? Enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
