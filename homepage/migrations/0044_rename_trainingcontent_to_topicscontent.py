from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0043_rename_training_to_topics"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TrainingContent",
            new_name="TopicsContent",
        ),

        migrations.RenameField(
            model_name="topicscontent",
            old_name="training",
            new_name="topics",
        ),

        migrations.RenameField(
            model_name="topicsvideo",
            old_name="training_content",
            new_name="topics_content",
        ),
    ]