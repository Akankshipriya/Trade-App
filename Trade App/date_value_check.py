import datetime


def date_check(Date):
	isValidDate = True
	try :
		year,month,day = Date.split('-')
	except ValueError :
		return True
	try :
		datetime.datetime(int(year),int(month),int(day))
	except ValueError :
	    return True
	if(isValidDate) :
	    return False


def value_check(x,y):
	if x == '' or y == '' or int(x)>int(y):
		return True
	else:
	    return False

def value_check2(x):
	if x == '':
		return True
	else:
	    return False