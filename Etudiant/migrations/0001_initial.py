# Generated by Django 3.2.9 on 2022-01-05 13:59

import CED_Tools.models
import CED_Tools.tools.Functions
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CED_Tools', '0001_initial'),
        ('Administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursusType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('intitule', models.CharField(max_length=255)),
                ('duree_annees', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'Types de Cursus',
                'db_table': 'ced_cursus_types',
            },
        ),
        migrations.CreateModel(
            name='Doctorant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=CED_Tools.tools.Functions.photo_upload_to)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(choices=[('h', 'Homme'), ('f', 'Femme')], max_length=1)),
                ('cne', models.CharField(max_length=10, verbose_name='CNE')),
                ('cin', models.CharField(max_length=10, verbose_name='CIN')),
                ('date_naissance', models.CharField(max_length=10, validators=[CED_Tools.tools.Functions.birhdayValidator], verbose_name='Date de naissance')),
                ('lieu_naissance', models.CharField(max_length=255, verbose_name='Lieu de naissance')),
                ('nom_ar', models.CharField(max_length=100)),
                ('prenom_ar', models.CharField(max_length=100)),
                ('lieu_naissance_ar', models.CharField(max_length=255)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('ville', models.CharField(max_length=100)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email_ac', models.EmailField(blank=True, max_length=255, null=True)),
                ('email_pr', models.EmailField(blank=True, max_length=255, null=True)),
                ('handicap', models.BooleanField(default=False)),
                ('centre_bac', models.CharField(max_length=255)),
                ('mention_bac', models.CharField(choices=[('passable', 'Passable'), ('assez bien', 'Assez bien'), ('bien', 'Bien'), ('tres bien', 'Très bien')], max_length=10)),
                ('academie_bac', models.CharField(max_length=255)),
                ('serie_bac', models.CharField(max_length=16)),
                ('fonctionnaire', models.BooleanField(default=False)),
                ('employeur', models.CharField(blank=True, max_length=255, null=True)),
                ('profession', models.CharField(blank=True, max_length=255, null=True)),
                ('annee_bac', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='CED_Tools.annee')),
                ('pays', models.ForeignKey(default=CED_Tools.models.Pays.default_value_id, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doctorants', to='CED_Tools.pays')),
            ],
            options={
                'db_table': 'ced_doctorants',
            },
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sujet_detail', models.CharField(max_length=255)),
                ('annee', models.ForeignKey(default=CED_Tools.tools.Functions.current_year, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inscriptions', to='CED_Tools.annee')),
                ('doctorant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inscriptions', to='Etudiant.doctorant')),
                ('sujet', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inscriptions', to='Administration.sujet')),
            ],
            options={
                'db_table': 'ced_inscriptions',
            },
        ),
        migrations.CreateModel(
            name='RetraitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('intitule', models.CharField(max_length=255)),
                ('max_delais', models.IntegerField(default=3, verbose_name='Délais Maximum')),
            ],
            options={
                'verbose_name_plural': 'Types de documents à retirer',
                'db_table': 'ced_retraits_types',
            },
        ),
        migrations.CreateModel(
            name='Retrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date création')),
                ('date_retour', models.DateTimeField(blank=True, null=True)),
                ('definitif', models.BooleanField(default=False)),
                ('doctorant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='retraits', to='Etudiant.doctorant')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='retraits', to='Etudiant.retraittype')),
            ],
            options={
                'verbose_name_plural': 'Retraits',
                'db_table': 'ced_retraits',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('intitule', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('inscription', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='publications', to='Etudiant.inscription')),
            ],
            options={
                'db_table': 'ced_publications',
            },
        ),
        migrations.CreateModel(
            name='Formation_C_Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('formation_complementaire', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inscriptions', to='Administration.formationcomplementaire')),
                ('inscription', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fomations_complementaires', to='Etudiant.inscription')),
            ],
            options={
                'db_table': 'ced_FC_inscription',
            },
        ),
        migrations.CreateModel(
            name='Cursus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('specialite', models.CharField(max_length=255)),
                ('duree', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ville', models.CharField(max_length=255)),
                ('etablissement', models.CharField(max_length=255)),
                ('moyenne', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(20)])),
                ('annee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cursus', to='CED_Tools.annee')),
                ('doctorant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cursus', to='Etudiant.doctorant')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cursus', to='Etudiant.cursustype')),
            ],
            options={
                'verbose_name_plural': 'Cursus',
                'db_table': 'ced_cursus',
            },
        ),
    ]