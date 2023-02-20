# Generated by Django 3.2.18 on 2023-02-20 06:38

from django.db import migrations, models
import django.db.models.deletion
import tbi.models


class Migration(migrations.Migration):

    dependencies = [
        ('tbi', '0002_alter_ballad_historical_references_squashed_0015_alter_ballad_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='balladindex',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbi.ballad'),
        ),
        migrations.AddField(
            model_name='balladname',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbi.ballad'),
        ),
        migrations.AddField(
            model_name='supptradfile',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbi.ballad'),
        ),
        migrations.AlterField(
            model_name='balladname',
            name='title',
            field=tbi.models.IndexableCharField(max_length=255),
        ),
    ]
