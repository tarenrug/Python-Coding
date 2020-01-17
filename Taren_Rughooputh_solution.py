"""
Please write you name here: Taren Rughooputh
"""
import csv
import numpy as np

def process_shifts(path_to_csv):
    input_file=csv.DictReader(open(path_to_csv,"r"))
    row_count = (len(open(path_to_csv).readlines())-1)
    breaks=[]
    start=[]
    end=[]
    pay=[]
    for row in input_file:
        breaks.append(list(map(float,row['break_notes'].replace('PM','').split('-'))))
        start.append(list(map(float,row['start_time'].replace(':','.').split())))
        end.append(list(map(float,row['end_time'].replace(':','.').split())))
        pay.append(list(map(int,row['pay_rate'].split())))
        
    start2=[]
    end2=[]
    pay2=[]
    for i in range(row_count):
        start2.append(start[i][0])
        end2.append(end[i][0])
        pay2.append(pay[i][0])
    
    breaks=np.array(breaks)
    start=np.array(start2)
    end=np.array(end2)
    
    int_start=[int(x) for x in start]
    final_start=(((start-int_start)*100)/60)+int_start
    int_end=[int(x) for x in end]
    final_end=(((end-int_end)*100)/60)+int_end
    int_breaks=np.zeros((row_count,2))
    
    for k in range(row_count):
        int_breaks[k,:]=np.array([int(x) for x in breaks[k,:]])
    final_breaks=(((breaks-int_breaks)*100)/60)+int_breaks
    
    for k in range(row_count):
        if final_breaks[k,0]<9:
            final_breaks[k,0]+=12
            
    for k in range(row_count):
        if final_breaks[k,1]<9:
            final_breaks[k,1]+=12

    times=[]
    totalpay=[]
    for k in range(int(final_end.max()-final_start.min())):
        times.append(final_start.min()+k)
    
    count=0
    for t in times:
        totalpay.append(0)
        for i in range(row_count):
            if (final_start[i] <= t) and (t < final_end[i]):
                totalpay[count]+=pay2[i]
                if (final_breaks[i,0] <= t) and (t < final_breaks[i,1]):
                    totalpay[count]-=pay2[i]
                    
                if (t==int(final_start[i])) and (int(final_start[i])!= final_start[i]):
                    totalpay[count]-=(final_start[i]-int(final_start[i]))*pay2[i]
                    
                if (t==int(final_end[i])) and (int(final_end[i])!= final_end[i]):
                    totalpay[count]-=(((int(final_end[i]))+1)-final_end[i])*pay2[i]
                    
                if (t==int(final_breaks[i,0])) and (int(final_breaks[i,0])!= final_breaks[i,0]):
                    totalpay[count]-=(final_breaks[i,0]-int(final_breaks[i,0]))*pay2[i]
                    
                if (t==int(final_breaks[i,1])) and (int(final_breaks[i,1]) != final_breaks[i,1]):
                    totalpay[count]+=(((int(final_breaks[i,1]))+1)-final_breaks[i,1])*pay2[i]
        count+=1
    
    for k in range(len(totalpay)):
        totalpay[k]=round(totalpay[k],2)
        
    times2=[]
    for k in range(len(times)):
        times2.append(str(times[k]).replace('.0',':00'))
        
    shift_pay = dict(zip(times2, totalpay))
#    print(shift_pay)

#    print(times)
#    print(totalpay)
#    print(final_breaks)
#    print(final_start)
#    print(final_end)
#    print(pay2)

    return(shift_pay)
	
    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """


def process_sales(path_to_csv):
    input_file=csv.DictReader(open(path_to_csv,"r"))
    row_count = (len(open(path_to_csv).readlines())-1)
    amount=[]
    time=[]
    for row in input_file:
        amount.append(list(map(float,row['amount'].split())))
        time.append(list(map(float,row['time'].replace(':','.').split())))
        
    amount2=[]
    time2=[]
    for i in range(row_count):
        amount2.append(amount[i][0])
        time2.append(time[i][0])

    amount=np.array(amount2)
    time=np.array(time2)
    
    hours=[]
    
    for k in range(14):
        hours.append(float(9+k))
    
    total_sales=[]
    count=0
    count2=0
    for h in hours:
        total_sales.append(0)
        for t in time2:
            if int(t)==h:
                total_sales[count]+=amount2[count2]
                count2+=1
        count+=1

    for k in range(len(total_sales)):
        total_sales[k]=round(total_sales[k],2)
        
    hours2=[]
    for k in range(len(hours)):
        hours2.append(str(hours[k]).replace('.0',':00'))
        
    hourly_sales = dict(zip(hours2, total_sales))
    
#    print(total_sales)
#    print(hours)
#    print(amount2)
#    print(time2)
    
#    print(hourly_sales)
    
    return(hourly_sales)
	
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """


def compute_percentage(shift_pay, hourly_sales):
    hours=[]
    for k in range(14):
        hours.append(float(9+k))
    hours2=[]
    for k in range(len(hours)):
        hours2.append(str(hours[k]).replace('.0',':00'))
    percentages=[]
    for k in hours2:
         if hourly_sales[k]==0:
             percentages.append(-shift_pay[k])
         else:
             percentages.append(((shift_pay[k])/(hourly_sales[k]))*100)
             
    for k in range(len(percentages)):
        percentages[k]=round(percentages[k],2)

    percentage_hourly=dict(zip(hours2,percentages))
    
#    print(percentage_hourly)

    return(percentage_hourly)
	
	
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """

def best_and_worst_hour(percentages):
    
    temp_list=[]
    for time, percentage in percentages.items():
        if abs(percentage)+percentage!=0:
            temp_list.append(percentage)
    
    temp1 = min(temp_list)
    temp2 = min(percentages.values())
    
    best_hour=''
    worst_hour=''
    
    for time, percentage in percentages.items():
        if percentage == temp1:
            best_hour = time
        elif percentage == temp2:
            worst_hour = time
    
    return(best_hour, worst_hour)

    """
    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    (best_hour,worst_hour)=best_and_worst_hour(percentages)
    print([best_hour,worst_hour])   


# Please write you name here: Taren Rughooputh
