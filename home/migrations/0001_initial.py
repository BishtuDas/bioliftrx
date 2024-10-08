# Generated by Django 5.1.1 on 2024-10-03 07:41

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('name', models.CharField(max_length=156)),
                ('position', models.CharField(max_length=156)),
                ('fb', models.CharField(blank=True, max_length=156, null=True)),
                ('insta', models.CharField(blank=True, max_length=156, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=156, null=True)),
                ('image', models.ImageField(upload_to='SEO')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=156)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('number', models.CharField(max_length=150)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=156)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('h1', models.CharField(max_length=156)),
                ('slug', models.CharField(blank=True, max_length=1256, null=True)),
                ('page_name', models.CharField(blank=True, max_length=1256, null=True)),
                ('keyword', models.CharField(max_length=156)),
                ('description', models.CharField(max_length=900)),
                ('title', models.CharField(max_length=156)),
                ('breadcrumb', models.CharField(max_length=156)),
                ('canonical', models.CharField(default='https://thegrandindianroute.com/', max_length=900)),
                ('og_type', models.CharField(max_length=156)),
                ('og_card', models.CharField(max_length=156)),
                ('og_site', models.CharField(max_length=156)),
                ('image', models.ImageField(upload_to='SEO')),
                ('updated', models.DateField(auto_now=True)),
                ('published', models.DateField()),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('edits', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('schema', models.TextField(blank=True, max_length=15622, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.author')),
                ('category', models.ManyToManyField(to='home.category')),
                ('tag', models.ManyToManyField(to='home.tags')),
            ],
        ),
    ]
