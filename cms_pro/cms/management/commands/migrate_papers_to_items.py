from django.core.management.base import BaseCommand
from cms.models import Paper, Item, Category

class Command(BaseCommand):
    help = 'Migrate data from cms_paper to cms_item based on keywords and category'

    def add_arguments(self, parser):
        parser.add_argument('keywords', type=str, help='Keywords to search in cms_paper')

    def handle(self, *args, **kwargs):
        keywords = kwargs['keywords']

        try:
            category = Category.objects.get(name=keywords)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category with {keywords} name does not exist.'))
            return

        papers = Paper.objects.filter(key_words__icontains=keywords)
        if not papers:
            self.stdout.write(self.style.WARNING(f'No papers found with keywords "{keywords}".'))
            return

        for paper in papers:
            item = Item(
                title=paper.title,
                content=paper.summary,
                published_date=paper.published_date,
                category_id=category.id,
                paper_url=paper.paper_url
            )
            item.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully migrated Paper id {paper.id} to Item id {item.id}'))