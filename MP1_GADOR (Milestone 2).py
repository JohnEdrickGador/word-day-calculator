import datetime
import sys
def isYearLeap(y): 
    #checks if the year is a leap year
    if (y%4==0 and y%100!=0 or y%400==0):
        return True
    else:
        return False
def nth_day(month,day,year): 
    #returns the day number of the input date
    nth_day = day
    for months_passed in range(1,month):
        if isYearLeap(year) == True:
            if months_passed in [1,3,5,7,8,10,12]:
                nth_day += 31
            elif months_passed in [4,6,9,11]:
                nth_day += 30
            elif months_passed == 2:
                nth_day += 29
        else:
            if months_passed in [1,3,5,7,8,10,12]:
                nth_day += 31
            elif months_passed in [4,6,9,11]:
                nth_day += 30
            elif months_passed == 2:
                nth_day += 28            
    return nth_day

def days_in_a_month(month,year): 
    #returns the number of months in a year
    if isYearLeap(year) == True:
        if month in [1,3,5,7,8,10,12]:
            days = 31
        elif month in [4,6,9,11]:
            days = 30
        elif month == 2:
            days = 29
    else:
        if month in [1,3,5,7,8,10,12]:
            days = 31
        elif month in [4,6,9,11]:
            days = 30
        elif month == 2:
            days = 28            
    return days
def doomsday(month,day,year): 
    #returns week day value of the input date (monday = 1 tuesday = 2 wednesday = 3 thursday = 4 friday = 5 saturday = 6 sunday = 7)
    day_of_week = datetime.date(year,month,day).isoweekday()
    return(day_of_week)
def compute_total_weekends(start_month,start_day,start_year,end_month,end_day,end_year):
    #returns the number of weekends between the start and end month
    total_weekends = 0
    if start_year == end_year:
        if start_month == end_month:
            for day in range(start_day,end_day + 1):
                if doomsday(start_month,day,start_year) in [6,7]:
                    total_weekends += 1
            return total_weekends
        else:
            #weekends for start month
            weekends_in_start_month = []
            days_in_start_month = days_in_a_month(start_month,start_year)
            for day in range(start_day,days_in_start_month+1):
                if  doomsday(start_month,day,start_year) in [6,7]:
                    weekends_in_start_month.append(day) 
            #weekends for months between start month and end month
            weekends_in_between_months = []
            for month in range(start_month + 1,end_month):
                for day in range(1,days_in_a_month(month,start_year) + 1):
                    if doomsday(month,day,start_year) in [6,7]:
                        weekends_in_between_months.append(day)
            #weekends passed by end day within end month
            weekends_passed_by_end_day_within_end_month = []
            for day in range(1,end_day + 1):
                if doomsday(end_month,day,end_year) in [6,7]:
                    weekends_passed_by_end_day_within_end_month.append(day)
            total_weekends = len(weekends_in_start_month) + len(weekends_in_between_months) + len(weekends_passed_by_end_day_within_end_month)
            return total_weekends
    else:
        #weekends for start month
        weekends_in_start_month1 = []
        days_in_start_month = days_in_a_month(start_month,start_year)
        for day in range(start_day,days_in_start_month+1):
            if  doomsday(start_month,day,start_year) in [6,7]:
                weekends_in_start_month1.append(day) 
        #weekends of the remaining months of start year 
        weekends_for_other_months = []
        for month in range(start_month + 1,13):
            days_in_this_month = days_in_a_month(month,start_year)
            for day in range(1,days_in_this_month+1):
                if doomsday(month,day,start_year) in [6,7]:
                    weekends_for_other_months.append(day)

        #weekends for years between start and end time
        sundays_for_other_years = 0
        saturdays_for_other_years = 0
        #according to https://www.convertunits.com/dates/howmany/Saturdays-in-2020
        #if the year starts on a Saturday in a non-leap year, you end up with 53 Saturdays. 
        # Or if either of the first two days lands on a Saturday during a leap year, then you can also get 53 Saturdays.
        for year in range(start_year + 1, end_year):
            if isYearLeap(year) == True:
                if doomsday(1,2,year) == 7 or doomsday(1,1,year) == 7  :
                    sundays_for_other_years += 53 
                else:
                    sundays_for_other_years += 52
                if doomsday(1,1,year) == 6 or doomsday(1,2,year) == 6:
                    saturdays_for_other_years += 53
                else:
                    saturdays_for_other_years += 52
            else:
                if doomsday(1,1,year) == 7:
                    sundays_for_other_years += 53
                else:
                    sundays_for_other_years += 52

                if doomsday(1,1,year) == 6:
                    saturdays_for_other_years += 53
                else:
                    saturdays_for_other_years += 52
        weekends_for_extra_years = sundays_for_other_years + saturdays_for_other_years
        #weekends from preceeding months before end months
        weekends_from_preceeding_months_of_end_months = []
        for month in range(1,end_month):
            days_in_prev_months = days_in_a_month(month,end_year)
            for day in range(1,days_in_prev_months+1):
                if doomsday(month,day,end_year) in [6,7]:
                    weekends_from_preceeding_months_of_end_months.append(day)
        #weekends passed by end day within end month
        weekends_passed_by_end_day_within_end_month1 = []
        for day in range(1,end_day + 1):
            if doomsday(end_month,day,end_year) in [6,7]:
                weekends_passed_by_end_day_within_end_month1.append(day)
        total_weekends = len(weekends_in_start_month1) + len(weekends_for_other_months) + weekends_for_extra_years + len(weekends_from_preceeding_months_of_end_months) + len(weekends_passed_by_end_day_within_end_month1)
        return total_weekends
