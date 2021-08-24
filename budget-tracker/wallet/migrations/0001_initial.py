# Generated by Django 3.2.6 on 2021-08-20 10:54

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.TextField(choices=[('HealthCare', 'Doctor/Medicine'), ('Loans/Interests', 'Loans/Interests'), ('Travel', 'Petrol/Transport'), ('Cash', 'Cash/Bank/'), ('Lifestyle', 'Grocery/Sports'), ('Food', 'Restaurant/Fast Food'), ('Salary', 'Salary')])),
                ('debit_amount', models.FloatField(default=0)),
                ('credit_amount', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_tracking_date', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('transaction_date', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('credit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_account', to='wallet.account')),
                ('debit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_account', to='wallet.account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.wallet'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('wallet', 'title')},
        ),
    ]
