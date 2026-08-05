from django.utils.text import slugify


def generate_unique_slug(
    model,
    value,
    slug_field="slug",
    instance=None,
    **filters,
):
    """
    Δημιουργεί μοναδικό slug για οποιοδήποτε Django model.

    Args:
        model:
            Το model (π.χ. Training).

        value:
            Το κείμενο από το οποίο θα δημιουργηθεί το slug.

        slug_field:
            Το πεδίο του slug (προεπιλογή: "slug").

        instance:
            Το υπάρχον αντικείμενο όταν γίνεται edit.

        **filters:
            Επιπλέον φίλτρα μοναδικότητας
            (π.χ. training_content=obj.training_content)

    Returns:
        Ένα μοναδικό slug.
    """

    slug = slugify(value, allow_unicode=True)

    unique_slug = slug
    counter = 1

    queryset = model.objects.filter(**filters)

    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(**{slug_field: unique_slug}).exists():

        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug