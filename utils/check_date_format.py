import datetime
from utils.custom_exceptions import CustomError

def check_date_formatISO8601(date_string:str):
    "check string against this date format ISO 8601"
    date_format = '%Y-%m-%d'
    try:
        # formatting the date using strptime() function
        dateObject = datetime.datetime.strptime(date_string, date_format)
    # If the date validation goes wrong
    except ValueError:
        # printing the appropriate text if ValueError occurs
        raise CustomError({'':"Incorrect data format, should be YYYY-MM-DD"})

    except TypeError:
        "this means it a date error we can use it"
        return True