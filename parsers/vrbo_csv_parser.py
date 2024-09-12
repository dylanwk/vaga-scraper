import csv
import re
from utils.constants import relevant_amenities

input_csv = "listings_amenities_test.csv"
output_csv = "vrbo_listings_modified.csv"

""" 
Vagaspace Schema Requirements:

    Title: string
    Description: string
    LatLng: double[2] (ex: [-0.2342343, 0.9234233])
    CityCountryExact: string
    CityCountryVague: string
    CategoryOptions: string[]
    NearbyAttractions: string[]
    Amenities: string[]
    Price: int
    ListingLink: string
    GuestCount: int
    BedCount: int
    BathCount: int
    ImageSrc: string
    
"""
def parse_vrbo_listings(input_csv=input_csv, output_csv=output_csv):
    with open(input_csv, mode="r", newline="", encoding="utf-8") as infile, \
         open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            modified_row = modify_listing(row)
            writer.writerow(modified_row)

    print(f"Modifications applied on {output_csv}")


## main parser function
## parses the following:
## price, bedCount, bathCount, guestCount, location, amenities
def modify_listing(listing):
    listing["price"] = listing["price"].replace("$", "")
    listing["bedCount"] = re.sub(r"\D", "", listing["bedCount"])
    listing["bathCount"] = re.sub(r"\D", "", listing["bathCount"])
    listing["guestCount"] = re.sub(r"\D", "", listing["guestCount"])
    listing["location"] = listing["location"].replace(",", ", ")
    listing["amenities"] = filter_amenities(listing["amenities"])

    validate_bath_count(listing)
    return listing



## bathCount vailidation
def validate_bath_count(listing):
    if listing["bathCount"].startswith("0"):
        listing["bathCount"] = "1"


## standardize amenities by funneling similar 
def filter_amenities(amenities_str: str):
    amenities_list = re.split(r"\n+", amenities_str.replace("\r", "").lower())
    filtered_amenities = set()

    for amenity in amenities_list:
        standardized_amenity = amenity_lookup.get(amenity.strip())
        if standardized_amenity:
            filtered_amenities.add(standardized_amenity)

    return ", ".join(filtered_amenities)


def create_amenity_lookup(relevant_amenities: dict[str, set[str]]):
    lookup = {}
    for standard_amenity, synonyms in relevant_amenities.items():
        for synonym in synonyms:
            lookup[synonym.lower()] = standard_amenity
    return lookup

amenity_lookup = create_amenity_lookup(relevant_amenities)

if __name__ == "__main__":
    parse_vrbo_listings()
