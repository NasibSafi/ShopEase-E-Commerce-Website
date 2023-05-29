# Generated by Django 4.2.1 on 2023-05-22 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PhoneReview', '0011_remove_review_relatedbrand_review_relatedbrand'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentId', models.CharField(max_length=16)),
                ('studentName', models.CharField(max_length=16)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='relatedbrand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PhoneReview.brand', verbose_name='Related Brand'),
        ),
    ]
