# Generated by Django 5.2 on 2025-05-07 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_storeurldetailsmodel_review_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeurldetailsmodel',
            name='ratings_count',
            field=models.IntegerField(default=0),
        ),
    ]
