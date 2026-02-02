# test_Sculptor.py
import pytest
from Sculptor_Unit_Tests import *

@pytest.mark.parametrize("page2", ["0219"], indirect=True)
def test_Bundle_consists_of_three_sections(page2):
    page, unique_number = page2  # Use the page from the fixture
    Bundle_consists_of_three_sections(page, unique_number)

@pytest.mark.parametrize("page2", ["0220.1"], indirect=True)
def test_Bundle_Left_Sidebar_can_be_sorted_by_Displayed_fields(page2):
    page, unique_number = page2
    Bundle_Left_Sidebar_can_be_sorted_by_Displayed_fields(page, unique_number)

@pytest.mark.parametrize("page2", ["0220.2"], indirect=True)
def test_Bundle_Left_Sidebar_can_be_filtered_by_Displayed_fields(page2):
    page, unique_number = page2
    Bundle_Left_Sidebar_can_be_filtered_by_Displayed_fields(page, unique_number)

@pytest.mark.parametrize("page2", ["0221"], indirect=True)
def test_Bundle_Left_Sidebar_Active_grouping(page2):
    page, unique_number = page2
    Bundle_Left_Sidebar_Active_grouping(page, unique_number)