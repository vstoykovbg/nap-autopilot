import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


import time
import datetime
import re
from decimal import Decimal, InvalidOperation, DecimalException, ROUND_HALF_UP
from napcountrysearch import get_country

bad_request_errors_global=0
bad_request_errors_global_previous=0

slow_global=False

# Подпрограма за проверка дали даден елемент със зададено ID съществува.
# Подпрограмата чака time секунди да види дали този елемент ще се появи.

def check_if_element_with_ID_exists(driver, element_id, time=3):
    try:
        WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, element_id)))
        return True
    except:
        return False

# Подпрограма за проверка дали има <h1>Bad Request</h1>

def bad_request_is_appearing(driver):

    global bad_request_errors_global
    
    # Wait for up to 1 second for the "Bad Request" to appear
    for _ in range(10):

        try:
            bad_request_h1 = driver.find_elements(By.XPATH,"//h1[contains(text(), 'Bad Request')")
        except:
            time.sleep(0.1)  # Wait for 0.1 second before checking again
            continue

        if bad_request_h1:
            bad_request_errors_global += 1
            return True

        time.sleep(0.1)  # Wait for 0.1 second before checking again

    # If the button is not found after 1 second, print a message and return False
    else:
        print("This is good - tag h1 with text Bad Request not found within 1 second.")
        return False


# Подпрограма за проверка дали има диалог за избор на задължено лице

def dialog_selection_of_taxable_person_is_appearing(driver):

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ag-cell-value')]")))
    except: # catch any exceptions
        pass

    ag_cell_value_spans = driver.find_elements(By.XPATH, "//span[contains(@class, 'ag-cell-value')]")

    if len(ag_cell_value_spans) > 0:
        return True
    else:
        return False

# Подпрограма за проверка дали съобщението за добре дошли се вижда.

def welcome_message_is_appearing(driver):
    # Wait for up to 1 second for the dialog and button to appear
    for _ in range(10):

        try:
            close_button = driver.find_elements(By.XPATH,"//button[@id='skip']")
        except:
            time.sleep(0.1)  # Wait for 0.1 second before checking again
            continue

        if close_button:
            return True  # Return True if the button exists

        time.sleep(0.1)  # Wait for 0.1 second before checking again

    # If the button is not found after 1 second, print a message and return False
    else:
        print("Button (welcome message) not found within 1 second.")
        return False



# Връща брой на ЕГН-та. Ако върне 0 броя значи в списъка няма нито едно ЕГН.
# Ако върне None значи няма изобщо списък.
# def .... / още не съм измислил как ще се казва.


# Проверява дали има списък с ЕГН-та и ако има само едно ЕГН в списъка го клика
# Ако има повече от едно ЕГН зацикля и чака потербителят да кликне за да избере ЕГН.
# При успешно кликане с изчезване на ЕГН-то връща True.
# А какво става при други обстоятелства не е много ясно, дано не се случват.
# Логиката не е много смислена, за пренаписване е.
# Но ако се ползва за потребители с права за едно ЕГН и се ползва само за избор на ЕГН-то
# с цел да се затвори диалога и да може да се продължи - върши работа.
# За потребители, които попълват декларация за физически лица с някакъв друг номер (не ЕГН)
# тази подпрограма няма да работи! Трябва да се види какво точно излиза като текст,
# за да се добави и търсене на друго име на идентификатор, примерно ЛНЧ, служебен номер (не знам как излиза).
# Трябва да има версия на автопилота, която да изчаква потребителят да се заеме с този диалог.
# Тази функция да се ползва само за версията автопилот "може би работи".
def check_and_click_egn_spans(driver):
    while True:
        try:
            # wait for the element to be present, up to 5 seconds
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'ЕГН') and contains(@class, 'ag-cell-value')]")))
        except Exception as e: # catch any exceptions
            pass
            #print(f"Error: {e}") # print the error message
            #return False # exit the function

        print("check_and_click_egn_spans debug")

        egn_spans = driver.find_elements(By.XPATH, "//span[contains(text(), 'ЕГН') and contains(@class, 'ag-cell-value')]")

        if len(egn_spans) == 1:
            egn_span = egn_spans[0]
            egn_span.click()

            try:
                WebDriverWait(driver, 10).until_not(EC.visibility_of(egn_span))
                return True
            except:
                return True
        elif len(egn_spans) > 0:
            print("Error: Too many lines with 'ЕГН' are present. Please click the appropriate line.")
            break
        else:
            print("Error: No lines with 'ЕГН' are present.")
            return False

    print("Waiting indefinitely for 'ЕГН' spans to disappear. Press Ctrl+C to interrupt.")
    while True:
        egn_spans = driver.find_elements(By.XPATH, "//span[contains(text(), 'ЕГН') and contains(@class, 'ag-cell-value')]")
        if not egn_spans:
            print("All 'ЕГН' lines have disappeared.")
            break


def how_many_EGN_spans_appear(driver):
    egn_count = 0
    
    try:

        egn_spans = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'ЕГН') and contains(@class, 'ag-cell-value')]")))

        # Count the number of elements found
        egn_count = len(egn_spans)
        
    except TimeoutException:
        print("Timed out waiting for ЕГН spans to appear.")
    except Exception as e:
        print(f"Error: {e}")
        # Additional error handling if needed
    
    return egn_count



def get_supplement_id(supplement_number):
  """
  Returns the corresponding supplement_id based on the given supplement_number.

  Args:
      supplement_number: The supplement number (integer or Roman numeral).

  Returns:
      The corresponding supplement_id (string).

  Raises:
      ValueError: If the supplement_number is out of range (not an integer between 1 and 13, or not a valid Roman numeral between "III" and "V").
      TypeError: If the supplement_number is not an integer or string.
  """

  if isinstance(supplement_number, int):
    if 1 <= supplement_number <= 13:
      # return f"part_{1159 + supplement_number}" # през 2024 година работеше
      return f"part_{1224 + supplement_number}" # корекция за 2025 година
    else:
      raise ValueError(f"Integer supplement number {supplement_number} is out of range (must be between 1 and 13)")
  elif isinstance(supplement_number, str):
    if supplement_number.upper() in ["III", "IV", "V"]:
      roman_to_int = {"III": 3, "IV": 4, "V": 5}
      # return f"part_{1154 + roman_to_int[supplement_number.upper()]}"  # през 2024 година работеше
      return f"part_{1219 + roman_to_int[supplement_number.upper()]}"  # през 2024 година работеше
    else:
      raise ValueError(f"Roman numeral supplement number '{supplement_number}' is invalid (must be one of 'III', 'IV', or 'V')")
  else:
    raise TypeError("Invalid supplement number type: must be integer or string")


def go_to_supplement(driver, supplement_number):

    try:
        supplement_id = get_supplement_id(supplement_number)
        print(f"Supplement number: {supplement_number}, Supplement ID: {supplement_id}")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return False

    try:
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[@id='{supplement_id}']/a"))
        )
        print("Element found! Sleeping for 1 second before clicking it..")
        time.sleep(1)
        
        # Scroll into view if needed
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        
        # Attempt to click using actions chain
        actions = ActionChains(driver)
        actions.move_to_element(link).click().perform()
        
        print("Link clicked!")
        
        if bad_request_is_appearing(driver):
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)
        
        return True
    except TimeoutException:
        print("Timed out waiting for element to be clickable.")
        return False
    except Exception as e:
        print("Error:", e)
        return False

def click_submit_part_button(driver):
    try:
        confirm_button_xpath = "//form[@name='submitFrm']//input[@type='button' and contains(@onclick, 'SubmitPart')]"
        
        time.sleep(0.5) # in case JS did not finished updating the yellow fields
        # Click the confirm button
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath))
        )
        confirm_button.click()
        
        return True  # Success
    except NoSuchElementException:
        print("Error: SubmitPart button not found.")
        return False



def enable_supplement(driver, supplement_number):
    if not 1 <= supplement_number <= 13:
        raise SystemExit("Error: Supplement number is out of range.")

    go_to_supplement(driver, "III")

    checkbox_name = f"dec50_part3_issetapp{supplement_number}"
    checkbox_xpath = f"//input[@name='{checkbox_name}']"

    try:
        # Check if the checkbox is already checked
        checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        if checkbox.is_selected():
            print(f"Error: Supplement {supplement_number} is already checked.")
            return True  # Already checked, return True
        
        # Check the checkbox
        checkbox.click()
        
        # Click the SubmitPart button
        if not click_submit_part_button(driver):
            print("Error: Failed to click SubmitPart button.")
            return False

        if bad_request_is_appearing(driver):
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)
        
        return True  # Success
    except NoSuchElementException:
        print(f"Error: Checkbox for supplement {supplement_number} not found.")
        return False


def check_if_row_exists(driver, row_id):
    # Function to check if a row exists
    try:
        driver.find_element(By.ID, row_id)
        return True
    except NoSuchElementException:
        return False


def check_if_row_full_owned(driver, row_id):
    # Function to check if a row is already filled with non-zero data
    try:
        # Find the input fields in the row
        count_input = driver.find_element(By.ID, f"{row_id}_count")
        price_input = driver.find_element(By.ID, f"{row_id}_price")
        price_in_currency_input = driver.find_element(By.ID, f"{row_id}_priceincurrency")
        acquiredate_input = driver.find_element(By.ID, f"{row_id}_acquiredate_display")
        
        # Get the values from the input fields
        count_value = count_input.get_attribute("value")
        price_value = price_input.get_attribute("value")
        price_in_currency_value = price_in_currency_input.get_attribute("value")
        acquiredate_value = acquiredate_input.get_attribute("value")
        
        # Check if any of the input fields contain non-zero values
        if count_value.strip() and float(count_value) != 0 or \
           price_value.strip() and float(price_value) != 0 or \
           price_in_currency_value.strip() and float(price_in_currency_value) != 0 or \
           acquiredate_value.strip() and acquiredate_value != "0":
            return True
        else:
            return False
    except NoSuchElementException:
        # If any of the input fields are not found we don't want to touch it, so we consider the row as full
        return True
    except ValueError:
        # If any of the input fields cannot be converted to float we don't want to touch it, so we consider the row as full
        return True


def check_if_row_full_dividends(driver, row_id):
    # Function to check if a row is already filled with meaningful data for dividends table
    try:
        sum_input = driver.find_element(By.ID, f"{row_id}_sum")
        name_input = driver.find_element(By.ID, f"{row_id}_name")
        paidtax_input = driver.find_element(By.ID, f"{row_id}_paidtax")
        
        # Get the values from the input fields
        sum_value = sum_input.get_attribute("value")
        name_value = name_input.get_attribute("value")
        paidtax_value = paidtax_input.get_attribute("value")
        
        # Check if any of the input fields contain meaningful non-zero data
        if (sum_value.strip() and sum_value != "0.00") or \
           name_value.strip() or \
           (paidtax_value.strip() and paidtax_value != "0.00"):
            return True
        else:
            return False
    except NoSuchElementException:
        # If any of the input fields are not found, consider the row as full
        return True


def check_if_row_full_sales(driver, row_id):
    # Function to check if a row is already filled with meaningful data for the sales table
    try:
        sellvalue_input = driver.find_element(By.ID, f"{row_id}_sellvalue")
        buyvalue_input = driver.find_element(By.ID, f"{row_id}_buyvalue")
        profit_input = driver.find_element(By.ID, f"{row_id}_profit")
        loss_input = driver.find_element(By.ID, f"{row_id}_loss")
        
        # Get the values from the input fields
        sellvalue_value = sellvalue_input.get_attribute("value")
        buyvalue_value = buyvalue_input.get_attribute("value")
        profit_value = profit_input.get_attribute("value")
        loss_value = loss_input.get_attribute("value")
        
        # Check if any of the input fields contain meaningful non-zero data
        if any(float(value.strip() or 0) != 0 for value in [sellvalue_value, buyvalue_value, profit_value, loss_value]):
            return True
        else:
            return False
    except NoSuchElementException:
        # If any of the input fields are not found, consider the row as full
        return True


def fill_income_code_v1(driver, row_id, income_code):
    # Function to select the income code from the dropdown menu
    try:
        income_code_select = Select(driver.find_element(By.ID, f"{row_id}_incomecode"))
        income_code_select.select_by_value(income_code)
        #print(f"Income code '{income_code}' selected.")
    except NoSuchElementException:
        print("Error: Income code field not found.")
    except:
        print("Error: Failed to select income code.")


