# Generated by Django 4.1.5 on 2023-02-02 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '0002_delete_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=10)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('gst_no', models.CharField(max_length=14)),
                ('Pic', models.FileField(default='sad.jpg', upload_to='Seller_profile')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('des', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=500, max_digits=6)),
                ('pic', models.FileField(default='sad.jpg', upload_to='products_images')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]