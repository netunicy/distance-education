from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0042_alter_training_category"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Training",
            new_name="Topics",
        ),
        migrations.RenameModel(
            old_name="TrainingVideo",
            new_name="TopicsVideo",
        ),
    ]