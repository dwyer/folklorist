# Generated by Django 3.2.18 on 2023-02-20 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tbi', '0003_auto_20230220_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balladindex',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbi.balladname'),
        ),
    ]