def fill_dropdown_menu(driver, field_id, value, retry_attempts=10):

    attempt=0
    while True:
        attempt += 1

        print(f"DEBUG: fill_dropdown_menu: attempt: \"{attempt}\",  field_id: \"{field_id}\", value: \"{value}\"")
        
        try:
            # Wait for the dropdown element to be clickable
            dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, field_id)))

            try:
                if dropdown_element.get_attribute("value") == str(value):
                    print(f"fill_dropdown_menu: The field_id \"{field_id}\" is already with the same string value \"{value}\", we don't touch it.")
                    return True
            except Exception as e:
                print(f"Error in fill_dropdown_menu while trying to check if the field_id \"{field_id}\" is already selected: {e}")
                time.sleep(1)

            if attempt > retry_attempts:
                print("")
                print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
                print(f"fill_dropdown_menu: All attempts failed. DEBUG: retry_attempts: {retry_attempts} attempt: {attempt}")
                print("This is unusual. So we requre user confirmation to continue.")
                print("Това е необичайно. Потвърждение за продължаването на скрипта се изисква.")
                print(f"We tried to enter in \"{field_id}\" the value \"{value}\".")
                print(f"Опитахме се да въведем в \"{field_id}\" стойността \"{value}\".")
                print("Type \"stop\" and press Enter to stop the program. Напишете \"стоп\" и натиснете Enter за да спрете скрипта.")
                print("Or to continue trying again: Или за следващ опит:")
                while True:
                    user_input = input("Press Enter to try again. Натиснете Enter за да опитаме пак.")
                    if user_input == "":
                        break
                    if user_input == "стоп":
                        raise SystemExit("Скриптът спря, защото потребителят потвърди, че иска да спре.")
                    if user_input == "stop":
                        raise SystemExit("Script stopped because of user confirmation to stop.")

            #time.sleep(1)
            # Scroll the element into view, aligning it to the center of the viewport
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", dropdown_element)

            
            #time.sleep(1)
            
            #print("Click!")
            # Open the dropdown menu
            #dropdown_element.click()
            #time.sleep(1)
            
            #driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)
            
            time.sleep(0.1)

            if slow_global:
                time.sleep(1)

            if attempt > 3:
                time.sleep(0.5)

            # Wait for the dropdown options to become visible
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, field_id)))

            #input("DEBUG: fill_dropdobwn_menu - press ENTER to continiue. Checkpoint 2.")

            if attempt > 3:
                time.sleep(0.5)
                    
            # Select the value from the dropdown
            select = Select(driver.find_element(By.ID, field_id))
            select.select_by_value(value)

            if attempt > 3:
                time.sleep(0.5)
            
            #driver.execute_script("arguments[0].blur();", select)

            #select_element = driver.find_element(By.ID, field_id)

            # select_element.send_keys(Keys.TAB)
            #actions = ActionChains(driver)
            #actions.move_to_element(select_element).send_keys(Keys.TAB).perform()

            #print("Blur element...")
            #driver.execute_script("arguments[0].blur();", select_element)        
            #select_element.click()
            #select_element.send_keys(Keys.ESCAPE)
            
            print(f"Value '{value}' selected in dropdown '{field_id}'.")

            time.sleep(0.1)

            if attempt > 3:
                time.sleep(0.5)

            if slow_global:
                time.sleep(0.5)

            # Check if the selected value matches the expected value
            if select.first_selected_option.get_attribute("value") == value:
                return True
            else:
                print(f"Error: Selected value '{select.first_selected_option.get_attribute('value')}' doesn't match the expected value '{value}'.")
                continue

        except TimeoutException:
            print(f"Error: Timeout while waiting for the dropdown options in '{field_id}' to appear.")
        except NoSuchElementException:
            print(f"Error: Dropdown element or option not found in '{field_id}'.")
        except Exception as e:
            print(f"Error: {e}")

    return False



def fill_income_code_v2(driver, row_id, income_code, retry_attempts=10):
    field_id = f"{row_id}_incomecode"

    for attempt in range(retry_attempts + 1):
        if attempt > 0:
            print(f"fill_income_code: Retry attempt {attempt}...")
            time.sleep(2)

        if fill_dropdown_menu(driver, field_id, income_code):
            print(f"fill_income_code: Income code '{income_code}' successfully selected for row '{row_id}'.")
            return True

    print(f"fill_income_code: All {retry_attempts + 1} attempts failed to select income code '{income_code}' for row '{row_id}'.")
    return False


def fill_income_code(driver, row_id, income_code, retry_attempts=10):
    field_id = f"{row_id}_incomecode"

    if fill_dropdown_menu(driver, field_id, income_code, retry_attempts):
        print(f"fill_income_code: Income code '{income_code}' successfully selected for row '{row_id}'.")
        return True

    print(f"fill_income_code: fill_dropdown_menu failed to select income code '{income_code}' for row '{row_id}' in field_id '{field_id}'.")
    return False


# Затваря прозореца с инструкции за попълване, който излиза при попълване на кода на дохода
# Предишна версия, не се ползва, пази се за всеки случай (за справка).
def click_the_close_button_v1(driver):
    # Wait for up to 1 second for the dialog and button to appear
    for _ in range(10):

        try:
            close_button = driver.find_elements(By.CLASS_NAME, "ui-dialog-titlebar-close")
        except:
            time.sleep(0.1)  # Wait for 0.1 second before checking again
            continue

        if close_button:
            try:
                close_button[0].click()  # Click the first close button found
                #print("Button clicked successfully.")
                return True  # Return True if the button is clicked successfully
            except Exception as e:
                print(f"Error clicking button: {e}")
            break  # Exit the loop once the button is found and clicked
        time.sleep(0.1)  # Wait for 0.1 second before checking again

    # If the button is not found after 1 second, print a message and return False
    else:
        print("Button not found within 1 second.")
        return False

# Затваря прозореца с инструкции за попълване, който излиза при попълване на кода на дохода
def click_the_close_button(driver,timeout=1):
    # Wait for up to 1 second for the dialog and button to appear

    try:
        close_button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-dialog-titlebar-close")))

        # driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", close_button)

        # time.sleep(1) # ако не се изчака не зацепва
        time.sleep(0.1) # за всеки случай, има WebDriverWait отдолу, който трябва да чака

        # вместо sleep за всеки случай        
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-dialog-titlebar-close")))
        
        close_button.click()  # Click the first close button found
        print("click_the_close_button: Button clicked successfully.")
        return True  # Return True if the button is clicked successfully

    except TimeoutException:
        print(f"click_the_close_button: TimeoutException")
        return False
    except Exception as e:
        print(f"Error in click_the_close_button: {e}")
        return False



def click_the_close_skip_button_from_welcome_message(driver):
    # Wait for up to 1 second for the dialog and button to appear
    for _ in range(10):

        try:
            #close_button = driver.find_elements_by_xpath("//button[@id='skip']")
            #close_buttons = driver.find_elements(By.XPATH,"//button[@id='skip']")
            #close_button = close_buttons[0]
            close_button = driver.find_element(By.XPATH, "//button[@id='skip']")
        except:
            time.sleep(0.1)  # Wait for 0.1 second before checking again
            continue

        if close_button:
            try:
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", close_button)
                time.sleep(1)
            except Exception as e:
                print(f"Error scrollIntoView button: {e}")

        if close_button:
            try:
                close_button.click()  # Click the first close button found
                #print("Button clicked successfully.")
                return True  # Return True if the button is clicked successfully
            except Exception as e:
                print(f"Error clicking button: {e}")
            break  # Exit the loop once the button is found and clicked
        time.sleep(0.1)  # Wait for 0.1 second before checking again

    # If the button is not found after 1 second, print a message and return False
    else:
        print("Button not found within 1 second.")
        return False



def check_messenger_status(driver):
    try:
        #messenger_div = driver.find_element_by_id("messenger")
        messenger_div = driver.find_element(By.ID, "messenger")
        content = messenger_div.text
        print("Messenger div content:", content)
        
        # Check if the content is not only whitespace
        if content and not content.isspace():

            try:
                # Check if there is a span with id="msgr_title" and text "Вие потвърдихте успешно тази част"
                #msgr_title_span = messenger_div.find_element_by_id("msgr_title")
                msgr_title_span = messenger_div.find_element(By.ID, "msgr_title")
                if "Вие потвърдихте успешно тази част" in msgr_title_span.text:
                    return "green"

                print("The content of msgr_title_span.text is: ", msgr_title_span.text)

            except:
                print("Error while trying msgr_title_span = messenger_div.find_element(By.ID, \"msgr_title\").")

            try:
                # Check if any child div has class="error"
                #error_divs = messenger_div.find_elements_by_css_selector("div.error")
                error_divs = messenger_div.find_elements(By.CSS_SELECTOR, "div.error")
                if error_divs:
                    print("Error content:", [error_div.text for error_div in error_divs])
                    return "error"
            except:
                print("Error while trying error_divs = messenger_div.find_element(By.CSS_SELECTOR, \"div.error\").")

            try:
                # Check if there is a span with id="msgr_title" and text "Грешки при потвърждаване на частта"
                #msgr_title_span = messenger_div.find_element_by_id("msgr_title")
                msgr_title_span = messenger_div.find_element(By.ID, "msgr_title")
                if "Грешки при потвърждаване на частта" in msgr_title_span.text:
                    return "error"

                print("The content of msgr_title_span.text is: ", msgr_title_span.text)

            except:
                print("Error while trying msgr_title_span = messenger_div.find_element(By.ID, \"msgr_title\").")

            
            # If there is a div with id="messenger" but no error and no success message, return "unexpected"
            return "unexpected"
        else:
            if not content:
                print("It's an empty string")
            elif content.isspace():
                print("It's whitespace")
            else:
                print("The content is:", content)
            return "none"
    
    except NoSuchElementException:
        # If there is no div with id="messenger", return "none"
        print("check_messenger_status: NoSuchElementException")
        return "none"
    except Exception as e:
        print(f"check_messenger_status: Error: {e}")
        return "exception"

def click_and_check_messenger_hide(driver):
    try:
        # Find the div with id="messenger"
        messenger_div = driver.find_element(By.ID, "messenger")

        # Check if the messenger_div exists
        if messenger_div:
            # Search for an img with onclick="msgr.hide()"
            hide_img = messenger_div.find_element(By.XPATH, ".//img[contains(@onclick, 'msgr.hide()')]")
            
            # Check if the hide_img exists
            if hide_img:
            
                try:
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", hide_img)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error scrollIntoView hide_img in click_and_check_messenger_hide: {e}")
            
                # Click on the hide_img
                hide_img.click()

                # Wait for the hide_img to disappear
                start_time = time.time()
                while hide_img.is_displayed():
                    time.sleep(0.1)
                    if time.time() - start_time >= 2:
                        return False
    except ElementNotInteractableException as e:
        print(f"Element is not interactable: {e}")
        return True # no need to click, it's already clicked?
    except Exception as e:
        print(f"Error in click_and_check_messenger_hide:: {e}")
        return False

    return True

def is_message_no_data_present(driver):
    """Check if the specific message box about no data exists on the page."""
    try:
        # Find the dialog by class name
        # dialog = driver.find_element(By.CLASS_NAME, "ui-dialog")

        # Wait for up to 5 seconds for the dialog to appear
        dialog = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog"))
        )
        
        # Check for the title containing "Съобщение"
        title_element = dialog.find_element(By.CLASS_NAME, "ui-dialog-title")
        if "Съобщение" not in title_element.text:
            return False
        
        # Check for the specific message text in the body
        message_body = dialog.find_element(By.CLASS_NAME, "ui-dialog-content")
        if "Към настоящия момент в НАП няма постъпили данни от" not in message_body.text:
            return False
        
        # Check if the close button with class "ui-dialog-titlebar-close" exists
        close_button = dialog.find_elements(By.CLASS_NAME, "ui-dialog-titlebar-close")
        if not close_button:
            return False
        
        return True
    except Exception:
        return False

def close_message_no_data(driver):
    """Close the message box about no data if it exists."""
    if not is_message_no_data_present(driver):
        print("Message about no data from employers or income payers not found.")
        return False
    
    try:
        # Locate the close button within the dialog
        close_button = driver.find_element(By.CLASS_NAME, "ui-dialog-titlebar-close")
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", close_button)
        time.sleep(1)
        close_button.click()
        print("Message about no data from employers or income payers closed successfully.")
        return True
    except Exception as e:
        print(f"Error closing the message: {e}")
        return False


