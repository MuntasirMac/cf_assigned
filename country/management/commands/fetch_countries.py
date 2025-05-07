import requests
from django.core.management.base import BaseCommand
from country.models import Country  # Replace 'app' with your actual app name

class Command(BaseCommand):
    help = 'Populates the Country model with data from REST Countries API'

    def handle(self, *args, **kwargs):
        url = "https://restcountries.com/v3.1/all"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(f"Error fetching data: {e}")
            return

        countries = response.json()
        created, updated = 0, 0

        for item in countries:
            name = item.get("name", {}).get("common")
            official_name = item.get("name", {}).get("official")
            cca2 = item.get("cca2")
            capital = item.get("capital", [])
            area = item.get("area", 0)
            population = item.get("population", 0)
            timezones = item.get("timezones", [])
            currencies = list(item.get("currencies", {}).values())
            coat_of_arms = item.get("coatOfArms", {}).get("png", "")
            region = item.get("region", "")
            subregion = item.get("subregion", "")
            flag = item.get("flag")
            flags = item.get("flags", {}).get("png", "")
            coat_of_arms = item.get("coatOfArms", {}).get("png", "")
            languages = list(item.get("languages", {}).values())

            if not name or not cca2:
                continue

            obj, is_created = Country.objects.update_or_create(
                cca2=cca2,
                defaults={
                    "name": name,
                    "capital": capital[0] if capital else "",
                    "region": region,
                    "subregion": subregion,
                    "flag": flag,
                    "languages": languages,
                    "coat_of_arms": coat_of_arms,
                    "flags": {
                        "png": flags,
                        "svg": item.get("flags", {}).get("svg", "")
                    },
                    
                    "official_name": official_name,
                    "population": population,
                    "area": area,
                    "timezones": timezones,
                    "currencies": currencies
                }
            )

            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: {created}, Updated: {updated} countries."
        ))
