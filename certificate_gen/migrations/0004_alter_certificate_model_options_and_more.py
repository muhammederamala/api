# Generated by Django 4.1.2 on 2023-07-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("certificate_gen", "0003_alter_certificate_model_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="certificate_model",
            options={},
        ),
        migrations.AlterField(
            model_name="certificate_model",
            name="certificate_number",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