def fill_sales_code_v1(driver, row_id):
    # Function to select the income code from the dropdown menu
    try:
        code_select = Select(driver.find_element(By.ID, f"{row_id}_code"))
        code_select.select_by_value("508")

        if row_id.endswith(":1"):
            time.sleep(0.2)
            click_the_close_button(driver)


    except NoSuchElementException:
        print("Error: Sales code field not found.")
    except:
        print("Error: Failed to select sales code.")


def fill_sales_code_v2(driver, row_id):
    # Function to select the income code from the dropdown menu
    code_id = f"{row_id}_code"
    print(f"DEBUG: fill_sales_code_v2 is invoked. code_id is \"{code_id}\"")
    try:
        code_element = driver.find_element(By.ID, code_id)
        
        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 1")
            click_the_close_button(driver,0.1)
        
        # Scroll the element into view, aligning it to the center of the viewport
        try:
            print("Scroll more precisely...")
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", code_element)
        except Exception as e:
            print(f"Error scrollIntoView code_element in fill_sales_code: {e}")
        
        time.sleep(0.1)

        # code_select.click() # НЕ МОЖЕ ДА СЕ КЛИКА: AttributeError: 'Select' object has no attribute 'click'
        # time.sleep(1) # трябва да се изчака скролирането да завръши преди кликането
        # code_element.click() # може
        
        wait = WebDriverWait(driver, 5)
        # code_element = wait.until(EC.element_to_be_clickable((By.ID, f"{row_id}_code")))
        # code_element = wait.until(EC.element_to_be_clickable(code_element))
        # wait.until(EC.element_to_be_clickable(code_element))
        wait.until(EC.element_to_be_clickable((By.ID, code_id)))
        code_select = Select(code_element)
         
        code_element.click()
        
        time.sleep(0.1)
        
        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 2")
            click_the_close_button(driver,1)

        # Scroll the element into view, aligning it to the center of the viewport
        try:
            print("Scroll more precisely...")
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", code_element)
        except Exception as e:
            print(f"Error scrollIntoView code_element in fill_sales_code: {e}")
        
        code_select.select_by_value("508")

        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 2")
            click_the_close_button(driver,0.1)

        code_element.send_keys(Keys.TAB)

    except NoSuchElementException:
        print("Error in fill_sales_code: Sales code field not found.")
    except Exception as e:
        print(f"Error in fill_sales_code:: {e}")        



def fill_sales_code(driver, row_id, sales_code="508"):
    # Function to select the income code from the dropdown menu
    code_id = f"{row_id}_code"
    print(f"DEBUG: fill_sales_code is invoked. code_id is \"{code_id}\"")
    try:
        code_element = driver.find_element(By.ID, code_id)
        
        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 1")
            click_the_close_button(driver,0.1)
        
        # Scroll the element into view, aligning it to the center of the viewport
        try:
            print("Scroll...")
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", code_element)
        except Exception as e:
            print(f"Error scrollIntoView code_element in fill_sales_code: {e}")
        
        time.sleep(0.1)
        
        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.ID, code_id)))
        code_select = Select(code_element)

        if row_id.endswith(":1"):
         
            #code_element.click()

            # Create an instance of ActionChains
            actions = ActionChains(driver)

            # Click on the code_element
            actions.click(code_element)

            time.sleep(0.5) #  CRITICAL It does not work without this delay
            
            # Perform the action to click
            actions.perform()        
            
            time.sleep(0.1)
        
        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 2")
            # click_the_close_button(driver,1)
            if click_the_close_button(driver,1):
                time.sleep(5)


        # Scroll the element into view, aligning it to the center of the viewport
        try:
            print("Scroll...")
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", code_element)
        except Exception as e:
            print(f"Error scrollIntoView code_element in fill_sales_code: {e}")
        
        # code_select.select_by_value("508")
        fill_dropdown_menu(driver, code_id, sales_code)

        if row_id.endswith(":1"):
            print("DEBUG: row_id.endswith LINE 3")
            click_the_close_button(driver,0.1)

    except NoSuchElementException:
        print("Error in fill_sales_code: Sales code field not found.")
    except Exception as e:
        print(f"Error in fill_sales_code:: {e}")        



# Keep for reference
def sales_code_message_provoke_and_close_BROKEN(driver):
    field_id = "A5D2:1_code"
    
    code_select = Select(driver.find_element(By.ID, field_id))

    # Scroll into view if needed
    driver.execute_script("arguments[0].scrollIntoView(true);", code_select)

    time.sleep(5)
            
    # Attempt to click using actions chain
    actions = ActionChains(driver)
    actions.move_to_element(code_select).click().perform()

    time.sleep(5)
   
    click_the_close_button(driver)

# Keep for reference
def sales_code_message_provoke_and_close(driver):
    field_id = "A5D2:1_code"

    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.select import Select
    
    # Find the <select> element
    select_element = driver.find_element(By.ID, field_id)

    # Create a Select object
    code_select = Select(select_element)

    # Scroll into view if needed
    # driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

    # Scroll just in case
    try:
        print("Scroll...")
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", select_element)
    except Exception as e:
        print(f"Error scrollIntoView code_element in sales_code_message_provoke_and_close: {e}")


    time.sleep(0.1)
            
    # Attempt to click the <select> element using actions chain
    # actions = ActionChains(driver)
    # actions.move_to_element(select_element).click().perform()

    # Create an instance of ActionChains
    actions = ActionChains(driver)

    # Click
    actions.click(select_element)

    time.sleep(0.5) # It does not work without this delay
    
    # Perform the action to click
    actions.perform()        

    #time.sleep(0.1)
   
    return click_the_close_button(driver)

    
    

def fill_sales_code_new_do_not_work(driver, row_id, retry_attempts=4):
    field_id = f"{row_id}_code"

    sales_code="508"
    
    for attempt in range(retry_attempts + 1):
        if attempt > 0:
            print(f"Retry attempt {attempt}...")
            time.sleep(0.5)

        if fill_dropdown_menu(driver, field_id, sales_code):
            print(f"Sales code '{sales_code}' successfully selected for row '{row_id}'.")
            
            if row_id.endswith(":1"):
                time.sleep(0.2)
                click_the_close_button(driver)

            return True
    
    print(f"All {retry_attempts + 1} attempts failed to select sales code '{sales_code}' for row '{row_id}'.")

    if row_id.endswith(":1"):
        time.sleep(0.2)
        click_the_close_button(driver)

    return False



def fill_method_code(driver, row_id, method_code):
    # Function to select the method code from the dropdown menu
    try:
        method_code_select = Select(driver.find_element(By.ID, f"{row_id}_methodcode"))
        method_code_select.select_by_value(method_code)
        #print(f"Method code '{method_code}' selected.")
    except NoSuchElementException:
        print("Error: Method code field not found.")
    except:
        print("Error: Failed to select method code.")

def create_row(driver, table_type):
    # Function to create a new row in the table
    try:
        if table_type == "stocks":
            add_button_id = "A8D1"
        elif table_type == "shares":
            add_button_id = "A8D2"
        elif table_type == "dividends":
            add_button_id = "A8D5"
        elif table_type == "sales":
            add_button_id = "A5D2"
        else:
            print("Error: Invalid table type.")
            return
        
        # Construct XPath to locate the button with the specified ID and onclick attribute
        #button_xpath = f"//button[@id='{add_button_id}' and @onclick='addDynamicElement(this.id);']"
        button_xpath = f"//button[@id='{add_button_id}' and contains(@onclick, 'addDynamicElement')]"
        
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        add_button.click()
        #print("New row created.")
        return True
    except NoSuchElementException:
        print("Error in create_row: Add button not found.")
    except Exception as e:
        print(f"Error in create_row: {e}")

    return False
    


def mathematically_equal(num1, num_string):
    if num_string == "":
        return False
    try:
        return Decimal(str(num1)) == Decimal(num_string)
    except InvalidOperation:
        return False
    except Exception as e:
        print(f"Error in mathematically_equal: {e}")
        time.sleep(2)
        return False

def wait_for_input_field(driver, element_id, timeout=10):
    try:
        input_field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, element_id)))
        return input_field
    except TimeoutException:
        print(f"Error: Input field with ID '{element_id}' not visible within {timeout} seconds.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fill_input(driver, element_id, value, input_type="string", retry_attempts=20):
    if input_type not in ["string", "numerical"]:
        print("Error: Invalid input_type. Defaulting to 'string'.")
        input_type = "string"

    global slow_global

    attempt=0
    while True:
        attempt += 1

        print(f"DEBUG: fill_input: attempt: \"{attempt}\",  element_id: \"{element_id}\", value: \"{value}\"")
        
        input_field = wait_for_input_field(driver, element_id, 10)
        
        if not input_field:
            if attempt < 2:
                print(f"Error: Function fill_input failed to find element_id '{element_id}' at the first try.")
            else:
                print(f"Error: Function fill_input failed to find element_id '{element_id}' at attempt {attempt}.")
            continue

        if input_type == "string":
            if input_field.get_attribute("value") == str(value):
                if attempt == 1:
                    print("fill_input: The input field \"{element_id}\" is already with the same string value \"{value}\", we don't touch it.")
                else:
                    print(f"fill_input: String value \"{value}\" successfully entered in \"{element_id}\".")
                return True
        elif input_type == "numerical":
            if mathematically_equal(value, input_field.get_attribute("value")):
                if attempt == 1:
                    print("fill_input: The input field \"{element_id}\" is already with a mathematically identical value \"{value}\", we don't touch it.")
                else:
                    print(f"fill_input: Numerical value \"{value}\" successfully entered in \"{element_id}\".")
                return True

        try:
            if attempt > retry_attempts:
                print("")
                print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
                print(f"fill_input: All attempts failed. DEBUG: retry_attempts: {retry_attempts} attempt: {attempt}")
                print("This is unusual. So we requre user confirmation to continue.")
                print("Това е необичайно. Потвърждение за продължаването на скрипта се изисква.")
                print(f"We tried to enter in \"{element_id}\" the value \"{value}\" with type input_type \"{input_type}\".")
                print(f"Опитахме се да въведем в \"{element_id}\" стойността \"{value}\" с тип input_type \"{input_type}\".")
                print("Type \"stop\" and press Enter to stop the program. Напишете \"стоп\" и натиснете Enter за да спрете скрипта.")
                print("Or to continue trying again: Или за следващ опит:")
                while True:
                    user_input = input("Press Enter to try again. Натиснете Enter за да опитаме пак.")
                    if user_input == "":
                        break
                    if user_input == "стоп":
                        raise SystemExit("Скриптът спря, защото потребителят потвърди, че иска да спре.")
                    if user_input == "stop":
                        raise SystemExit("Script stopped because of user confirmation to stop.")

            if attempt > 1:
                print(f"In fill_input: Retry attempt {attempt}... (element_id:{element_id})")
                time.sleep(1)  # Delay before each retry attempt
                if attempt > 5:
                    time.sleep(3)

            try:
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", input_field)
                if attempt > 3:
                    time.sleep(1)
                elif slow_global:
                    time.sleep(1)
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error scrollIntoView input_field (element_id: {element_id}, attempt {attempt}): {e}")
                time.sleep(1)


            #time.sleep(0.1)

            #input_field.clear() # conflicting with ActionChains send_keys.
            
            #time.sleep(0.1)

            # Using ActionChains instead of send_keys prevents scrolling the input field to the bottom of the page.
            
            # input_field.send_keys(str(value))
            # alterantive:
            actions = ActionChains(driver)

            if (attempt > 12) and (attempt < 15):
                input_field.clear()
                input_field.send_keys(value)
                time.sleep(0.5)
                input_field.send_keys(Keys.TAB)                

                if slow_global:
                    time.sleep(0.5)

                time.sleep(0.5)
            elif attempt < 3:
                driver.execute_script("arguments[0].value = arguments[1];", input_field, value)
                if slow_global:
                    time.sleep(1)
                ActionChains(driver).click(input_field).perform()
                ActionChains(driver).send_keys(Keys.TAB).perform()

                if slow_global:
                    time.sleep(0.5)
            else:
                # Clear the input field
                actions.click(input_field).send_keys(Keys.CONTROL + "a").send_keys(Keys.DELETE)
                actions.click(input_field).send_keys(str(value))
                time.sleep(0.2) # just in case
                if slow_global:
                    time.sleep(0.2)
                actions.perform()
            
                time.sleep(0.2)  # Delay after sending keys

                if slow_global:
                    time.sleep(0.2)

                # input_field.send_keys(Keys.TAB)  # Move focus out of the input field
                # alternative
                actions.move_to_element(input_field).send_keys(Keys.TAB).perform()

                time.sleep(0.2)  # Delay after sending keys

                if slow_global:
                    time.sleep(0.3)

        except Exception as e:
            print(f"Error in fill_input: {e}")
            time.sleep(1)
    
    return False


# Тази версия на функцията изведнъж спря да работи за таблицата с дивидентите, а преди работеше.
# Интересно, че продължава да работи за таблицата с притежаваните акции и дялове.
# Проваля се когато хоризонталният скролер закрива съответното поле.
# Един от начините за решаване на проблема е като се превърти съответния елемент някъде
# по-всредата (далеч от скролерите).
# Други начини - като се променят настройките на браузъра (избрах да не ги пипам за да не се счупи
# скрипта ако при нова версия на браузъра не работят).
# Как се проемнят настройките на браузъра във връзка със скролерите:
# https://github.com/mozilla/geckodriver/issues/2013
def select_country_v1(driver, row_id, country_input):
    # Function to select the country from the dropdown menu
    dropdown_id = f"{row_id}_country"
    country = country_input

    try:
        if country_input.strip():
            got_country = get_country(country)
            if got_country is None:
                print(f"Error: Country '{country}' not found in the database, but we will try.")
            else:
                country = got_country

    except:
        print(f"Error: failed search for country '{country}' in the database.")

    try:
        country_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, dropdown_id))
        )
        country_dropdown.click()
        country_option_xpath = f"//*[@id='{dropdown_id}']/option[text()='{country}']"
        country_option = driver.find_element(By.XPATH, country_option_xpath)
        country_option.click()
        #print(f"Country '{country}' selected.")
    except:
        print(f"Error: Country '{country}' not found in the dropdown menu.")


