# Generated by Django 4.1.3 on 2022-11-27 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("toyota", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.CreateModel(
            name="ProductIMG",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("img", models.ImageField(upload_to="images/")),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="toyota.product",
                    ),
                ),
            ],
        ),
    ]