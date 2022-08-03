# Generated by Django 4.0.6 on 2022-07-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_user_trust_score_alter_user_bio"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="trust_score",
        ),
        migrations.AddField(
            model_name="user",
            name="voting_right",
            field=models.FloatField(
                default=None,
                help_text="The voting right assigned to the user based on the vouching mechanism.",
                null=True,
            ),
        ),
    ]