# С малка корекция спрямо v1 (вж. реда с country_option_xpath).
# Също като v1 не работи когато полето за държава е съвсем отдолу.
# Ако предварително полето за държава се премести около средата на страницата работи.
# Не трий! Ползва се от select_country() в краен случай!
def select_country_v2(driver, row_id, country_input):
    # Function to select the country from the dropdown menu
    dropdown_id = f"{row_id}_country"
    country = country_input

    try:
        if country_input.strip():
            got_country = get_country(country)
            if got_country is None:
                print(f"Error: Country '{country}' not found in the database, but we will try.")
            else:
                country = got_country

    except:
        print(f"Error: failed search for country '{country}' in the database.")

    try:
        country_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, dropdown_id))
        )
        country_dropdown.click()
        country_option_xpath = f"//*[@id='{dropdown_id}']/option[@value='{country}']"
        country_option = driver.find_element(By.XPATH, country_option_xpath)
        country_option.click()
        #print(f"Country '{country}' selected."
    except:
        print(f"Error: Country '{country}' not found in the dropdown menu.")


# Тази версия на функцията за избор на държава ползва fill_dropdown_menu.
# Не трий! Ползва се от select_country().
def select_country_v3(driver, row_id, country_input):
    # Function to select the country from the dropdown menu
    country = country_input

    try:
        if country_input.strip():
            got_country = get_country(country)
            if got_country is None:
                print(f"Error: Country '{country}' not found in the database, but we will try.")
            else:
                country = got_country

    except:
        print(f"Error: failed search for country '{country}' in the database.")

    dropdown_id = f"{row_id}_country" # for fill_dropdown_menu
    return fill_dropdown_menu(driver, dropdown_id, country)


def select_country(driver, row_id, country_input):

    if select_country_v3(driver, row_id, country_input):
        return True

    else:
        print("select_country_v3 failed, we try select_country_v2...")
        return select_country_v2(driver, row_id, country_input)

def fill_date_print_error_processing_date_and_ask():
    print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print(f"fill_date: Error processing the date.")
    print("This is unusual. So we requre user confirmation to continue.")
    print("Грешка при обработка на датата.")
    print("Това е необичайно. Потвърждение за продължаването на скрипта се изисква.")
    print("Type \"stop\" and press Enter to stop the program. Напишете \"стоп\" и натиснете Enter за да спрете скрипта.")
    print("Or to continue (without filling the date): Или за да продължим (без да въвеждаме датата):")
    while True:
        user_input = input("Press Enter to continue. Натиснете Enter за да продължим.")
        if user_input == "":
            return False
        if user_input == "стоп":
            raise SystemExit("Скриптът спря, защото потребителят потвърди, че иска да спре.")
        if user_input == "stop":
            raise SystemExit("Script stopped because of user confirmation to stop.")


def fill_date(driver, date_field_id, date_value, retry_attempts=20):
    # Function to fill date value in a hidden input field

    # Check if the date is valid
    try:
        date_value_hidden = convert_to_yyyy_mm_dd(date_value)  # Convert to "YYYY-MM-DD"
        year, month, day = map(int, date_value_hidden.split('-'))
        datetime.datetime(year, month, day)
    except ValueError:
        print(f"Error: Invalid date value '{date_value_hidden}'. Skipping filling date field '{date_field_id}'.")
        print(f"Грешка: невалидна дата.")
        return fill_date_print_error_processing_date_and_ask()
    except Exception as e:
        print(f"Error in fill_input: {e}")
        return fill_date_print_error_processing_date_and_ask()

    attempt=0
    while True:
        attempt += 1

        print(f"DEBUG: fill_date: attempt: \"{attempt}\",  date_field_id: \"{date_field_id}\", date_value_hidden: \"{date_value_hidden}\"")

        try:

            try:
                hidden_date_field = driver.find_element(By.ID, date_field_id)
            except NoSuchElementException:
                print(f"Error: Date field '{date_field_id}' not found.")
            except Exception as e:
                print(f"Error in fill_date (trying to find the element with ID '{date_field_id}'): {e}")
            
            if hidden_date_field.get_attribute("value") == str(date_value_hidden):
                if attempt == 1:
                    print("fill_date: The input field \"{fill_date}\" is already with the same string value \"{date_value_hidden}\", we don't touch it.")
                else:
                    print(f"fill_date: String value \"{date_value_hidden}\" successfully entered in \"{date_field_id}\".")

                return True

            if attempt > retry_attempts:
                print("")
                print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
                print(f"fill_date: All attempts failed. DEBUG: retry_attempts: {retry_attempts} attempt: {attempt}")
                print("This is unusual. So we requre user confirmation to continue.")
                print("Това е необичайно. Потвърждение за продължаването на скрипта се изисква.")
                print(f"We tried to enter in \"{date_field_id}\" the value \"{date_value_hidden}\".")
                print(f"Опитахме се да въведем в \"{date_field_id}\" стойността \"{date_value_hidden}\".")
                print("Type \"stop\" and press Enter to stop the program. Напишете \"стоп\" и натиснете Enter за да спрете скрипта.")
                print("Or to continue trying again: Или за следващ опит:")
                while True:
                    user_input = input("Press Enter to try again. Натиснете Enter за да опитаме пак.")
                    if user_input == "":
                        break
                    if user_input == "стоп":
                        raise SystemExit("Скриптът спря, защото потребителят потвърди, че иска да спре.")
                    if user_input == "stop":
                        raise SystemExit("Script stopped because of user confirmation to stop.")
            elif attempt > 5:
                time.sleep(1)

            try:
                date_field_id_visible = f"{date_field_id}_display"
                visible_date_field = driver.find_element(By.ID, date_field_id_visible)
                driver.execute_script("arguments[0].value = arguments[1];", visible_date_field, date_value)
                print(f"fill_date: Visible date field '{date_field_id_visible}' filled with value '{date_value}'.")
            except Exception as e:
                print(f"Error in fill_date (trying to fill the visible date): {e}")
                time.sleep(1)

            try:
                driver.execute_script(f"arguments[0].setAttribute('value', '{date_value_hidden}')", hidden_date_field)
                print(f"fill_date: Hidden date field '{date_field_id}' filled with value '{date_value_hidden}'.")
            except Exception as e:
                print(f"Error in fill_date (trying to fill the visible date): {e}")
                time.sleep(1)

        except Exception as e:
            print(f"Error in fill_date: {e}")

        time.sleep(0.5)

    return False

def convert_to_yyyy_mm_dd(date_value):
    # Convert date format from "DD.MM.YYYY" to "YYYY-MM-DD"
    parts = date_value.split('.')
    # Pad single-digit day and month values with leading zero
    day = parts[0].zfill(2)
    month = parts[1].zfill(2)
    return f"{parts[2]}-{month}-{day}"

def round_value(value, max_digits_after_decimal, field):
    # Check if the number has a decimal part
    if '.' in value:
        try:
            decimal_value = Decimal(value)
            integer_part, decimal_part = str(decimal_value).split('.')
            
            # Check if the number is already rounded
            if len(decimal_part) <= max_digits_after_decimal:
                return value
            
            # Otherwise, round the number
            rounded_value = decimal_value.quantize(Decimal('1e-{0}'.format(max_digits_after_decimal)), rounding=ROUND_HALF_UP)
            print(f"We rounded the number {value} for field {field} to {max_digits_after_decimal} digits after the decimal point. The rounded value is {rounded_value}.")
            return str(rounded_value)
        except (ValueError, DecimalException) as e:
            print(f"Error rounding value for field {field}: {e}")
            return value
    else:
        return value


def process_csv_data_owned(driver, csv_file, table_type):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        retry=0
        for row_data in csvreader:
            row_id = 1  # Start with row_id 1
            while True:
                if table_type == "stocks":
                    current_row_id = f"A8D1:{row_id}"
                elif table_type == "shares":
                    current_row_id = f"A8D2:{row_id}"
                else:
                    print("Error: Invalid table type.")
                    return

                #print("Debug (process_csv_data_owned): current_row_id: ", current_row_id)
                
                if not check_if_row_exists(driver, current_row_id):
                    if not create_row(driver, table_type):
                        print("Error in process_csv_data_owned: Error creating row for table type ", table_type)
                        retry += 1
                        print("Error in process_csv_data_owned: Something unexpected happened. We should not be here.")
                        print("   Retry: ", retry, " row_id: ", row_id)

                        if retry > 5:
                            time.sleep(10)
                            
                        if retry > 20:
                            print("Error in process_csv_data_owned: too many attempts.")
                            # return False
                            press_enter_to_continue()

                        time.sleep(5)
                
                if not check_if_row_full_owned(driver, current_row_id):
                    country = row_data.get("country")

                    if country is None:
                        country = ""
                        print("Error (process_csv_data_owned): No country specified.")

                    select_country(driver, current_row_id, country)
                    
                    # Fill other input fields if they are present in the csv file
                    if "count" in row_data:
                        count_value = row_data["count"]
                        count_value = str(round_value(count_value, 8, "count"))
                        fill_input(driver, f"{current_row_id}_count", count_value, "numerical")
                    else:
                        fill_input(driver, f"{current_row_id}_count", 0, "numerical")
                    
                    if "price_in_currency" in row_data:
                        price_in_currency_value = row_data["price_in_currency"]
                        price_in_currency_value = str(round_value(price_in_currency_value, 2, "price_in_currency"))
                        fill_input(driver, f"{current_row_id}_priceincurrency", price_in_currency_value, "numerical")
                    else:
                        fill_input(driver, f"{current_row_id}_priceincurrency", 0, "numerical")
                    
                    if "price" in row_data:
                        price_value = row_data["price"]
                        price_value = str(round_value(price_value, 2, "price"))
                        fill_input(driver, f"{current_row_id}_price", price_value, "numerical")
                    else:
                        fill_input(driver, f"{current_row_id}_price", 0, "numerical")
                    
                    if "date" in row_data:
                        # Fill hidden date field if date is present in the csv file
                        hidden_date_value = row_data["date"]
                        acquiredate_id = f"{current_row_id}_acquiredate"
                        fill_date(driver, acquiredate_id, hidden_date_value)
                    
                    break  # Exit loop after filling data
                
                else: # if the row is occupied with data we go to the next row
                    row_id += 1  # Move to the next row if current row is full

                
                
               


