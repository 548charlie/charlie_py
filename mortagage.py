#!c:\python38\python.exe
import calendar
total =232000
interestRate=4.72
year = 2021
month = 8
day = 1
paid = 0
payment = 1600
premiem = 1526.00
print("Principal,  Interest/day, paid, day, month, year,comment" ) 
while total > 0: 

    if day == calendar.monthrange(year, month)[1]:
        day = 1
        if month == 12 and day == 1:
            year += 1
            month = 1
        else:
            month += 1
    else:
        day += 1
    if day == calendar.monthrange(year, month)[1]  :
        total -= premiem
        paid += premiem
        print("{:5.2f},  {:3.2f},  {:5.2f},  {:2d}, {:2d},  {:4d}, premiem paid ".format(total, interestPerDay, paid,day, month, year)     )  

    if day  == 15:
        paid += payment 
        interestPerDay = (interestRate *total)/(36500) 
        print("{:5.2f},  {:3.2f},  {:5.2f},  {:2d}, {:2d},  {:4d}, extra payment".format(total, interestPerDay, paid,day, month, year)     )  
        total -= payment 
        
