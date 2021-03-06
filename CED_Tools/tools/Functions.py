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

def photo_upload_to(doctorant, filename):
    folder_name = doctorant.cne if doctorant else 'unknown'
    file_extention = filename.split('.')[-1]
    return f"doctorants/{folder_name}/photo.{file_extention}"

def cv_upload_to(doctorant, filename):
    folder_name = doctorant.cne if doctorant else 'unknown'
    file_extention = filename.split('.')[-1]
    return f"doctorants/{folder_name}/CV.{file_extention}"

def cursus_document_upload_to(cursus, filename):
    folder_name = cursus.doctorant.cne if cursus else 'unknown'
    file_extention = filename.split('.')[-1]
    cursus_type = cursus.type.acronyme if cursus else 'unknown'
    return f"doctorants/{folder_name}/{cursus_type}.{file_extention}"

def file_upload_to(instance, filename):
    return f"files/{id_generator()}_-_{filename}"

def safe_image_tag(src):
    #  cleaning external source image
    src = src.replace('http%3A/','') if src else getattr(settings, "MEDIA_URL", "/media")+"no_photo.svg"
    source = src.replace('/media/','http://') if 'edoctorat.usmba.ac.ma' in src else src
    return mark_safe(f'<img src="{source}" style="width:100%;max-width:300px"/>')

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
        return ''

def birhdayValidator(value):
    day_month_year = "".join(re.findall('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', value))
    month_year = "".join(re.findall('^[0-9]{2}/[0-9]{4}$', value))
    year = "".join(re.findall('^[0-9]{4}$', value))

    isValid = True

    if day_month_year:
        try:
            datetime.strptime(day_month_year, "%d/%m/%Y")
        except:
            isValid = False
    elif month_year:
        try:
            datetime.strptime(month_year, "%m/%Y")
        except:
            isValid = False
    elif year:
        try:
            datetime.strptime(year, "%Y")
        except:
            isValid = False
    else:
        isValid = False

    if not isValid:
        raise ValidationError(_('%(value)s is not a valid birthday'), params={'value':value})


def loadinscriptions(file_path):
    import pandas as pd
    from Etudiant.models import Doctorant
    from Administration.models import Sujet

    sujets = pd.read_excel(file_path, dtype={'cin':str, 'cne':str})

    inscriptions = sujets.to_dict(orient="records")

    for row in inscriptions:
        try:
            sujet = Sujet.objects.filter(intitule__icontains=row['sujet']).first()
            row['sujet_id'] = sujet.pk
        except Exception as e:
            row['sujet_id'] = 0
            print(e, row['sujet'])
        
        try:
            doc = Doctorant.objects.filter(cin__icontains=row['cin']).first()
            if(doc):
                row['doc_id'] = doc.pk
            else:
                doc = Doctorant.objects.filter(cne__icontains=row['cne']).first()
                row['doc_id'] = doc.pk
        except Exception as e:
            row['doc_id'] = 0
            print(e, row['cin'], row['cne'])
    
    pd.DataFrame(data=inscriptions).to_csv("inscriptions.csv", index=False)