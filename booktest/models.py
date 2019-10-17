from django.db import models

# Create your models here


class BookInfo(models.Model):
    tittle = models.CharField(max_length=20)
    pub_date=models.DateField()

    def __str__(self):
        return  self.tittle


class HeroInfo(models.Model):
    name=models.CharField(max_length=10)
    content=models.CharField(max_length=100)
    gender=models.BooleanField(default=True)
    book=models.ForeignKey(BookInfo,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name



