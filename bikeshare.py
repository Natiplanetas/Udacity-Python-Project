import pandas as pd
import datetime as dt
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] 
#path_csv = 'C:/Users/natip/Desktop/Udacity/Proyecto 2/'
#columns_data = ['Start Time', 'End Time', 'Trip Duration','Start Station', 'End Station','User Type','Gender','Birth Year']

def get_filters():
    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    while True:
        city = input('Would you like to know information or data about Chicago, New York or Washington?:\n')
        city = city.lower()
        if city == "new york":
            city = 'new york city'
            break
        if city not in CITY_DATA.keys():
            print("Incorrect value. That city is not in the list")
            restart = input('\nWould you like to rewrite your answer? Enter yes or no.\n')
            if restart.lower() == 'yes':
                continue
            else:
                raise Exception("\nClosing the program. GOODBYE\n")
        if city in CITY_DATA.keys():
            #print('The inputted string is:', city)
            break
        
    while True:    
        user_input = input('Would you like to filter the data? Enter YES If you like to filter the data by month. If you prefer to see all month, enter NO.\n')
        user_input = user_input.lower()    
        if user_input == 'no': 
            month = 'all'
            break
        if user_input =='yes':
            month = input('Which month: {}.\n'.format(str(" , ".join(months)).title()))
            if month in months:
                month
                break
            else:
                print("Incorrect value")
                restart_month = input('\nWould you like to rewrite your answer? Enter yes or no.\n').lower()
                if restart_month == 'yes':
                    continue
                else:
                    raise Exception("\nClosing the program. GOODBYE\n")
        else:
            print("Incorrect value. Please only write YES or NO")
            continue
            #else:
             #   raise Exception("\nClosing the program. GOODBYE\n")
    while True:
        day = input('If you like to filter the data by day, type a day (e.g., Sunday). Or type NONE for no filter\n').lower()
        #user_input_2 = user_input_2.lower()
        if day != 'none':
            if day not in days:
                print("Incorrect value.(That day is not in the list)")
                restart = input('\nWould you like to rewrite your answer? Enter yes or no.\n')
                if restart.lower() == 'yes':
                    continue
                else:
                    raise Exception("\nClosing the program. GOODBYE\n")  
            if day in days:
                #day = user_input_2
                break      
        if day == 'none':
            day = 'all'
            break 
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
    while True:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] =pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.dayofweek

        if df.empty:
            print('This seach with this parameters, lead to and empty DataFrame !')
            load_data.close()

        else:
            if month != 'all':
        # use the index of the months list to get the corresponding int
                month = months.index(month) + 1
        # filter by month to create the new dataframe
                df = df[df['month'] == month]
                break
            if day != 'all':
        # filter by day of week to create the new dataframe
                day = days.index(day) + 1
                df = df[df['day_of_week'] == day]
                break
            if month == 'all' or day == 'all':
                df
                break 
    #print (df)
    
    return df

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel in {}...\n'.format(city))
    #check_for_nan = df['Start Time'].isnull().values.any()
    #print (check_for_nan)
    
    start_time = time.time()
    city_data = pd.read_csv(CITY_DATA[city])
    city_data['Start Time'] =pd.to_datetime(city_data['Start Time'])
    city_data['month'] = city_data['Start Time'].dt.month
    common_month = city_data['month'].mode()[0]
    city_data['day_of_week'] = city_data['Start Time'].dt.dayofweek
    common_day = city_data['day_of_week'].mode()[0]
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    #display the most common month, day of week, start hour: 

    print("The most common month for traveling in {} was {}.".format(city.upper(),months[common_month - 1].upper()))
    print("The most common day of week for traveling was {}".format(days[common_day - 1].upper()))
    print("The most common hour for traveling was {}\n".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station and used end station
    print('The most commonly used start station was {}'.format(df['Start Station'].mode()[0].upper()))
    print('The most commonly used used end station was {}'.format(df['End Station'].mode()[0].upper()))

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station']+ ' and ' + df['End Station']
    print('The most frequent combination of start station and end station trip was {}\n'.format(df['Combination'].mode()[0].upper()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Previous calculations
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['End Time'] =pd.to_datetime(df['End Time'])
    df['diff'] = df['End Time'] - df['Start Time']
    df['seconds'] = df['diff'].dt.total_seconds()

    # total travel time
    total_time = time.strftime("%H hours %M minutes and %S seconds", time.gmtime(df['seconds'].sum()))
    print('Total travel time {}.'.format(total_time))
    #mean travel time
    mean_time = time.strftime("%H hours %M minutes and %S seconds", time.gmtime(df['seconds'].mean())) 
    print('Mean travel time: {}.\n'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    csv_columns = list(df.columns)

    while True:
        if 'User Type' in df.columns:
            # Display counts of user types
            print("This is the breakdown of Users:\n")
            print(str(df['User Type'].value_counts()))
            break
        else: 
            break
            #print("\nThis took %s seconds." % (time.time() - start_time))
            # Display counts of gender
    while True:        
        if 'Gender' in df.columns:
            print("\nThis is the breakdown of Gender:\n")
            print(str(df['Gender'].value_counts()))
            break
             #print("\nThis took %s seconds.\n" % (time.time() - start_time))
        else: 
            break
    
        # Display earliest, most recent, and most common year of birth
    while True:    
        if 'Birth Year'in df.columns:
            print('\nThe most common year of birth was {}'.format(int(df['Birth Year'].mode()[0])))
            print('The earliest year of birth was {}'.format(int(df['Birth Year'].min())))
            print('The most recent year of birth was {}'.format(int(df['Birth Year'].max())))
            #print("\nThis took %s seconds." % (time.time() - start_time))
            break
        else: 
            break
    while True:    
        if ('Gender'or 'Birth Year') not in df.columns: 
            #restart = input('\nThera are some missing data in this CSV file so, Would you like to enter another city? Enter yes or no.\n')
            #if restart.lower() != 'yes':
            #    raise Exception("\nClosing the program\n")
            #if restart.lower() == 'yes':
            print('\nThera are some missing data in this CSV file')
            break
        else:
            break
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_more(df):
    """Displays raw data filtered by the city, month and day selected by the user, showing the DataFrame df."""
    index = 0
    while True:
        user_input_3 = input("Would you like to see 5 more rows of data?Please type YES or NO:\n")
        while user_input_3.lower() == 'yes':
            print(df.iloc[index:index+5])
            index += 5
            user_input_3 = input("Would you like to see 5 more rows of data?Please type YES or NO:\n")
        if user_input_3.lower() == 'no':
            break
        else:
            print("\nIncorrect value. Please only write YES or NO")
            restart_month = input('Would you like to rewrite your answer? Enter YES for rewrite or NO to close the program.\n').lower()
            if restart_month == 'yes':
                continue
            else:
                raise Exception("\nClosing the program. GOODBYE\n")   

def main():
    while True:
        city, month, day = get_filters()
        print("OK, your filters are: {}, {} and {}.".format(city.upper(), month.upper(),day.upper()))
        print('-'*40)
        df = load_data(city, month, day)
        #print(df.describe())
        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_more(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        

if __name__ == "__main__":
	main()