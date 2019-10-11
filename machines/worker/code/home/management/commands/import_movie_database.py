from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports the Movie Database by loading the JSON dump and processing each entry against the API. Will not reload existing files'

    def handle(self, *args, **options):
        from home.file_importer import process_import_file
        processed = process_import_file(None)

        self.stdout.write("Added all movies with output %s" % processed)