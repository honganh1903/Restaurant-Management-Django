from res.models import Student
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "res.settings")
django.setup()

settings.configure(
    INSTALLED_APPS=["res"],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3"
        }
    }
)


s = Student(roll='1', name='Thuan', email='a@gmail.com',
            address='DN', phone='111')
s.save()
