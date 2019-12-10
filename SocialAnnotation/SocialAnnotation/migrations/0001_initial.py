# Generated by Django 3.0 on 2019-12-10 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hypothesis_url', models.URLField()),
                ('hypothesis_text', models.TextField()),
                ('annotation_type', models.CharField(choices=[('Issue', '地域課題'), ('Whom', '当事者（誰が嬉しいのか）'), ('Where', '地域（場所）'), ('How', '取り組み'), ('Who', '取り組みを行っている人（誰がやっているのか）')], max_length=10)),
                ('relevant_url', models.URLField()),
            ],
        ),
    ]