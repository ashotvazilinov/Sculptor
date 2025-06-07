#html_elements.py
#bundle builder
Bundle_builder_tab = ('//span[contains(text(), "Bundle Builder")]')

#sculptor settings
Sculptor_settings_tab = ('//span[contains(text(), "Sculptor Settings")]')
Fields_and_layouts = ('//a[contains(text(), "Fields and Layouts")]')
Sculptor_settings_Product_sidebar_group_active = ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
Sculptor_settings_Product_sidebar_group_move_right = ("//div[text()='Sidebar Product Fields']//following::button[contains(@title, 'Move')][1]")
Sculptor_settings_Product_sidebar_group_move_left = ("//div[text()='Sidebar Product Fields']//following::button[contains(@title, 'Move')][2]")
Save_Button = ("(//button[contains(text(), 'Save')])[last()]")
Sculptor_settings_Save_Success_message = ("//*[text()='Configurations successfully updated']")
Sculptor_settings_Product_sidebar_group_li_count = ("(//div[normalize-space(text())='Sidebar Product Fields']/ancestor::div[contains(@part, 'dual-listbox')]//div[@class='slds-dueling-list__column slds-dueling-list__column_responsive'])[last()]//li")