def process_csv_data_dividends(driver, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        retry=0
        for row_data in csvreader:
            row_id = 1  # Start with row_id 1

            sum_value = row_data.get("sum")

            if sum_value is None:
                print("No sum specified, moving to the next line.")
                break  # Move to the next line if no sum is specified

            if not sum_value:
                print("No meaningful sum specified, moving to the next line.")
                break  # Move to the next line if no sum is specified

            while True:
                current_row_id = f"A8D5:{row_id}"
                #print("Debug (process_csv_data_dividends): current_row_id: ", current_row_id)

                if not check_if_row_exists(driver, current_row_id):
                    if not create_row(driver, "dividends"):
                        print("Error in process_csv_data_dividends: Error creating row for table type ", table_type)
                        retry += 1
                        print("Error in process_csv_data_dividends: Something unexpected happened. We should not be here.")
                        print("   Retry: ", retry, " row_id: ", row_id)

                        if retry > 5:
                            time.sleep(10)
                            
                        if retry > 20:
                            print("Error in process_csv_data_dividends: too many attempts.")
                            # return False
                            press_enter_to_continue()

                        time.sleep(5)


                if not check_if_row_full_dividends(driver, current_row_id):


                    name_value = row_data.get("name", "")
                    name_value = name_value.strip() # cleaning whitespace at the beginning and at the end
                    country_value = row_data.get("country", "")
                    paidtax_value = row_data.get("paidtax", "0")

                    if country_value is None:
                        country = ""
                        print("Error: No country specified.")

                    if name_value is None:
                        name_value = ""
                        print("Error: No name specified.")

                    #print("DEBUG: paidtax_value (before if):", paidtax_value)
                    if paidtax_value is None or paidtax_value == "":
                       paidtax_value = "0.00"

                    if len(name_value) > 200:
                        print("Error: Name is too long: ",name_value)

                        # Truncating the name_value to 200 symbols
                        name_value = name_value[:200]

                        # Printing the new version
                        print("Truncated to 200 symbols:", name_value)

                    # измествам най-горе кода на дохода нарочно
                    fill_income_code(driver, current_row_id, "8141")

                    #input("DEBUG: checkpoing 1D    press enter to continue")
                    
                    fill_input(driver, f"{current_row_id}_name", str(name_value), "string")

                    #input("DEBUG: checkpoing 2D    press enter to continue")

                    select_country(driver, current_row_id, country_value)

                    #input("DEBUG: checkpoing 3D    press enter to continue")
                    
                    #print("DEBUG: paidtax_value:", paidtax_value)
                    rounded_paidtax_value = round_value(str(paidtax_value), 2, "paidtax")
                    methodcode_value = "1" if Decimal(rounded_paidtax_value) > Decimal('0') else "3"
                    fill_method_code(driver, current_row_id, methodcode_value)

                    # Check and round numerical values with more than two decimal points
                    rounded_sum_value = round_value(sum_value, 2, "sum")

                    fill_input(driver, f"{current_row_id}_sum", str(rounded_sum_value), "numerical")
                    fill_input(driver, f"{current_row_id}_value", "0.00", "numerical")
                    fill_input(driver, f"{current_row_id}_paidtax", str(rounded_paidtax_value), "numerical")

                    if Decimal(rounded_paidtax_value) > Decimal('0'):
                        permitedtax_value = (Decimal('0.05') * Decimal(rounded_sum_value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                        fill_input(driver, f"{current_row_id}_permitedtax", str(permitedtax_value), "numerical")

                        tax_value = min(permitedtax_value, Decimal(rounded_paidtax_value))
                        fill_input(driver, f"{current_row_id}_tax", str(tax_value), "numerical")

                        owetax_value = max(Decimal('0'), permitedtax_value - Decimal(rounded_paidtax_value))
                        fill_input(driver, f"{current_row_id}_owetax", str(owetax_value), "numerical")
                    else:
                        fill_input(driver, f"{current_row_id}_permitedtax", "0", "numerical")
                        fill_input(driver, f"{current_row_id}_tax", "0", "numerical")

                        owetax_value = (Decimal('0.05') * Decimal(rounded_sum_value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                        fill_input(driver, f"{current_row_id}_owetax", str(owetax_value), "numerical")

                    break  # Exit loop after filling data

                row_id += 1  # Move to the next row if current row is full


def process_csv_data_sales(driver, csv_file, sales_code="508"):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row_data in csvreader:
            row_id = 1  # Start with row_id 1
            while True:
                current_row_id = f"A5D2:{row_id}"

                if not check_if_row_exists(driver, current_row_id):
                    create_row(driver, "sales")
                print("Debug: current_row_id: ", current_row_id)

                if not check_if_row_full_sales(driver, current_row_id):
                    sellvalue_value = row_data.get("sellvalue", "0")
                    buyvalue_value = row_data.get("buyvalue", "0")
                    profit_value = row_data.get("profit", "0")
                    loss_value = row_data.get("loss", "0")
                    if (not sellvalue_value) and (not buyvalue_value):
                        print("No buy and sell value specified, moving to the next line.")
                        break  # Move to the next line if no buy and sell value is specified

                    if sellvalue_value is None:
                        sellvalue_value = "0.00"

                    if buyvalue_value is None:
                        buyvalue_value = "0.00"

                    if profit_value == "":
                        profit_value = None

                    if loss_value == "":
                        loss_value = None


                    if (profit_value is None) and (loss_value is None):

                        # BEGIN processing old version

                        if float(sellvalue_value.strip() or '0') == 0 and float(buyvalue_value.strip() or '0') == 0:
                            print("No meaningful (non-zero) buy and sell value specified, moving to the next line.")
                            break  # Move to the next line if both buy and sell values are zero

                        rounded_sellvalue_value = round_value(sellvalue_value, 2, "sellvalue")
                        rounded_buyvalue_value = round_value(buyvalue_value, 2, "buyvalue")

                        if (Decimal(rounded_sellvalue_value) == Decimal('0')) and (Decimal(rounded_buyvalue_value) == Decimal('0')):
                            print("Values are too small. Buy, sell values: ", buyvalue_value, "," , sellvalue_value)
                            break  # Move to the next line if both buy and sell values are too small

                        fill_sales_code(driver, current_row_id, sales_code)

                        fill_input(driver, f"{current_row_id}_sellvalue", str(rounded_sellvalue_value), "numerical")
                        fill_input(driver, f"{current_row_id}_buyvalue", str(rounded_buyvalue_value), "numerical")

                        if Decimal(rounded_sellvalue_value) > Decimal(rounded_buyvalue_value): # profit

                            profit_value = Decimal(rounded_sellvalue_value) - Decimal(rounded_buyvalue_value)
                            fill_input(driver, f"{current_row_id}_profit", str(profit_value), "numerical")
                            fill_input(driver, f"{current_row_id}_loss", "0.00", "numerical")

                        elif Decimal(rounded_sellvalue_value) < Decimal(rounded_buyvalue_value): # loss

                            loss_value = Decimal(rounded_buyvalue_value) - Decimal(rounded_sellvalue_value)
                            fill_input(driver, f"{current_row_id}_profit", "0.00", "numerical")
                            fill_input(driver, f"{current_row_id}_loss", str(loss_value), "numerical")

                        elif Decimal(rounded_sellvalue_value) == Decimal(rounded_buyvalue_value): # equal

                            fill_input(driver, f"{current_row_id}_profit", "0.00", "numerical")
                            fill_input(driver, f"{current_row_id}_loss", "0.00", "numerical")

                        else:
                            print("This does not make sense. Something is wrong. Buy, sell values: ", buyvalue_value, "," , sellvalue_value)
                            break  # Move to the next line if unexpected glitch happens

                        # END processing old version
                    else:
                        # BEGIN processing new version

                        if profit_value is None:
                            profit_value = "0.00"

                        if loss_value is None:
                            loss_value = "0.00"

                        print(f"DEBUG: profit_value: '{profit_value}'")
                        print(f"DEBUG: loss_value: '{loss_value}'")
                        rounded_sellvalue_value = round_value(sellvalue_value, 2, "sellvalue")
                        rounded_buyvalue_value = round_value(buyvalue_value, 2, "buyvalue")
                        rounded_profit_value = round_value(profit_value, 2, "profit")
                        rounded_loss_value = round_value(loss_value, 2, "loss")

                        if (Decimal(rounded_sellvalue_value) < Decimal('0')):
                            print("Negative sellvalue detected, we make it zero.")
                            rounded_sellvalue_value = "0.00"

                        if (Decimal(rounded_buyvalue_value) < Decimal('0')):
                            print("Negative buyvalue detected, we make it zero.")
                            rounded_buyvalue_value = "0.00"

                        if (Decimal(rounded_profit_value) < Decimal('0')):
                            print("Negative profit detected, we make it zero.")
                            rounded_profit_value = "0.00"

                        if (Decimal(rounded_loss_value) < Decimal('0')):
                            print("Negative loss detected, we make it zero.")
                            rounded_loss_value = "0.00"

                        if (Decimal(rounded_sellvalue_value) == Decimal('0')) and (Decimal(rounded_buyvalue_value) == Decimal('0')):
                            if (Decimal(rounded_profit_value) == Decimal('0')) and (Decimal(rounded_loss_value) == Decimal('0')):
                                print("Zeroes for all columns do not make sense. We are ignoring this line.")
                                break  # Move to the next line if both buy and sell values are too small

                        if (Decimal(rounded_sellvalue_value) - Decimal(rounded_buyvalue_value)) == (Decimal(rounded_profit_value) - Decimal(rounded_loss_value)):
                            print("Values (sell/buy/profit/loss) are mathematically sound.")
                        else:
                            print("Values (sell/buy/profit/loss) are NOT mathematically sound.")
                            print("We are ignoring these values.")
                            break # Move to the next line if the values are not mathematically sound.


                        fill_sales_code(driver, current_row_id, sales_code)

                        fill_input(driver, f"{current_row_id}_sellvalue", str(rounded_sellvalue_value), "numerical")
                        fill_input(driver, f"{current_row_id}_buyvalue", str(rounded_buyvalue_value), "numerical")
                        fill_input(driver, f"{current_row_id}_profit", str(rounded_profit_value), "numerical")
                        fill_input(driver, f"{current_row_id}_loss", str(rounded_loss_value), "numerical")


                        # END processing new version


                    break  # Exit loop after filling data

                row_id += 1  # Move to the next row if current row is full



def categorize_csv_files(directory):
    """
    Categorize CSV files in the given directory based on their content.

    Args:
        directory (str): Path to the directory containing the CSV files.

    Returns:
        tuple: A tuple containing lists of CSV files categorized as shares, stocks, dividends, sales, crypto and other.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return None, None, None, None, None, None

    # Initialize empty dictionaries to store file types
    shares_files = {}
    stocks_files = {}
    dividends_files = {}
    sales_files = {}
    crypto_files = {}
    other_files = {}

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)

            # Read the first row of the CSV file to check headers
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader, None)

                # Check if the headers match any known types
                if headers:
                    if "country" in headers and "count" in headers and "date" in headers \
                            and "price_in_currency" in headers and "price" in headers:
                        if "shares" in filename:
                            shares_files[filename] = file_path
                        else:
                            stocks_files[filename] = file_path
                    elif "name" in headers and "country" in headers and "sum" in headers:
                        dividends_files[filename] = file_path
                    elif "sellvalue" in headers and "buyvalue" in headers and "profit" in headers and "loss" in headers:
                    
                        filename = os.path.basename(file_path)

                        if "crypto" in filename:
                            crypto_files[filename] = file_path
                        else:
                            sales_files[filename] = file_path
                    else:
                        other_files[filename] = file_path
                else: # a file without header is also considered other
                    other_files[filename] = file_path
                
    return shares_files, stocks_files, dividends_files, sales_files, crypto_files, other_files




def validator_test():

    # Directory path relative to the script's location
    directory = os.path.join(os.path.dirname(__file__), "import")

    if validate_csv_files(directory):
        print("CSV files are valid.")



def validate_csv_files(directory):
    """
    Validate different types of CSV files in the given directory.

    Args:
        directory (str): Path to the directory containing the CSV files.

    Returns:
        bool: True if all CSV files are valid, False otherwise.
    """
    try:
        # Categorize the CSV files
        shares, stocks, dividends, sales, crypto, other = categorize_csv_files(directory)

        print("DEBUG: all found files from categorize_csv_files(directory):")
        print("shares:", shares)
        print("stocks:", stocks)
        print("dividends:", dividends)
        print("sales:", sales)
        print("crypto:", crypto)
        print("other:", other)

        errors = []

        if not any([shares, stocks, dividends, sales, crypto]):
            errors.append("No useful CSV files found in the directory.")
        else:

            # Validate shares and stocks CSV files if they exist
            if shares:
                errors.extend(validate_csv_files_shares_and_stocks(shares))

            if stocks:
                errors.extend(validate_csv_files_shares_and_stocks(stocks))

            # Validate dividends CSV files if they exist
            if dividends:
                errors.extend(validate_csv_files_dividends(dividends))

            # Validate sales CSV files if they exist
            if sales:
                errors.extend(validate_csv_files_sales(sales))
                if len(sales) > 1:
                    errors.append("More than one CSV file with sales data found in the directory.")

            # Validate crypto CSV files if they exist
            if crypto:
                errors.extend(validate_csv_files_sales(crypto))
                if len(crypto) > 1:
                    errors.append("More than one CSV file with crypto sales data found in the directory.")


        # Check if other files are present
        if other:
            errors.append("Non-recognized files are present: " + ", ".join(other))

        if errors:
            print("Validation errors:")
            for error in errors:
                print(error)
            return False
        else:
            print("All files validated successfully.")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def check_digits_after_decimal_point(value, n=2):
    """
    Check if a Decimal value has at most n digits after the decimal point,
    ignoring trailing zeroes.

    Args:
        value (Decimal): The Decimal value to check.
        n (int): The maximum number of significant digits after the decimal point.

    Returns:
        bool: True if the value satisfies the condition, False otherwise.
    """
    try:
        decimal_str = str(value)
        if '.' in decimal_str:
            integer_part, decimal_part = decimal_str.split('.')
            significant_digits_after_decimal = len(decimal_part.rstrip('0'))
            return significant_digits_after_decimal <= n
        return True  # No decimal point, so no significant digits after it
#    except InvalidOperation:
    except DecimalException:
        return False



def validate_csv_files_sales(files):
    """
    Validate sales CSV files.

    Args:
        files (dict): Dictionary where keys are file names and values are file paths.

    Returns:
        list: List of error messages encountered during validation.
    """
    errors = []
    separator = '-' * 50  # Define separator once
    try:
        for file_name, file_path in files.items():
            print(f"Validating {file_path}")
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Check if the required headers are present
                required_headers = ['sellvalue', 'buyvalue', 'profit', 'loss']
                headers = csv_reader.fieldnames
                missing_headers = [header for header in required_headers if header not in headers]
                if missing_headers:
                    error_message = f"Missing headers: {', '.join(missing_headers)} in {file_path}"
                    errors.append(error_message)
                    continue

                # Track the number of lines containing numerical data
                num_data_lines = 0

                for row_num, row in enumerate(csv_reader, start=1):
                    # Increment the count of data lines
                    num_data_lines += 1

                    # Check if required fields are present and not None
                    for field in required_headers:
                        if field not in row:
                            errors.append(f"Missing field '{field}' at line {row_num} in {file_path}")
                        elif row[field] is None:
                            errors.append(f"Field '{field}' has a None value at line {row_num} in {file_path}")

                    # Additional validation rules for Decimal fields and creation of Decimal values
                    decimal_fields = ['sellvalue', 'buyvalue', 'profit', 'loss']
                    field_decimal_values = {}
                    for field in decimal_fields:
                        field_value = row.get(field)
                        if field_value is not None:
                            try:
                                field_decimal_values[field] = Decimal(field_value)
                                if not check_digits_after_decimal_point(field_decimal_values[field]):
                                    errors.append(f"Value '{field_value}' for field '{field}' does not have at most 2 significant digits after the decimal point at line {row_num} in {file_path}")
                                if field_decimal_values[field] < 0:
                                    errors.append(f"Negative value '{field_value}' found for field '{field}' at line {row_num} in {file_path}")
                            except DecimalException:
                                errors.append(f"Invalid value '{field_value}' for field '{field}' at line {row_num} in {file_path}")
                        else:
                            errors.append(f"Missing value for '{field}' field at line {row_num} in {file_path}")

                    # Use the Decimal values in validation logic
                    if field_decimal_values.get('profit') is not None and field_decimal_values.get('sellvalue') is not None and field_decimal_values['profit'] > 0 and field_decimal_values['sellvalue'] <= 0:
                        errors.append(f"Profit is positive but sellvalue is not positive at line {row_num} in {file_path}")
                    if field_decimal_values.get('profit') is not None and field_decimal_values['profit'] <= 0 and field_decimal_values.get('sellvalue') is not None and field_decimal_values['sellvalue'] > 0:
                        errors.append(f"Profit is not positive but sellvalue is positive at line {row_num} in {file_path}")
                    if field_decimal_values.get('profit') is not None and field_decimal_values.get('sellvalue') is not None and field_decimal_values.get('buyvalue') is not None and field_decimal_values['profit'] > 0 and field_decimal_values['sellvalue'] > 0 and field_decimal_values['buyvalue'] > field_decimal_values['sellvalue']:
                        errors.append(f"Profit is positive but buyvalue is greater than sellvalue at line {row_num} in {file_path}")

                    # New validation rule: (sellvalue - buyvalue) should be equal to (profit - loss)
                    if 'sellvalue' in field_decimal_values and 'buyvalue' in field_decimal_values and 'profit' in field_decimal_values and 'loss' in field_decimal_values:
                        if field_decimal_values['sellvalue'] - field_decimal_values['buyvalue'] != field_decimal_values['profit'] - field_decimal_values['loss']:
                            errors.append(f"Inconsistent values: (sellvalue - buyvalue) is not equal to (profit - loss) at line {row_num} in {file_path}")

                    # Add a separator between error messages for different lines
                    # Check if the last message is a duplicate and skip adding it
                    if errors and errors[-1] != separator:
                        errors.append(separator)

                # Check if any numerical data is present
                if num_data_lines == 0:
                    errors.append(f"No lines of numerical data found in {file_path}")

                # Check if more than one line of numerical data is present
                if num_data_lines > 1:
                    errors.append(f"More than one line of numerical data found in {file_path}")

    except Exception as e:
        errors.append(f"Error while validating sales CSV files: {e}")

    return errors


def validate_csv_files_dividends(files):
    """
    Validate dividends CSV files.

    Args:
        files (list): List of CSV files to validate.

    Returns:
        list: List of error messages encountered during validation.
    """
    errors = []
    separator = '-' * 50  # Define separator once
    try:
        for file_name, file_path in files.items():
            print(f"Validating {file_path}")
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Check if the required headers are present
                required_headers = ['name', 'country', 'sum']
                optional_header = 'paidtax'
                headers = csv_reader.fieldnames

                if not all(header in headers for header in required_headers):
                    missing_headers = [header for header in required_headers if header not in headers]
                    errors.append(f"Missing headers: {', '.join(missing_headers)} in {file_path}")
                    continue

                # Track the number of lines containing numerical data
                num_data_lines = 0

                for row_num, row in enumerate(csv_reader, start=1):
                    # Increment the count of data lines
                    num_data_lines += 1

                    # Check if required fields are present and not None
                    for field in required_headers:
                        if field not in row:
                            errors.append(f"Missing field '{field}' at line {row_num} in {file_path}")
                        elif not row[field]:
                            errors.append(f"Field '{field}' is empty at line {row_num} in {file_path}")

                    # Check if the country is valid
                    this_country = row.get('country')
                    if this_country is not None and this_country.strip():
                        if get_country(this_country) is None:
                            errors.append(f"Invalid country '{this_country}' at line {row_num} in {file_path}")


                    # Additional validation rules for numerical fields and creation of Decimal values
                    numerical_fields = ['sum', 'paidtax']
                    field_decimal_values = {}
                    for field in numerical_fields:
                        field_value = row.get(field)
                        if field_value is not None:
                            try:
                                field_decimal_values[field] = Decimal(field_value)
                                if not check_digits_after_decimal_point(field_decimal_values[field]):
                                    errors.append(f"Value '{field_value}' for field '{field}' does not have at most 2 digits after the decimal point at line {row_num} in {file_path}")
                                if field_decimal_values[field] < 0:
                                    errors.append(f"Negative value '{field_value}' found for field '{field}' at line {row_num} in {file_path}")
                            except DecimalException:
                                errors.append(f"Invalid value '{field_value}' for field '{field}' at line {row_num} in {file_path}")

                    # Check text values length
                    for field in ['name', 'country']:
                        if field in row and len(row[field]) > 200:
                            errors.append(f"Length of field '{field}' exceeds 200 characters at line {row_num} in {file_path}")

                    # Add a separator between error messages for different lines
                    # Check if the last message is a duplicate and skip adding it
                    if errors and errors[-1] != separator:
                        errors.append(separator)

                # Check if any numerical data is present
                if num_data_lines == 0:
                    errors.append(f"No lines of numerical data found in {file_path}")

    except Exception as e:
        errors.append(f"Error while validating dividends CSV files: {e}")

    return errors







def validate_csv_files_shares_and_stocks(files):
    """
    Validate shares and stocks CSV files.

    Args:
        files (dict): Dictionary where keys are file names and values are file paths.

    Returns:
        list: List of error messages encountered during validation.
    """
    errors = []
    separator = '-' * 50  # Define separator once
    try:
        for file_name, file_path in files.items():
            print(f"Validating {file_path}")
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Check if the required headers are present
                required_headers = ['country', 'count', 'date', 'price_in_currency', 'price']
                headers = csv_reader.fieldnames
                missing_headers = [header for header in required_headers if header not in headers]
                if missing_headers:
                    error_message = f"Missing headers: {', '.join(missing_headers)} in {file_path}"
                    errors.append(error_message)
                    continue

                # Track the number of lines containing numerical data
                num_data_lines = 0

                for row_num, row in enumerate(csv_reader, start=1):
                    # Increment the count of data lines
                    num_data_lines += 1

                    # Check if required fields are present and not None
                    for field in required_headers:
                        if field not in row:
                            errors.append(f"Missing field '{field}' at line {row_num} in {file_path}")
                        elif row[field] is None:
                            errors.append(f"Field '{field}' has a None value at line {row_num} in {file_path}")

                    # Check if text fields are within 200 characters limit and not empty strings
                    for field in ['country', 'name']:
                        if field in row and (len(row[field]) > 200 or not row[field].strip()):
                            errors.append(f"Invalid value '{row[field]}' for field '{field}' at line {row_num} in {file_path}")

                    # Check if the country is valid
                    this_country = row.get('country')
                    if this_country is not None and this_country.strip():
                        if get_country(this_country) is None:
                            errors.append(f"Invalid country '{this_country}' at line {row_num} in {file_path}")


                    # Additional validation rules for Decimal fields and creation of Decimal values
                    decimal_fields = ['price_in_currency', 'price']
                    field_decimal_values = {}
                    for field in decimal_fields:
                        field_value = row.get(field)
                        if field_value is not None:
                            try:
                                field_decimal_values[field] = Decimal(field_value)
                                if field_decimal_values[field] < 0:
                                    errors.append(f"Negative value '{field_value}' found for field '{field}' at line {row_num} in {file_path}")
                                if field == 'price_in_currency':
                                    if not check_digits_after_decimal_point(field_decimal_values[field]):
                                        errors.append(f"Value '{field_value}' for field '{field}' does not have at most 2 digits after the decimal point at line {row_num} in {file_path}")
                                elif field == 'price':
                                    if not check_digits_after_decimal_point(field_decimal_values[field]):
                                        errors.append(f"Value '{field_value}' for field '{field}' does not have at most 2 digits after the decimal point at line {row_num} in {file_path}")
                            except DecimalException:
                                errors.append(f"Invalid value '{field_value}' for field '{field}' at line {row_num} in {file_path}")

                    # Validation for 'count' field
                    count_value = row.get('count')
                    if count_value is not None:
                        try:
                            count_decimal = Decimal(count_value)
                            if count_decimal <= 0:
                                errors.append(f"Non-positive value '{count_value}' found for field 'count' at line {row_num} in {file_path}")
                            if not check_digits_after_decimal_point(count_decimal, n=8):
                                errors.append(f"Value '{count_value}' for field 'count' does not have at most 8 digits after the decimal point at line {row_num} in {file_path}")
                        except DecimalException:
                            errors.append(f"Invalid value '{count_value}' for field 'count' at line {row_num} in {file_path}")

                    # Validation for 'date' field
                    date_value = row.get('date')
                    if date_value is not None:
                        # Check if date conforms to DD.MM.YYYY format using regex
                        if not re.match(r'\d{2}\.\d{2}\.\d{4}', date_value):
                            errors.append(f"Invalid date format '{date_value}' at line {row_num} in {file_path}")
                        else:
                            # Extract year, month, and day from the date
                            try:
                                day, month, year = map(int, date_value.split('.'))
                                datetime.datetime(year, month, day)
                            except ValueError:
                                errors.append(f"Invalid date value '{date_value}' at line {row_num} in {file_path}")

                    # Add a separator between error messages for different lines
                    # Check if the last message is a duplicate and skip adding it
                    if errors and errors[-1] != separator:
                        errors.append(separator)

                # Check if any numerical data is present
                if num_data_lines == 0:
                    errors.append(f"No lines of numerical data found in {file_path}")

    except Exception as e:
        errors.append(f"Error while validating shares and stocks CSV files: {e}")

    return errors



def click_login_submit_button(driver):
    try:
        # Find the form containing actions with "login" substring
        login_form_xpath = "//form[contains(@action, 'login')]"
        login_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_form_xpath))
        )
        
        # Find the button with type="submit" and class with substring "login" within the form
        submit_button_xpath = ".//button[@type='submit' and contains(@class, 'login')]"
        submit_button = login_form.find_element(By.XPATH, submit_button_xpath)
        
        # Click the submit button
        submit_button.click()
        
        return True  # Success
    except NoSuchElementException:
        print("Error: Login submit button not found.")
        return False


def is_login_page(driver):
    """
    Checks if the current page is likely a login page using WebDriver.

    Args:
        driver: A Selenium WebDriver instance.

    Returns:
        True if the page is likely a login page, False otherwise.
    """

    try:

        if "login" in driver.current_url.lower():
            return True

        WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, "form")))

        if "login" in driver.current_url.lower():
            return True

        #login_forms = driver.find_elements_by_xpath("//form[contains(@action, 'login')]")
        login_forms = driver.find_elements(By.XPATH, "//form[contains(@action, 'login')]")
        if len(login_forms) > 0:
            return True

    except Exception as e:
        #print(f"Failed to check login forms: {e}")
        return False

    return False


def go_to_login_and_click_login_button(driver):

    if not is_login_page(driver):
        nap_url="https://login-portal.nra.bg/auth/login"
        driver.get(nap_url)
        time.sleep(2)

    if is_login_page(driver):
        print("We are in the login page, will try to click the Login buttin automagically...")
    else:
        time.sleep(5)
        if is_login_page(driver):
            print("We are in the login page, will try to click the Login buttin automagically...")
        else:
            print("We can't load the login page.")
            return False

    if click_login_submit_button(driver):
        print("Login button clicked successfully!")
        return True
    else:
        print("Failed to click the login button.")
        return False

def we_are_somewhere_in_the_yearly_declaration_v1(driver):

    for this_ID in ['atdec_instructions', 'decContainer', 'part_1157']: 
        try:
            if driver.find_element(By.ID, this_ID):
                return True
        except:
            print("Search for an element by ID", this_ID, "failed.")

    return False

# работеше през 2024 година
def we_are_somewhere_in_the_yearly_declaration_v2(driver):
    # List of IDs to search for
    ids_to_search = ['atdec_instructions', 'decContainer', 'part_1157']

    # Wait for the elements to appear within 10 seconds
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'atdec_instructions')) and
            EC.presence_of_element_located((By.ID, 'decContainer')) and
            EC.presence_of_element_located((By.ID, 'part_1157'))
        )
        return True
    except TimeoutException:
        print("we_are_somewhere_in_the_yearly_declaration: Timed out waiting for elements to appear.")
        return False
    except Exception as e:
        print(f"Error in we_are_somewhere_in_the_yearly_declaration: {e}")
        return False
        

# v3 - корекция за 2025 година
def we_are_somewhere_in_the_yearly_declaration(driver):

    # Wait for the elements to appear within 10 seconds
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'atdec_instructions')) and
            EC.presence_of_element_located((By.ID, 'decContainer')) and
            EC.presence_of_element_located((By.ID, 'part_1221'))
        )
        return True
    except TimeoutException:
        print("we_are_somewhere_in_the_yearly_declaration: Timed out waiting for elements to appear.")
        return False
    except Exception as e:
        print(f"Error in we_are_somewhere_in_the_yearly_declaration: {e}")
        return False


def enable_supplement_and_go(driver, supplement):
    if enable_supplement(driver, supplement):
        if go_to_supplement(driver,supplement):
            return True
        else:
            return False
    else:
        return False


def manually_login_and_select_taxable_person(driver):

    while True:

        print (" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
        print ("")
        print("Please log in into the portal and make sure it works.")
        print("Close the welcome message and select the taxable person from the list.")
        print ("")
        print("Моля, влезте в портала и се убедете, че работи.")
        print("Затворете съобщението за добре дошли и изберете реда с ЕГН")
        print("от прозореца за избор на задължено лице.")
        print("След като сте готови натиснете ENTER (тук в конзолата).")

        print ("")
        input("Press ENTER after you are ready.")

        if not dialog_selection_of_taxable_person_is_appearing(driver):
            if not welcome_message_is_appearing(driver):
                if we_are_somewhere_in_the_yearly_declaration(driver):
                    return True

def ask_user_for_EGN_click_and_wait(driver):

    print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")
    print("*  *  * User action requred: Please select the appropriate ЕГН from the list (in the browser).")
    print("*  *  * Изисква се намеса на потребителя: Изберете правилното ЕГН (в браузъра).")
    print("*  *  *")
    print("*  *  * Do not type anything in the console (here), the program will know when to continue automatically.")
    print("*  *  *")
    print("*  *  * Не пишете нищо тук, програмата сама ще разбере кога да продължи.")
    print("*  *  *")
    print("*  *  * Do not type in console if not requested. Не пишете в конзолата, ако не сте подканени да го направите.")
    print("*  *  *")
    print("Waiting for the ЕГН dialog to disappear.... Чакаме диалогът за ЕГН да изчезне...")

    while True:
        if dialog_selection_of_taxable_person_is_appearing(driver):
            time.sleep(5)
        else:
            return True

def check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver):

    if dialog_selection_of_taxable_person_is_appearing(driver):

        number_of_EGNs=how_many_EGN_spans_appear(driver)

        if number_of_EGNs > 1:
            print("More than one ЕГН found in the list!")
            print("Повече от едно ЕГН е намерено в списъка!")
            ask_user_for_EGN_click_and_wait(driver)
        elif number_of_EGNs == 1:
            if check_and_click_egn_spans(driver):
                print("We clicked the line with the ЕГН successfully!")
                if dialog_selection_of_taxable_person_is_appearing(driver):
                    print("Error: The ЕГН dialog should not appear anymore.")
                    return False

        else:
            print("No ЕГНs found in the list!")
            print("Няма ЕГН-та в списъка. Това е объркващо.")
            ask_user_for_EGN_click_and_wait(driver)



def wait_and_click_submit_button_on_details_dec_50_page(driver):
    try:
        # Wait for the submit button to appear within the specified timeout (e.g., 10 seconds)
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='button-container']//span[@class='MuiButton-label' and text()='Подаване']"))
        )
        
        # Wait for the h1 element to appear with the specified text
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Приемане на Годишна данъчна декларация по чл. 50 Закон за данъците върху доходите на физическите лица №1479')]"))
        )
        
        # Click the submit button once both elements appear
        submit_button.click()
        print("Success in wait_and_click_submit_button_on_details_dec_50_page: Submit button clicked successfully.")
        return True
    
    except TimeoutException:
        print("Error in wait_and_click_submit_button_on_details_dec_50_page:Timed out waiting for elements to appear.")
        return False
    except Exception as e:
        print(f"Error in wait_and_click_submit_button_on_details_dec_50_page: {e}")
        return False


def first_attempt_v1(driver):

    nap_url="https://login-portal.nra.bg/auth/login"
    driver.get(nap_url)

    if is_login_page(driver):
        print("Waiting for the user to login.")
        print("Чакаме потребителят да се логне.")

        while True:
            time.sleep(1)
            if not is_login_page(driver):
                break


    if bad_request_is_appearing(driver):
        bad_request_errors += 1
        print("WARNING: Bad Request message is appearing.")
        time.sleep(2)


    if welcome_message_is_appearing(driver):

        print("We see the welcome message, this is expected.")

        print("1 click_the_close_skip_button_from_welcome_message(driver)....")
        if click_the_close_skip_button_from_welcome_message(driver):
            print("1 click_the_close_skip_button_from_welcome_message(driver) DONE STATUS OK")
        else:
            print("1 click_the_close_skip_button_from_welcome_message(driver) FAILED")

        time.sleep(5)
        
        #input("DEBUG point 1: press ENTER to continue")
        
        nap_url="https://portal.nra.bg/details/dec-50"
        driver.get(nap_url)

        #input("DEBUG point 2: press ENTER to continue")

        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)

        if dialog_selection_of_taxable_person_is_appearing(driver):
            print("We don't expect the dialog for taxable person now, but it's appearing. (Checkpoint 1)")
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)

        time.sleep(5)
        
        if wait_and_click_submit_button_on_details_dec_50_page(driver):
            print("We clicked Подаване button successfully.")
        else:
            print("Failed to click Подаване button. Using driver.get instead")
            nap_url="https://portal.nra.bg/home.html?s=944#/goto:DEC2009.IPUBATDEC.publicEntry"
            driver.get(nap_url)

        #input("DEBUG point 3: press ENTER to continue")

        time.sleep(5)

        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)

        if dialog_selection_of_taxable_person_is_appearing(driver):
            print("We expect the dialog for taxable person now and it's appearing. Good.")
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)
        else:
            print("We expected the dialog for taxable person, waiting some more time...")
            time.sleep(2)

            if dialog_selection_of_taxable_person_is_appearing(driver):
                print("We expect the dialog for taxable person now and it's appearing. Good.")
                check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)
            else:
                print("Dialog for taxable person did not appear when we expected it.")
                time.sleep(2)

        if we_are_somewhere_in_the_yearly_declaration(driver):
            print("Looks like we made it into the tax declaration.")
            return True
        else:
            print("Failed to go to the tax declaration.")


        nap_url="https://portal.nra.bg/details/dec-50"
        driver.get(nap_url)

        #input("DEBUG point 3: press ENTER to continue")
        
        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)

        if dialog_selection_of_taxable_person_is_appearing(driver):
            print("We don't expect the dialog for taxable person now. (Checkpoing 2)")
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)            

        if welcome_message_is_appearing(driver):
            print("We see the welcome message, this is NOT expected. (Checkpoint 1)")
            print("click_the_close_skip_button_from_welcome_message(driver)....")
            if click_the_close_skip_button_from_welcome_message(driver):
                print("click_the_close_skip_button_from_welcome_message(driver) DONE STATUS OK")
            else:
                print("click_the_close_skip_button_from_welcome_message(driver) FAILED")


        if wait_and_click_submit_button_on_details_dec_50_page(driver):
            print("We clicked Подаване button successfully.")
        else:
            print("Failed to click Подаване button. Using driver.get instead")
            nap_url="https://portal.nra.bg/home.html?s=944#/goto:DEC2009.IPUBATDEC.publicEntry"
            driver.get(nap_url)

        # input("DEBUG point 4: press ENTER to continue")

        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)

        if dialog_selection_of_taxable_person_is_appearing(driver):
            print("We don't expect the dialog for taxable person now. (Checkpoing 3)")
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)

        if welcome_message_is_appearing(driver):
            print("We see the welcome message, this is NOT expected. (Checkpoint 1)")
            print("click_the_close_skip_button_from_welcome_message(driver)....")
            if click_the_close_skip_button_from_welcome_message(driver):
                print("click_the_close_skip_button_from_welcome_message(driver) DONE STATUS OK")
            else:
                print("click_the_close_skip_button_from_welcome_message(driver) FAILED")

        if we_are_somewhere_in_the_yearly_declaration(driver):
            print("Looks like we made it into the tax declaration.")
            return True
        else:
            return False


    else:
        print("We don't see the welcome message, this is NOT expected.")
        return False



def first_attempt(driver):


    for retry in range(3):
    
        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)


        nap_url="https://portal.nra.bg/details/dec-50"
        driver.get(nap_url)

        wait_and_click_submit_button_on_details_dec_50_page(driver)
        
        if is_login_page(driver):

            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            print("Please login and after that do not touch the browser.")
            print("The automatic data entry will not work correctly if you interfere with the mouse or keyboard.")
            print("Моля влезте в системата и след това не пипайте браузъра.")
            print("Автоматичното въвеждане на данни няма да работи коректно ако въздействате на браузъра с мишката или клавиатурата.")

            print("Waiting for the user to login....")
            print("Чакаме потребителят да се логне...")


            while True:
                time.sleep(1)
                if not is_login_page(driver):
                    break


        if dialog_selection_of_taxable_person_is_appearing(driver):
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)

        if dialog_selection_of_taxable_person_is_appearing(driver):
            print("We don't expect the dialog for taxable person now. (Checkpoing 2)")
            check_if_dialog_selection_of_taxable_person_is_appearing_and_take_action(driver)            

        if bad_request_is_appearing(driver):
            bad_request_errors += 1
            print("WARNING: Bad Request message is appearing.")
            time.sleep(2)

        if we_are_somewhere_in_the_yearly_declaration(driver):
            print("Looks like we made it into the tax declaration.")
            return True
        else:
            continue


    return False

def autopilot_navigation_mode_1(driver):

    bad_request_errors=0
    
    print("The subroutine autopilot_navigation_mode_1 started.")
    time.sleep(4)


    while True:

        if first_attempt(driver):
            print("OK")
            break
        else:
            if manually_login_and_select_taxable_person(driver):
                if we_are_somewhere_in_the_yearly_declaration(driver):
                    print("Looks like we made it into the tax declaration.")
                    break
                else:
                    print("Failed to go to the tax declaration.")

def too_many_attempts_press_enter():
    print("Too many atempts. Прекалено много опити.")
    print("Натиснете Enter за да продължим с опитите.")
    print("If the portal is not working wait and go to the yearly declaration.")
    print("Ако порталът не работи изчакайте и след като заработи (преди да натиснете Enter) отидете в годишната данъчна декларация.")
    press_enter_to_continue()

def enable_supplement_and_go_with_retries(driver, supplement_number):

    if supplement_number not in [5, 8]:
        raise ValueError("Error in enable_supplement_and_go_with_retries - wrong supplement number.")

    retries=0
    while True:
        retries += 1
        
        if not we_are_somewhere_in_the_yearly_declaration(driver):
            if not first_attempt(driver):
                too_many_attempts_press_enter()
                continue

        if enable_supplement_and_go(driver,supplement_number):
            break
        else:
            if retries < 5:
                print(f"Error enabling supplement {supplement_number}. Sleeping 10 seconds and retrying.")
                print(f"Не можем да отидем в приложение {supplement_number}, след 10 секунди ще опитаме пак.")
                time.sleep(10)
            else:
                print(f"Error enabling supplement {supplement_number}.")
                print(f"Не можем да отидем в приложение {supplement_number}.")
                too_many_attempts_press_enter()

def error_SubmitPart_user_intervention():
    print("Автоматичното въвеждане не може да продължи ако данните не са запазени.")
    print("Натиснете бутона (\"Потвърди\") преди да продължим (преди да натиснете ENTER)")
    print("Бутонът (\"Потвърди\") е долу в дясно, той служи за потвърждаване (запазване) на въведените до момента данни в приложението.")
    print("(Да не го объркате с бутона за подаване на данъчната декларация.)")
    press_enter_to_continue()


# Тази функция отива в съответното приложение (и го активира ако трябва)
# и след това въвежда данните от файла.
def navigate_and_process(driver, file_path, category):

    if category == "shares":
        enable_supplement_and_go_with_retries(driver, 8)
        process_csv_data_owned(driver, file_path, "shares")
    elif category == "stocks":
        enable_supplement_and_go_with_retries(driver, 8)
        process_csv_data_owned(driver, file_path, "stocks")
    elif category == "dividends":
        enable_supplement_and_go_with_retries(driver, 8)
        process_csv_data_dividends(driver, file_path)
    elif category == "sales":
        enable_supplement_and_go_with_retries(driver, 5)
        process_csv_data_sales(driver, file_path, sales_code="508")
    elif category == "crypto":
        enable_supplement_and_go_with_retries(driver, 5)
        process_csv_data_sales(driver, file_path, sales_code="5082")
    else:
        raise("Error in navigate_and_process: Invalid category.")

    if not click_submit_part_button(driver):
        print("Error: Failed to click SubmitPart (\"Потвърди\") button. Please manually click the button to save the data.")
        print("Грешка: Неуспешно натискане на бутона SubmitPart (\"Потвърди\") за потвърждаване на въведените данни.")

        error_SubmitPart_user_intervention()

    time.sleep(4)
    status = check_messenger_status(driver)
    print("Messenger status:", status)

    if status == "green":
        print("Since the status is green we continue after some sleep...")
        time.sleep(5)
        
    elif status == "none":
        echo("We can't see the status. Probably data is not saved.")
        echo("Не може да видим статуса. Вероятно данните не са запазени.")
        error_SubmitPart_user_intervention()        
    else:
        press_enter_to_continue()

    if click_and_check_messenger_hide(driver):
        print("Button for hiding the status clicked successfully")
    else:
        print("Failed to click the button for hiding the status.")


def press_enter_to_continue():
    input("Press Enter to continue. Натиснете Enter за да продължим.")


def check_bad_request_increase(stage="middle"):

    global bad_request_errors_global_previous
    global bad_request_errors_global

    print(f"DEBUG: bad_request_errors_global_previous: {bad_request_errors_global_previous}; bad_request_errors_global: {bad_request_errors_global}")

    if bad_request_errors_global > bad_request_errors_global_previous:
        print("")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("We detected additional bad request errors.")
        print("Забелязахме увеличаване на броя на грешките bad request от последния път когато споменахме за тях.")

        print("WARNING: So far we encountered ", bad_request_errors_global, "error(s) \"Bad Request\".")
        print("Внимание: До сега се натъкнахме на ", bad_request_errors_global, "грешк{а/и} \"Bad Request\".")
        difference = bad_request_errors_global - bad_request_errors_global_previous

        print("Difference / разлика: ", difference)
        
        print("Наличието на такива грешки показва, че може би в момента системите на НАП са в режим на")
        print("профилактика или по друга причина гличват. Възможни са грешки, затова наблюдавайте внимателно")
        print("за грешна работа на скрипта или изчакайте момент когато системите на НАП ще работят нормално.")

        if stage == "final":
            print("This is the last check for new \"Bad Request\" errors; there are no more supplements to fill out.")
            print("Това е последната проверка за нови грешки \"Bad Request\"; няма повече приложения за попълване.")

        print("If you want to stop type \"stop\" and press Enter. Ако искате да спрем напишете \"стоп\" и натиснете Enter.")

        while True:
            user_input=input("Type 'ok' and press Enter to continue. Напишете 'ок' и натиснете Enter за да продължим.")
            if user_input == "ok":
                break
            if user_input == "ок":
                break
            if user_input == "stop":
                raise SystemExit("")
            if user_input == "стоп":
                raise SystemExit("")

        bad_request_errors_global_previous = bad_request_errors_global

def autopilot(mode="fast",browser="firefox"):

    global slow_global

    if mode == "slow":
        slow_global = True

    global bad_request_errors_global_previous
    global bad_request_errors_global

    # Directory path relative to the script's location
    directory = os.path.join(os.path.dirname(__file__), "import")

    if validate_csv_files(directory):
        print("CSV files are valid.")
    else:
        print("Validation errors. It's recommeded to correct the invalid data instead of continuing.")
        print("Поради грешки при валидирането потърдете, че искате да продължите")
        print("въвеждането на данните с грешки като напишете \"kamikadze\".")
        print("Има допълнителни проверки и корекции на данните, но все пак е желателно")
        print("да спрете скрипта и да коригирате данните преди следващото му пускане.")
        kamikadze = input("Enter \"kamikadze\" if you want to continue in \"kamikadze\" mode: ")
        if kamikadze == "kamikadze":
            print("We continue with the invalid data...")
        else:
            print("You did not wrote \"kamikadze\" so we stop.")
            return

    if browser == "firefox":
        driver = create_firefox_driver()
    elif browser == "chrome":
        driver = webdriver.Chrome()
        
            
    if driver == None:
        raise("Can't create Firefox driver.")


    autopilot_navigation_mode_1(driver)

    print("Checking if the message about no data from employers or income payers exists...")
    close_message_no_data(driver)

    bad_request_errors_global_previous = bad_request_errors_global

    if bad_request_errors_global > 0:
        print("WARNING: So far we encountered ", bad_request_errors_global, "error(s) \"Bad Request\".")
        print("Внимание: До сега се натъкнахме на ", bad_request_errors_global, "грешк{а/и} \"Bad Request\".")
        print("Наличието на такива грешки показва, че може би в момента системите на НАП са в режим на")
        print("профилактика или по друга причина гличват. Възможни са грешки, затова наблюдавайте внимателно")
        print("за грешна работа на скрипта или изчакайте момент когато системите на НАП ще работят нормално.")

        print("If you want to stop just press Enter. Ако искате да спрем натиснете Enter.")
        
        while True:
            user_input=input("Type 'ok' and press Enter to continue. Напишете 'ок' и натиснете Enter за да продължим.")
            if user_input == "ok":
                break
            if user_input == "ок":
                break
            if user_input == "":
                raise SystemExit("")


    # Categorize the CSV files
    shares, stocks, dividends, sales, crypto, other = categorize_csv_files(directory)

    print("DEBUG: all found files from categorize_csv_files(directory):")
    print("shares:", shares)
    print("stocks:", stocks)
    print("dividends:", dividends)
    print("sales:", sales)
    print("crypto:", crypto)
    print("other:", other)


    # process shares
    try:
        for file_name, file_path in shares.items():
            print(f"Processing {file_path}...")
            navigate_and_process(driver, file_path, "shares")

    except Exception as e:
        print(f"An error occurred while processing shares: {e}")
        print("Грешка при обработка на информацията за дяловете.")
        press_enter_to_continue()

    check_bad_request_increase()

    # process stocks
    try:
        for file_name, file_path in stocks.items():
            print(f"Processing {file_path}")
            navigate_and_process(driver, file_path, "stocks")

    except Exception as e:
        print(f"An error occurred while processing stocks: {e}")
        print("Грешка при обработка на информацията за акциите.")
        press_enter_to_continue()

    check_bad_request_increase()

    # process dividends
    try:
        for file_name, file_path in dividends.items():
            print(f"Processing {file_path}")
            navigate_and_process(driver, file_path, "dividends")

    except Exception as e:
        print(f"An error occurred while processing shares: {e}")
        print("Грешка при обработка на информацията за дяловете.")
        press_enter_to_continue()

    check_bad_request_increase()

    # process sales
    try:
        for file_name, file_path in sales.items():
            print(f"Processing {file_path}")
            navigate_and_process(driver, file_path,"sales")

    except Exception as e:
        print(f"An error occurred while processing sales: {e}")
        print("Грешка при обработка на информацията за продажбите.")
        press_enter_to_continue()


    # process crypto
    try:
        for file_name, file_path in crypto.items():
            print(f"Processing {file_path}")
            navigate_and_process(driver, file_path,"crypto")

    except Exception as e:
        print(f"An error occurred while processing crypto sales: {e}")
        print("Грешка при обработка на информацията за продажбите на криптовалути.")
        press_enter_to_continue()


    check_bad_request_increase("final")

    print("Before closing the browser it's recommended to logout (this prevents 'expired sessing' errors).")
    print("Преди да затворите браузъра е препоръчително да излезете от портала на НАП (за да се предотвратят грешки 'изтекла сесия').")
    print("Когато натиснете ENTER в конзолата браузърът ще се затвори!")
    input("Press ENTER to close the browser. Натиснете ENTER за затваряне на браузъра (когато сте готови браузърът да бъде затворен).")
    driver.close()


# https://stackoverflow.com/questions/76846675/selenium-ubuntu22-bug-message-binary-is-not-a-firefox-executable
def create_firefox_driver():

    try:

        print("Please wait, it may be slow.... Моля изчакайте, може да отнеме време...")
        driver = webdriver.Firefox()
        return driver

    except:
   
        try:

            print("Failed to launch Firefox geckodriver. Will try another way.")
            print("Please wait, it may be slow.... Моля изчакайте, може да отнеме време...")
        
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            
            geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
            driver_service = Service(executable_path=geckodriver_path)
            driver = webdriver.Firefox(service=driver_service)
            return driver
            
        except:

            try:
                print("Failed to launch Firefox geckodriver (again). Will try another way.")
                print("Please wait, it may be slow.... Моля изчакайте, може да отнеме време...")

                from selenium.webdriver.firefox.options import Options
                from selenium.webdriver.firefox.service import Service

                options = Options()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')

                geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
                driver_service = Service(executable_path=geckodriver_path)

                driver = webdriver.Firefox(options=options, service=driver_service)
                return driver
            
            except:
                try:

                    print("Failed to launch Firefox geckodriver (third time). Will try another way.")
                    print("Please wait, it may be slow.... Моля изчакайте, може да отнеме време...")                
                    
                    from selenium.webdriver.firefox.options import FirefoxOptions
                    from selenium.webdriver.firefox.service import FirefoxService
                                    
                    options = FirefoxOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')

                    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
                    driver_service = FirefoxService(executable_path=geckodriver_path)

                    driver = webdriver.Firefox(options=options, service=driver_service)

                    return driver

                except:
                    return None




if __name__ == "__main__":
    print("This is a module. Read the README.md.")
 