def compute_leap_years(start_month,start_day,start_year,end_month,end_day,end_year):
    #computes the number of extra days caused by leap years
    additional = 0
    if isYearLeap(start_year) == False and isYearLeap(end_year) == False:
    #since both start and end years are not leap years, they are not included in the years to be checked by the loop
        for year in range(start_year + 1,end_year):
            if isYearLeap(year) == True:
                additional += 1
    elif isYearLeap(start_year) == True and isYearLeap(end_year) == False:
    #due to the start year being a leap year, we need to investigate if the start date includes feb 29 which causes the additional day
        if nth_day(start_month,start_day,start_year) <= nth_day(2,29,start_year):
    #the arguments above tests if the start year should be included in the loop's range
            for year in range(start_year,end_year):
                if isYearLeap(year) == True:
                    additional += 1
        elif nth_day(start_month,start_day,start_year) > nth_day(2,29,start_year):
    #a month greater than 2 means that it passed feb 29 which is the additional day which means that the start year should be omitted from the range of the loop
            for year in range (start_year + 1, end_year):
                if isYearLeap(year) == True:
                    additional += 1
    elif isYearLeap(start_year) == False and isYearLeap(end_year) == True:
    #We will examine here the end date's details since it is the leap year
        if nth_day(end_month,end_day,end_year) >= nth_day(2,29,end_year):
    #above are the conditions the end date to satisfy for the end year to be included in the loop's range
            for year in range(start_year + 1,end_year + 1):
                if isYearLeap(year) == True:
                    additional += 1
        elif nth_day(end_month,end_day,end_year) < nth_day(2,29,end_year):
    #the conditions above are opposite of the previous ones. This removes the end year from the range since the date was before feb 29
            for year in range(start_year + 1,end_year):
                if isYearLeap(year) == True:
                    additional += 1
    elif isYearLeap(start_year) == True and isYearLeap(end_year) == True:
    # for the last elif statement, we have both the start and end years as leap years
        if (nth_day(start_month,start_day,start_year) <= nth_day(2,29,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(2,29,end_year)):
            # all the conditions stated above is for the start and end date to be included in the loop's range
            for year in range(start_year,end_year + 1):
                if isYearLeap(year) == True:
                    additional += 1
        elif (nth_day(start_month,start_day,start_year) > nth_day(2,29,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(2,29,end_year)):
            # the condition above checks if the start year should be excluded in the range and the end year be included in the loop's range
            for year in range(start_year + 1,end_year + 1):
                if isYearLeap(year) == True:
                    additional += 1
        elif (nth_day(start_month,start_day,start_year) <= nth_day(2,29,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(2,29,end_year)):
            # the condition above checks if the start year should be included in the loop's range and the end year be ignored.  
            for year in range(start_year,end_year):
                if isYearLeap(year) == True:
                    additional += 1
        elif (nth_day(start_month,start_day,start_year) > nth_day(2,29,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(2,29,end_year)):
            #the condition above checks if both start and end year be excluded from the range.
            for year in range(start_year + 1,end_year):
                if isYearLeap(year) == True:
                    additional += 1
    return additional
def compute_total_days(start_month,start_day,start_year,end_month,end_day,end_year): 
    #computes the total number of days between the start date and end date (includes the end date)
    total_days = 0
    start = datetime.date(start_year,start_month,start_day)
    end = datetime.date(end_year,end_month,end_day)
    diff = end - start
    total_days = total_days + 1 + int(diff.days)
    return total_days
def compute_total_weekdays(start_month,start_day,start_year,end_month,end_day,end_year):
    #to compute the total number of weekdays, the number of weekends is subtracted from total number of days
    total_weekdays = 0
    amt_days = compute_total_days(start_month,start_day,start_year,end_month,end_day,end_year)
    amt_weekends = compute_total_weekends(start_month,start_day,start_year,end_month,end_day,end_year)
    total_weekdays = amt_days - amt_weekends
    return total_weekdays

def error_checker(start_month,start_day,start_year,end_month,end_day,end_year):
    if (1971 <= start_year <= 2020) and (1971 <= end_year <= 2020): #if the year is within range, continue
        if (1 <= start_month <= 12) and (1 <= end_month <= 12): #checks if the input months are valid. If so, checks for the input days
            start_month_days = days_in_a_month(start_month,start_year)
            end_month_days = days_in_a_month(end_month,end_year)
            if ((start_day > start_month_days) or (end_day > end_month_days)) or ((start_day <= 0) or (end_day <= 0)):
                print()
                print("Invalid Input. Exiting Program.")
                sys.exit()
        else: #if the input month is not valid, exit
            print()
            print("Invalid Input. Exiting Program.")
            sys.exit()
        
    else: #if input year is not in range, exit
        print()
        print("Invalid Input. Exiting Program.")
        sys.exit()
def user_inputs():
    inputs = [] #list of inputs
    a = 0
    try:
        start_month = int(input("Enter start month: "))
        inputs.append(start_month)
    except:
        a += 1 
    try:
        start_day = int(input("Enter start day: "))
        inputs.append(start_day)
    except:
        a += 1
    try:
        start_year = int(input("Enter start year: "))
        inputs.append(start_year)
    except:
        a += 1
    try:
        end_month = int(input("Enter end month: "))
        inputs.append(end_month)
    except:
        a += 1  
    try:
        end_day = int(input("Enter end day: "))
        inputs.append(end_day)
    except:
        a += 1
    try:
        end_year = int(input("Enter end year: "))
        inputs.append(end_year)
    except:
        a += 1
    if a != 0:
        return False
    else:       
        return inputs
def compute_new_year(start_month,start_day,start_year,end_month,end_day,end_year):
    new_years_weekday = 0
    if start_year == end_year: #for special cases wherein the start and end dates are within the same year.
        if start_month == end_month:#for cases wherein they are in the same year AND month
            for day in range(start_day,end_day + 1):
                if nth_day(start_month,day,start_year) == nth_day(1,1,start_year): #checks the day is New Year's day
                    if doomsday(start_month,day,start_year) in [1,2,3,4,5]:
                        new_years_weekday += 1
        elif start_month != end_month: #for cases wherein they are in the same year BUT different months
            for month in range(start_month,end_month + 1):
                for day in range(1,days_in_a_month(month,start_year)):
                    if nth_day(month,day,start_year) == nth_day(1,1,start_year): #checks the day is New Year's day
                        if doomsday(month,day,start_year) in [1,2,3,4,5]:
                            new_years_weekday += 1
        return new_years_weekday
    else:
        if (nth_day(start_month,start_day,start_year) == nth_day(1,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(1,1,end_year)): #True True
            if doomsday(start_month,start_day,start_year) in [1,2,3,4,5]:
                new_years_weekday += 1
            if doomsday(1,1,end_year) in [1,2,3,4,5]:
                new_years_weekday += 1
        elif (nth_day(start_month,start_day,start_year) != nth_day(1,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(1,1,end_year)): #False True
            if doomsday (1,1,end_year) in [1,2,3,4,5]:
                new_years_weekday += 1
        elif (nth_day(start_month,start_day,start_year) == nth_day(1,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(1,1,end_year)): #True False
            if doomsday(1,1,start_year)  in [1,2,3,4,5]:
                new_years_weekday += 1
        elif (nth_day(start_month,start_day,start_year) != nth_day(1,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(1,1,end_year)): #False False
            pass
        for year in range(start_year + 1,end_year):
            if doomsday(1,1,year) in [1,2,3,4,5]:
                new_years_weekday += 1
        return new_years_weekday
def compute_labor_day(start_month,start_day,start_yearx ,end_month,end_day,end_year):
    labor_day_weekday = 0
    if start_year == end_year:
        if start_month == end_month:
            for day in range(start_day,end_day + 1):
                if nth_day(start_month,day,start_year) == nth_day(5,1,start_year):
                    labor_day_weekday += 1
        elif start_month != end_month:
            for month in range(start_month,end_month + 1):
                for day in range(1,days_in_a_month(month,start_year)):
                    if nth_day(month,day,start_year) == nth_day(5,1,start_year):
                        if doomsday(month,day,start_year) in [1,2,3,4,5]:
                            labor_day_weekday += 1
        return labor_day_weekday
    else:
        if (nth_day(start_month,start_day,start_year) <= nth_day(5,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(5,1,end_year)): #True True
            if doomsday(5,1,start_year) in [1,2,3,4,5]:
                labor_day_weekday += 1
            if doomsday(5,1,end_year) in [1,2,3,4,5]:
                labor_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) <= nth_day(5,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(5,1,end_year)): #True False
            if doomsday(5,1,start_year) in [1,2,3,4,5]:
                labor_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) > nth_day(5,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(5,1,end_year)): #False True
            if doomsday(5,1,end_year) in [1,2,3,4,5]:
                labor_day_weekday += 1
        elif  (nth_day(start_month,start_day,start_year) > nth_day(5,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(5,1,end_year)): #False False
            pass
        for year in range (start_year + 1,end_year):
            if doomsday(5,1,year) in [1,2,3,4,5]:
                labor_day_weekday += 1
        return labor_day_weekday
def compute_AS_day(start_month,start_day,start_year,end_month,end_day,end_year):
    AS_day_weekday = 0
    if start_year == end_year:
        if start_month == end_month:
            for day in range(start_day,end_day + 1):
                if nth_day(start_month,day,start_year) == nth_day(11,1,start_year):
                    AS_day_weekday += 1
        elif start_month != end_month:
            for month in range(start_month,end_month + 1):
                for day in range(1,days_in_a_month(month,start_year)):
                    if nth_day(month,day,start_year) == nth_day(11,1,start_year):
                        if doomsday(month,day,start_year) in [1,2,3,4,5]:
                            AS_day_weekday += 1
        return AS_day_weekday
    else:
        if (nth_day(start_month,start_day,start_year) <= nth_day(11,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(11,1,end_year)): #True True
            if doomsday(11,1,start_year) in [1,2,3,4,5]:
                AS_day_weekday += 1
            if doomsday(11,1,end_year) in [1,2,3,4,5]:
                AS_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) <= nth_day(11,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(11,1,end_year)): #True False
            if doomsday(11,1,start_year) in [1,2,3,4,5]:
                AS_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) > nth_day(11,1,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(11,1,end_year)): #False True
            if doomsday(11,1,end_year) in [1,2,3,4,5]:
                AS_day_weekday += 1
        elif  (nth_day(start_month,start_day,start_year) > nth_day(11,1,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(11,1,end_year)): #False False
            pass
        for year in range (start_year + 1,end_year):
            if doomsday(11,1,year) in [1,2,3,4,5]:
                AS_day_weekday += 1
        return AS_day_weekday
def compute_christmas_day(start_month,start_day,start_year,end_month,end_day,end_year):
    christmas_day_weekday = 0
    if start_year == end_year:
        if start_month == end_month:
            for day in range(start_day,end_day + 1):
                if nth_day(start_month,day,start_year) == nth_day(12,25,start_year):
                    christmas_day_weekday += 1
        elif start_month != end_month:
            for month in range(start_month,end_month + 1):
                for day in range(1,days_in_a_month(month,start_year)):
                    if nth_day(month,day,start_year) == nth_day(12,25,start_year):
                        if doomsday(month,day,start_year) in [1,2,3,4,5]:
                            christmas_day_weekday += 1
        return christmas_day_weekday
    else:
        if (nth_day(start_month,start_day,start_year) <= nth_day(12,25,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(12,25,end_year)): #True True
            if doomsday(12,25,start_year) in [1,2,3,4,5]:
                christmas_day_weekday += 1
            if doomsday(12,25,end_year) in [1,2,3,4,5]:
                christmas_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) <= nth_day(12,25,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(12,25,end_year)): #True False
            if doomsday(12,25,start_year) in [1,2,3,4,5]:
                christmas_day_weekday += 1
        elif (nth_day(start_month,start_day,start_year) > nth_day(12,25,start_year)) and (nth_day(end_month,end_day,end_year) >= nth_day(12,25,end_year)): #False True
            if doomsday(12,25,end_year) in [1,2,3,4,5]:
                christmas_day_weekday += 1
        elif  (nth_day(start_month,start_day,start_year) > nth_day(12,25,start_year)) and (nth_day(end_month,end_day,end_year) < nth_day(12,25,end_year)): #False False
            pass
        for year in range (start_year + 1,end_year):
            if doomsday(12,25,year) in [1,2,3,4,5]:
                christmas_day_weekday += 1
        return christmas_day_weekday
def compute_holidays(start_month,start_day,start_year,end_month,end_day,end_year):
    #to return the total number of holidays, we get the values from the other functions who are checking for each holiday if they are landing on a weekday. 
    #we then get their sum and return it.
    h_new_year = compute_new_year(start_month,start_day,start_year,end_month,end_day,end_year)
    h_labor_day = compute_labor_day(start_month,start_day,start_year,end_month,end_day,end_year)
    h_all_saints_day = compute_AS_day(start_month,start_day,start_year,end_month,end_day,end_year)
    h_christmas_day = compute_christmas_day(start_month,start_day,start_year,end_month,end_day,end_year)
    total_holidays = h_new_year + h_labor_day + h_all_saints_day + h_christmas_day
    return total_holidays
def compute_workdays(start_month,start_day,start_year,end_month,end_day,end_year):
    #to compute the total number of working days, we subtract the number of holidays from the number of weekdays.
    weekdays = compute_total_weekdays(start_month,start_day,start_year,end_month,end_day,end_year)
    holidays = compute_holidays(start_month,start_day,start_year,end_month,end_day,end_year)
    workdays = weekdays - holidays
    return workdays
#start
inputs = user_inputs()
if inputs == False:
    print()
    print("Invalid Input. Exiting Program.")
    sys.exit()
else:
    start_month = inputs[0]
    start_day = inputs[1]
    start_year = inputs[2]
    end_month = inputs[3]
    end_day = inputs[4]
    end_year = inputs[5]
    error_checker(start_month,start_day,start_year,end_month,end_day,end_year) #A function runs to check if each input is valid. If one of them is invalid, the program will exit. 
    #total days
    total_days = compute_total_days(start_month,start_day,start_year,end_month,end_day,end_year)
    add_days = compute_leap_years(start_month,start_day,start_year,end_month,end_day,end_year)
    total_weekends = compute_total_weekends(start_month,start_day,start_year,end_month,end_day,end_year)
    total_weekdays = compute_total_weekdays(start_month,start_day,start_year,end_month,end_day,end_year)
    #holidays
    new_years = compute_new_year(start_month,start_day,start_year,end_month,end_day,end_year)
    labor_days = compute_labor_day(start_month,start_day,start_year,end_month,end_day,end_year)
    all_saints_days = compute_AS_day(start_month,start_day,start_year,end_month,end_day,end_year)
    christmas_days = compute_christmas_day(start_month,start_day,start_year,end_month,end_day,end_year)
    total_holidays = compute_holidays(start_month,start_day,start_year,end_month,end_day,end_year)
    #total workdays
    total_workdays = compute_workdays(start_month,start_day,start_year,end_month,end_day,end_year)
    #outputs
    print()
    print(f"total days from start date to end date: {total_days}")
    print()
    print(f"total additional days from leap years: {add_days}")
    print()
    print(f"total weekends: {total_weekends}")
    print()
    print(f"total days without weekends: {total_weekdays}")
    print()
    print(f"new year holiday: {new_years}")
    print(f"labor day holiday: {labor_days}")
    print(f"all saints day holiday: {all_saints_days}")
    print(f"christmas holiday: {christmas_days}")
    print(f"total holidays: {total_holidays}")
    print()
    print(f"total working days: {total_workdays}")
