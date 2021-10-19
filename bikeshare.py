import time
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cities = ['chicago', 'new_york_city', 'washington']
    months = ['all', 'january', 'february', 'march','april','may' , 'june','july','august','september','october','november','december']
    days = ['all','saturday','friday','monday','sunday','tuesday','wednesday','thursday']
    
    while(True):
        try:
            city = input('Please Type the city name  ')
            if city.lower() in cities:
                print(city)
                break
            else:
                match = process.extractOne(city, cities,scorer=fuzz.token_sort_ratio)
                suggested = match[0]
                answer = input('You entered wrong city, do you mean {} ? [y/n]'.format(suggested))
                if answer.lower() == 'y' or answer.lower() == 'yes':
                    city = suggested.lower()
                    print(city)
                    break
                
        except:
            print('Wrong, Please add one of these cities (chicago, new york city, washington)','\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    while(True):
        try:
            month = input('Please Type the month name  ')
            if month.lower() in months:
                print(month)
                break
            else:
                match = process.extractOne(month, months,scorer=fuzz.token_sort_ratio)
                suggested = match[0]
                answer = input('You entered wrong month name, do you mean {} ? [y/n]'.format(suggested))
                if answer.lower() == 'y' or answer.lower() == 'yes':
                    month = suggested.lower()
                    print(month)
                    break
        except:
            print('Wrong, Please check the month name')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        try:
            day = input('Please Type the day name  ')
            if day.lower() in days:
                print(day)
                break
            else:
                match = process.extractOne(day, days,scorer=fuzz.token_sort_ratio)
                suggested = match[0]
                answer = input('You entered wrong day name, do you mean {} ? [y/n]'.format(suggested))
                if answer.lower() == 'y' or answer.lower() == 'yes':
                    day = suggested.lower()
                    print(day)
                    break
        except:
            print('Wrong, Please check the day name','\n')


    print('-'*40)
    return city, month, day


############################  DONE  #################################

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
    #Reading Data
    try:
        data = city + '.csv'
        df_temp = pd.read_csv(data,index_col = 0)
    except:
        print("Can't find the current city data")
        
    #Adding a DateTime column to the dataframe
    #Adding the month and day names columns for the df
    df_temp['Datetime'] = pd.to_datetime(df_temp['Start Time'])
    df_temp['month_name'] = df_temp['Datetime'].dt.month_name().str.lower()
    df_temp['day_name'] = df_temp['Datetime'].dt.day_name().str.lower()
    
    
    #Filtering for month
    if month != 'all':
        if (df_temp['month_name'] == month).sum() == 0:
            print('There is no data for the month {} in this city, So we will view all months'.format(month))
        else:
            df_temp = df_temp[df_temp['month_name'] == month]
                  
        
    if day != 'all':
        if (df_temp['day_name'] == day).sum() == 0:
            print('There is no data for the day {} in this city, So we will view all days'.format(day))
        else:
            df_temp = df_temp[df_temp['day_name'] == day]
    
                                                               
    #Dropping added columns
    df = df_temp.drop(columns = ['Datetime','month_name','day_name'])
    
    #return
    return df

############################  DONE  #################################

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if 'Start Time' in df.columns:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # TO DO: display the most common month
        df['month'] = df['Start Time'].dt.month_name()
        print('Most common month is {}'.format(df['month'].mode()[0]))

        # TO DO: display the most common day of week
        df['day'] = df['Start Time'].dt.day_name()
        print('Most common day is {}'.format(df['day'].mode()[0]))

        # TO DO: display the most common start hour
        df['st_hour'] = df['Start Time'].dt.hour
        print('Most common start hour is {}'.format(df['st_hour'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#########################################################################################
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    if 'Start Station' in df.columns:
        print('The Most Commonly Used Start Station is {}'.format(df['Start Station'].mode().loc[0]))

    # TO DO: display most commonly used end station
    if 'End Station' in df.columns:
        print('The Most Commonly Used End Station is {}'.format(df['End Station'].mode().loc[0]))

    # TO DO: display most frequent combination of start station and end station trip
    if 'Start Station' and 'End Station' in df.columns:
        t = df[['Start Station', 'End Station']].mode().loc[0]
        print('The Most Commonly combination of start station and end station trip {} , {}'.format(t[0],t[1]))
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

###############################################################################
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if 'Trip Duration' in df.columns:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # TO DO: display total travel time
        print('Total travel time is {}'.format(df['Trip Duration'].sum()))

        # TO DO: display mean travel time
        print('Avg travel time is {}'.format(df['Trip Duration'].mean()))


        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if "User Type" in df.columns:
        print('Count of user types: ')
        print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('Count of genders: ')
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year is {}'.format(df['Birth Year'].min()))
        print('Most recent year is {}'.format(df['Birth Year'].max()))
        print('Most common year of birth is {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
#Function that views a sample of data for the user   
def show_data(df):
    counter = 0
    df_len = df.shape[0]
    
    while True:
        try:
            ans = input('Do you want to review some of the data? [y/n]')
            #Checking the answer
            if ans.lower() == 'yes' or ans.lower() == 'y':
                #answer is yes
                #so we check if we have data to review
                if counter + 5 <= df_len:
                    df_subset = df.iloc[counter:counter+5]
                    print(df_subset)
                    counter+= 5
                else:
                    df_subset = df.iloc[counter:]
                    if df_subet.empty: print('No more data')
                    else:
                        print(df_subset)
                    print('Finished Viewing all of the data!!')
                    print('-'*40)
                    break
            #answered no
            else:
                print('-'*40)
                break
        except:
            print('You answered wrong')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
