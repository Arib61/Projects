from django.db import migrations

def create_rh_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='RH')

class Migration(migrations.Migration):
    dependencies = [
        ('stages', '0004_rh_user'),  # Remplacez par la dernière migration de votre application
    ]

    operations = [
        migrations.RunPython(create_rh_group),
    ]
