#html_elements.py
#bundle builder
Bundle_builder_tab = ('//span[contains(text(), "Bundle Builder")]')
BB_Product_Name_exists = ('//span[@title="Product Name"]//span')
BB_Active_exists = ('//span[@title="Active"]//span')
BB_Price_book_needs_to_be_selected = ('//*[text()="No products created/found or pricebook wasn\'t specified"]')
BB_No_Products_were_found = ('//*[text()="No products were found."]')

#sculptor settings
Sculptor_settings_tab = ('//span[contains(text(), "Sculptor Settings")]')
Fields_and_layouts = ('//a[contains(text(), "Fields and Layouts")]')
Sculptor_settings_Product_sidebar_group_active = ("//div[@role='group' and .//*[text()='Sidebar Product Fields']]//*[text()='Active']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
Sculptor_settings_Product_sidebar_group_move_right = ("//div[text()='Sidebar Product Fields']//following::button[contains(@title, 'Move')][1]")
Sculptor_settings_Product_sidebar_group_move_left = ("//div[text()='Sidebar Product Fields']//following::button[contains(@title, 'Move')][2]")
Save_Button = ("(//button[contains(text(), 'Save')])[last()]")
Sculptor_settings_Save_Success_message = ("//*[text()='Configurations successfully updated']")
Sculptor_settings_Product_sidebar_group_li_count = ("(//div[normalize-space(text())='Sidebar Product Fields']/ancestor::div[contains(@part, 'dual-listbox')]//div[@class='slds-dueling-list__column slds-dueling-list__column_responsive'])[last()]//li")
Sculptor_settings_Product_right_sidebar_contains_active = ("(//div[normalize-space(text())='Sidebar Product Fields']/ancestor::div[contains(@part, 'dual-listbox')]//div[@class='slds-dueling-list__column slds-dueling-list__column_responsive'])[last()]//li[.//*[contains(text(), 'Active')]]")