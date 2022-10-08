from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20221007_1518'),
    ]

    operations = [
        migrations.DeleteModel(name='Title')
    ]