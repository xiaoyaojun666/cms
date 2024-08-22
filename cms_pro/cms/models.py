from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.TextField()
    paper_url = models.TextField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Paper(models.Model):
    key_words = models.TextField()
    title = models.TextField()
    summary = models.TextField()
    published_date = models.TextField()
    authors = models.TextField()
    paper_url = models.TextField()
    pdf_path = models.TextField()
    create_time = models.TextField()

    def __str__(self):
        return self.title