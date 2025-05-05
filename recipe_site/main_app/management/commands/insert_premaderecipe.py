import time
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from recipe_scrapers import scrape_html
from selenium import webdriver
from selenium.webdriver.common.by import By

from main_app.models import PremadeRecipe


class Command(BaseCommand):
    help = "Insert multiple PremadeRecipe entries into the database"

    def handle(self, *args, **options):
        cuisines = [
            "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/",
            "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/",
            "https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/",
            "https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/",
            "https://www.allrecipes.com/recipes/721/world-cuisine/european/french/",
            "https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/",
            "https://www.allrecipes.com/recipes/731/world-cuisine/european/greek/",
        ]

        driver = webdriver.Firefox()
        try:
            for cuisine_url in cuisines:
                try:
                    driver.get(cuisine_url)
                    # Adjust the element ID if needed for other cuisines
                    wrapper = driver.find_element(
                        By.ID, "mntl-taxonomysc-article-list-group_1-0"
                    )
                    class_name = "mntl-universal-card"
                    href_values = []
                    card_elements = wrapper.find_elements(By.CLASS_NAME, class_name)
                    for card in card_elements:
                        href = card.get_attribute("href")
                        if href:
                            href_values.append(href)

                    for link in href_values:
                        try:
                            driver.get(link)
                            time.sleep(1)
                            html_source = driver.page_source

                            scraper = scrape_html(html_source, link)
                            title = scraper.title()
                            nutrients = scraper.nutrients()

                            recipe = PremadeRecipe.objects.create(
                                name=title,
                                description=driver.find_element(
                                    By.CLASS_NAME, "article-subheading"
                                ).text,
                                instructions=scraper.instructions().replace(";", "\n"),
                                cook_time=scraper.cook_time(),
                                protein=float(nutrients["proteinContent"][:-2]),
                                calories=float(nutrients["calories"][:-5]),
                                fat=float(nutrients["fatContent"][:-2]),
                                carbohydrates=float(
                                    nutrients["carbohydrateContent"][:-2]
                                ),
                                ingredients="\n".join(map(str, scraper.ingredients())),
                                cuisine=cuisine_url.rstrip("/")
                                .split("/")[-1]
                                .capitalize(),
                            )

                            image_url = scraper.image()
                            if image_url:
                                response = requests.get(image_url, timeout=10)
                                if response.status_code == 200:
                                    image_name = image_url.split("/")[-1]
                                    recipe.picture.save(
                                        image_name,
                                        ContentFile(response.content),
                                        save=True,
                                    )
                            # pylint: disable=no-member
                            self.stdout.write(self.style.SUCCESS(f"Inserted: {title}"))
                        except Exception as e:
                            self.stderr.write(f"Error inserting record for {link}: {e}")
                            continue
                except Exception as e:
                    self.stderr.write(f"Error processing cuisine {cuisine_url}: {e}")
                    continue
        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")
        finally:
            driver.quit()
