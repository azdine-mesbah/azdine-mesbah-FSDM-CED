from datetime import date, datetime
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from string import ascii_uppercase, digits
from random import choice
import re

from .Constants import MENTIONS

def current_year():
    return date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)    

def year_choices():
    return [r for r in range(date.today().year, getattr(settings, "MIN_YEAR", 1900) , -1)]

def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

def photo_upload_to(instance, filename):
    return f"photos/{instance.cin or id_generator()}.{filename.split('.')[-1]}"

def file_upload_to(instance, filename):
    return f"files/{id_generator()}_-_{filename}"

def safe_image_tag(src=getattr(settings, "MEDIA_URL", "/media")+"photos/no_photo.svg"):
    return mark_safe(f'<img src="{src}" style="width:100%;max-width:300px"/>')

def avg_to_mention(avg):
    if(avg >= 10 and avg < 12):
        return MENTIONS[0][1]
    elif(12 <= avg < 14):
        return MENTIONS[1][1]
    elif(14 <= avg < 16):
        return MENTIONS[2][1]
    elif(16 <= avg):
        return MENTIONS[3][1]
    else:
        return 'Null'

def birhdayValidator(value):
    day_month_year = "".join(re.findall('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', value))
    month_year = "".join(re.findall('^[0-9]{2}/[0-9]{4}$', value))
    year = "".join(re.findall('^[0-9]{4}$', value))

    isValid = True

    if day_month_year:
        print(day_month_year)
        try:
            datetime.strptime(day_month_year, "%d/%m/%Y")
        except:
            isValid = False
    elif month_year:
        print(month_year)
        try:
            datetime.strptime(month_year, "%m/%Y")
        except:
            isValid = False
    elif year:
        print(year)
        try:
            datetime.strptime(year, "%Y")
        except:
            isValid = False
    else:
        isValid = False

    if not isValid:
        raise ValidationError(_('%(value)s is not a valid birthday'), params={'value':value})