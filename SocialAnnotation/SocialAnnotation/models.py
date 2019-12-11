from django.db import models
# Create your models here.


class SocialAnnotation(models.Model):
    ANNOTATION_TYPES = (
        ('Issue', '地域課題'),
        ('Whom', '当事者（誰が困っているのか）'),
        ('Where', '地域（場所）'),
        ('How', '取り組み'),
        ('Who', '取り組みを行っている人（誰がやっているのか）')
    )

    hypothesis_url = models.URLField()
    hypothesis_text = models.TextField()
    annotation_type = models.CharField(choices=ANNOTATION_TYPES, max_length=10)
    relevant_url = models.URLField()
