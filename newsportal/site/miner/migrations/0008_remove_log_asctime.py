# Generated by Django 3.2 on 2021-04-26 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("miner", "0007_alter_log_asctime")]

    operations = [migrations.RemoveField(model_name="log", name="asctime")]
