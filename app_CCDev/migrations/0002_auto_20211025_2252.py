# Generated by Django 3.2.8 on 2021-10-25 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_CCDev', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='avatar',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='logo',
            field=models.BinaryField(editable=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='img_producto',
            field=models.BinaryField(editable=True),
        ),
    ]
