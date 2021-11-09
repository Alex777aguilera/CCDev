# Generated by Django 2.1.5 on 2021-11-08 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ACCOUNT_BANK',
            fields=[
                ('ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('DATES', models.CharField(max_length=8)),
                ('DESCR', models.CharField(max_length=500)),
                ('ID_CLIENT', models.CharField(max_length=100)),
                ('TYPE', models.CharField(max_length=1)),
                ('DEBT', models.FloatField()),
                ('CRED', models.FloatField()),
                ('BALANCE', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CLIENT',
            fields=[
                ('ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('NAME', models.CharField(max_length=250)),
                ('ORIGIN', models.CharField(max_length=30)),
                ('AGE', models.PositiveIntegerField()),
                ('STATUS', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('avatar', models.BinaryField(blank=True, editable=True, null=True)),
                ('correo', models.CharField(max_length=50, null=True)),
                ('direccion', models.CharField(max_length=100)),
                ('n_identidad', models.CharField(max_length=30)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Detalle_Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_producto', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empresa', models.CharField(max_length=20)),
                ('logo', models.BinaryField(editable=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=290)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_genero', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('isv', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('carrito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Carrito')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=50)),
                ('img_producto', models.BinaryField(editable=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha_expira', models.DateField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('fecha_registro', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cuenta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Moneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_moneda', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_pago', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_producto', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_transaccion', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Tipo_producto'),
        ),
        migrations.AddField(
            model_name='orden',
            name='t_pago',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Tipo_pago'),
        ),
        migrations.AddField(
            model_name='orden',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detalle_orden',
            name='orden',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Orden'),
        ),
        migrations.AddField(
            model_name='detalle_orden',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Producto'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='genero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Genero'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='carrito',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_CCDev.Producto'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
