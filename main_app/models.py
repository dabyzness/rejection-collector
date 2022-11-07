from django.db import models
from datetime import datetime

COMPANY_SIZES = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))

INTERVIEW_TYPES = ('HR Screening', 'Technical', 'Behavioral', 'Negotiation')

STATES = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')

LOCATION_TYPES = ('Office', 'Remote', 'Hybrid')
# Create your models here.
class Company(models.Model):
  name = models.CharField(max_length=100)
  category = models.CharField(max_length=100)
  company_size = models.CharField(max_length=6, choices=COMPANY_SIZES, default=COMPANY_SIZE[0][0])
  website = models.CharField(max_length=250)

class Technology(models.Model):
  name = models.CharField(max_length=50)
  application = models.ForeignKey(Application, on_delete=models.CASCADE)

class Application(models.Model):
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=250)
  application_date = models.DateField(default=datetime.date.today())
  rejection_date = models.DateField(blank=True)
  job_description = models.TextField(max_length=2000, blank=True)
  job_responsibilities = models.TextField(max_length=1000, blank=True)
  sent_followup = models.BooleanField(default=False)

  tech_stack = models.ManyToManyField(Technology)
  location = models.ForeignKey(Location)
  company = models.ForeignKey(Company)
  user = models.ForeignKey(User)
  resume = models.ForeignKey(Application, on_delete=models.CASCADE)

  def should_i_follow_up(self):
    if(datetime.date.today() - self.application_date >= 7 and not self.sent_followup and not self.rejection_date):
      return True
    return False


class Cover_Letter(models.Model):
  url = models.CharField(max_length=250)
  application = models.ForeignKey(Application, on_delete=models.CASCADE)

class Resume(models.Model):
  url = models.CharField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Interviewer(models.Model):
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  linkedin_url = models.CharField(max_length=250)

class Interview(models.Model):
  date = models.DateField(max_length)
  interview_type = models.CharField(max_length=30, choices=INTERVIEW_TYPES, default=INTERVIEW_TYPES[0])
  sent_thank_you = models.BooleanField(default=False)
  sent_followup = models.BooleanField(default=False)
  application.models.ForeignKey(Application, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  interviewer = models.ManyToManyField(Interviewer)

  def should_i_follow_up(self):
    if(datetime.date.today() - self.date >= 7 and not self.sent_followup):
      return True
    return False

class Location(models.Model):
  city = models.CharField(max_length=25)
  state = models.CharField(max_length=2, choices=STATES, default=STATES[0])
  location_type = models.CharField(max_length=6, choices=LOCATION_TYPES, default=LOCATION_TYPES[0])
