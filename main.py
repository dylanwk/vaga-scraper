from parsers.attractions_parser import get_attractions
from utils.constants import EXCEL_LISTING_COLUMNS, descriptive_categories
from utils.constants import attraction_resturant_keywords as buzz_words
from models.listing import Listing, create_listing
from services.keyword_matcher import match_descriptors_nltk
from services.text_generator import create_description

import csv


csv_file_path = "modified_listings.csv"



def finalize_listings(csv_file):
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXCEL_LISTING_COLUMNS:
            print(
                f"Error: CSV columns do not match the expected columns: {EXCEL_LISTING_COLUMNS}"
            )
            return

        for i, row in enumerate(reader):

            if i < 10:
                listing = Listing(
                    title=row["title"],
                    price=row["price"],
                    link=row["link"],
                    imageSrc=row["image_URL"],
                    amenities=row["amenities"],
                    bedCount=row["bedCount"],
                    bathroomCount=row["bathCount"],
                    guestCount=row["guestCount"],
                    locationAttractions=get_attractions(
                        row["resturants"], row["attractions"]
                    ),
                    location=row["location"],
                )
                description = create_description(
                    row["location description"], row["title"], row["amenities"]
                )

                listing.description = description

                print(f"\n\n Title: {listing.title}")
                create_listing(listing)



