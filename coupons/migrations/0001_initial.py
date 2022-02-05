# Generated by Django 4.0.2 on 2022-02-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=50, verbose_name='Coupon Code')),
                ('type', models.CharField(choices=[('FLAT', 'Flat'), ('PERCENTAGE', 'Percentage')], default='FLAT', max_length=50, verbose_name='Type')),
                ('offer_value', models.FloatField(default=0, verbose_name='Offer Value')),
                ('coupon_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('status', models.CharField(choices=[('APPROVED', 'Approved'), ('PENDING', 'Pending')], default='PENDING', max_length=50, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'db_table': 'coupon',
                'ordering': ['-offer_value'],
            },
        ),
    ]
