# Generated by Django 5.1.5 on 2025-01-20 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0003_alter_monosaccharidecomponent_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonosaccharideComposition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('H_num', models.PositiveIntegerField(default=0)),
                ('N_num', models.PositiveIntegerField(default=0)),
                ('F_num', models.PositiveIntegerField(default=0)),
                ('P_num', models.PositiveIntegerField(default=0)),
                ('T_num', models.PositiveIntegerField(default=0)),
                ('A_num', models.PositiveIntegerField(default=0)),
                ('G_num', models.PositiveIntegerField(default=0)),
                ('S_num', models.PositiveIntegerField(default=0)),
                ('E_num', models.PositiveIntegerField(default=0)),
                ('M_num', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Composition',
                'verbose_name_plural': 'Compositions',
            },
        ),
        migrations.RemoveField(
            model_name='diagnosticfragment',
            name='motif_structure',
        ),
        migrations.AddField(
            model_name='diagnosticfragment',
            name='mass',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='glycan',
            name='diagnostic_fragments',
            field=models.ManyToManyField(blank=True, to='DB.diagnosticfragment'),
        ),
        migrations.AlterField(
            model_name='glycan',
            name='monosaccharide_comp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glycans', to='DB.monosaccharidecomposition'),
        ),
        migrations.DeleteModel(
            name='MonosaccharideComponent',
        ),
    ]
