# Generated by Django 5.2 on 2025-05-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_storeurldetailsmodel_sentiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeurldetailsmodel',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]
