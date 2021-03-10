# Generated by Django 3.1.7 on 2021-03-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('item', models.CharField(max_length=500)),
                ('creation_date', models.CharField(max_length=50)),
                ('creation_price', models.IntegerField(default=0)),
                ('trigger_price', models.IntegerField(default=0)),
            ],
        ),
    ]
