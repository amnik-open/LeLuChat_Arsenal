# pylint: skip-file
# Generated by Django 4.2.6 on 2023-12-03 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arsenal', '0002_chat'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='membership',
            name='unique membership',
        ),
        migrations.AlterField(
            model_name='membership',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='arsenal.room'),
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('room', 'member_uuid'), name='unique uuid membership'),
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('room', 'member_email'), name='unique email membership'),
        ),
    ]