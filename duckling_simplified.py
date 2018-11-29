from duckling import Duckling
import calendar
import re
from datetime import datetime

present = datetime.now()
d = Duckling()
d.load()


def clean_date(date):
    date_in_no = re.sub('[a-zA-Z-:+.]', '', date)
    temp = 0
    year = ''
    month = ''
    day = ''
    for i in date_in_no:
        temp += 1
        if temp <= 4:
            year += i
        if temp == 5 or temp == 6:
            month += i
        if temp == 7 or temp == 8:
            day += i
    return year, month, day


def get_end_date(grain, date):
    date_in_no = re.sub('[a-zA-Z-:+.]', '', date)
    temp = 0
    year = ''
    month = ''
    day = ''
    output = 0
    quarter_means = 2
    for i in date_in_no:
        temp += 1
        if temp <= 4:
            year += i
        if temp == 5 or temp == 6:
            month += i
        if temp == 7 or temp == 8:
            day += i

    if grain == 'year':
        print "grain:", grain
        print "date:", date
        month = 12
        mycal = calendar.monthcalendar(int(year), month)
        last_day = mycal[-1]
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break
        if datetime(int(year), int(month), int(output)) < present:
            print "end_date:",
            print year, "-", month, "-", output
            end_date = str(year) + '-' + str(month) + '-' + str(output)
            return end_date
        else:
            print "present_date:", present
            return present

    elif grain == 'quarter':
        print "grain:", grain
        print "date:", date
        mycal = calendar.monthcalendar(int(year), int(month) + quarter_means)
        last_day = mycal[-1]
        # print last_day
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break
        if datetime(int(year), int(month) + quarter_means, int(output)) < present:
            print "end_date:",
            print year, "-", int(month) + quarter_means, "-", output
            end_date = str(year) + '-' + str(int(month) + quarter_means) + '-' + str(output)
            return end_date
        else:
            print "present_date:", present
            return present

    elif grain == 'month':
        print "grain:", grain
        print "date:", date
        mycal = calendar.monthcalendar(int(year), int(month))
        last_day = mycal[-1]
        # print last_day
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break
        if datetime(int(year), int(month), int(output)) < present:
            print "end_date:",
            print year, "-", month, "-", output
            end_date = str(year) + '-' + str(month) + '-' + str(output)
            return end_date
        else:
            print "present_date:", present
            return present

    elif grain == 'week':
        week_means = 6
        print "grain:", grain
        print "date:", date
        try:
            if datetime(int(year), int(month), int(day) + week_means) < present:
                print "end_date:",
                print year, "-", month, "-", int(day) + week_means
                end_date = str(year) + '-' + str(month) + '-' + str(int(day) + week_means)
                return end_date
            else:
                print "present_date:", present
                return present
        except Exception as error1:
            print "Exception in get end date:: Week"
            print present
            return present
            pass
    else:
        print "grain:", grain
        print "date:", date


def next_date(grain, date):
    date_in_no = re.sub('[a-zA-Z-:+.]', '', date)
    temp = 0
    year = ''
    month = ''
    day = ''
    output = 0
    quarter_means = 2
    for i in date_in_no:
        temp += 1
        if temp <= 4:
            year += i
        if temp == 5 or temp == 6:
            month += i
        if temp == 7 or temp == 8:
            day += i

    if grain == 'year':
        print "grain:", grain
        print "date:", date
        month = 12
        mycal = calendar.monthcalendar(int(year), month)
        last_day = mycal[-1]
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break
        print "end_date:",
        print year, "-", month, "-", output
        end_date = str(year)+'-'+str(month)+'-'+str(output)
        return end_date

    elif grain == 'quarter':
        print "grain:", grain
        print "date:", date
        mycal = calendar.monthcalendar(int(year), int(month) + quarter_means)
        last_day = mycal[-1]
        # print last_day
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break
        print "end_date:",
        print year, "-", int(month) + quarter_means, "-", output
        end_date = str(year) + '-' + str(month) + '-' + str(output)
        return end_date

    elif grain == 'month':
        print "grain:", grain
        print "date:", date
        mycal = calendar.monthcalendar(int(year), int(month))
        last_day = mycal[-1]
        # print last_day
        for day in last_day:
            # print day
            if day is not 0:
                output = day
                # print day
            else:
                break

        print "end_date:",
        print year, "-", month, "-", output
        end_date = str(year) + '-' + str(month) + '-' + str(output)
        return end_date

    elif grain == 'week':
        week_means = 6
        print "grain:", grain
        print "date:", date
        try:
            print "end_date:",
            print year, "-", month, "-", output

            end_date = str(year) + '-' + str(month) + '-' + str(output)
            return end_date

        except:
            print 'Exception in Week'
            pass
    else:
        print "grain:", grain
        print "date:", date


def Parse_date_duckling(result):
    result = d.parse(result)

    for i in range(len(result)):
        if result[i]['dim'] == 'time':
            if result[i]['value']['type'] == 'value':
                grain = result[i]['value']['grain']
                date = result[i]['value']['value']
                year, month, day = clean_date(date)
                if datetime(int(year), int(month), int(day)) > present:
                    end_date = next_date(grain, date)
                else:
                    end_date = get_end_date(grain, date)

                return grain, date, end_date, result[i]['body']

            elif result[i]['value']['type'] == 'interval':
                print "type: interval"
                try:
                    print "fromDate:", result[i]['value']['from']['value']
                    fromdate = result[i]['value']['from']['value']
                    print "grain:", result[i]['value']['from']['grain']
                    grain = result[i]['value']['from']['grain']
                except:
                    grain = result[i]['value']['to']['grain']
                    fromdate = result[i]['value']['to']['value']
                print "toDate  :", result[i]['value']['to']['value']
                end_date = result[i]['value']['to']['value']
                print "grain:", result[i]['value']['to']['grain']
                return grain, fromdate, end_date, result[i]['body']

            else:
                return None, None, None, None
    return None, None, None, None

# result = d.parse('How many closed deals this year?')
