# Generated by Django 2.1.1 on 2018-11-13 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact_box', '0004_auto_20181012_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='persons',
        ),
        migrations.AddField(
            model_name='person',
            name='addresses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contact_box.Address'),
        ),
    ]
