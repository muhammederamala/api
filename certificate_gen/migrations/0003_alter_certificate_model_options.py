# Generated by Django 4.1.2 on 2023-07-30 09:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("certificate_gen", "0002_remove_certificate_model_id_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="certificate_model",
            options={"ordering": ["-certificate_number"]},
        ),
    ]