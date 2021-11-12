from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.utils import file_response
from city_scrapers_core.constants import ADVISORY_COMMITTEE
from freezegun import freeze_time

from city_scrapers.spiders.chi_design import ChiDesignSpider

test_response_main = file_response(
    join(dirname(__file__), "files", "chi_design.html"),
    url="https://www.chicago.gov/city/en/depts/dcd/supp_info/committee-on-design.html",
)

test_response_meeting_august = file_response(
    join(dirname(__file__), "files", "chi_design_august.html"),
    url="https://www.chicago.gov/city/en/depts/dcd/supp_info/committee-on-design/august-2021.html",
)

test_response_meeting_september = file_response(
    join(dirname(__file__), "files", "chi_design_september.html"),
    url="https://www.chicago.gov/city/en/depts/dcd/supp_info/committee-on-design/september-2021-committee-on-design-meeting.html",
)

# test_response_meeting_october = file_response(
#     join(dirname(__file__), "files", "chi_design_october.html"),
#     url="https://www.chicago.gov/city/en/depts/dcd/supp_info/committee-on-design/october-2021.html",
# )
#
# test_response_meeting_november = file_response(
#     join(dirname(__file__), "files", "chi_design_november.html"),
#     url="https://www.chicago.gov/city/en/depts/dcd/supp_info/committee-on-design/november-2021.html",
# )

test_response_meetings = [test_response_meeting_august, test_response_meeting_september]
spider = ChiDesignSpider()

freezer = freeze_time("2021-11-11")
freezer.start()

parsed_items = [item for meeting in test_response_meetings for item in spider.parse_meeting(meeting)]

freezer.stop()


@pytest.mark.xfail(raises=AssertionError)
def test_finds_all_meetings():
    assert len(parsed_items) == 7


def test_title():
    assert parsed_items[0]["title"] == "Committee on Design"


def test_description():
    description = ('The historic Laramie Bank Building will be restored and reopened to the '
 'public with a new bank, café, Blues Museum, and business incubator space. It '
 'will be operated by a community board and profits will be reinvested into '
 'the neighborhood, building generational wealth. The vacant parcels will be '
 'redeveloped into a six-story, 76-unit residential building, with a mix of 1, '
 '2, and 3 bedroom units. Tenant amenities will include an outdoor rooftop '
 'deck, fitness room, computer room, common space on each floor and a 1st '
 'floor community room for events and social gatherings.')
    assert parsed_items[1]["description"] == description


# def test_start():
#     assert parsed_items[0]["start"] == datetime(2019, 1, 1, 0, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"


# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"


# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"


def test_location():
    assert parsed_items[1]["location"] == {
        "name": "",
        "address": "5200-5224 W. Chicago Ave.(Austin, 37th Ward)"
    }


# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


def test_classification():
    assert parsed_items[0]["classification"] == ADVISORY_COMMITTEE


# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
