# test_main.py
import pytest
from Demo import (
    open_sculptor_cpq, create_bundle, 
    drag_and_drop_product1, drag_and_drop_product2, 
    create_opportunity, Add_Product_to_the_Opportunity, 
    click_product_if_condition_met, Create_Quote, 
    Add_Product_to_the_Quote, click_Quote_product_if_condition_met
)

@pytest.mark.parametrize("page2", [33], indirect=True) # Change "unique_number" to "page2"
def test_main(page2):
    page, unique_number = page2  # Use the page from the fixture

    
    create_bundle(page, unique_number)
    drag_and_drop_product1(page, unique_number)
    drag_and_drop_product2(page, unique_number)
    create_opportunity(page, unique_number)
    Add_Product_to_the_Opportunity(page, unique_number)
    click_product_if_condition_met(page)
    Create_Quote(page, unique_number)
    Add_Product_to_the_Quote(page, unique_number)
    click_Quote_product_if_condition_met(page)