from selenium import webdriver
import csv
import time

# Configure the driver
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')  # Open WhatsApp Web

# Wait for the user to log in and open the desired WhatsApp group
input("Press ENTER after logging in and opening the desired WhatsApp group...")

# JavaScript code to be executed in the browser console
js_code = """
function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function getNumbers() {
    a = new Set();
    for (i = 0; i < 100; i++) {
        try {
            a.add(getElementByXpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[' + i + ']/div/div/div[2]/div[2]/div[2]/span[1]/span').innerHTML);
        } catch (error) {
            try {
                a.add(getElementByXpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[' + i + ']/div/div/div[2]/div[1]/div/div/span').innerHTML);
            } catch (error) {
            }
        }
    }
    return Array.from(a);
}

function updateNumbers() {
    numbers = new Set([...numbers, ...getNumbers()]);
    if (s < 50000) {
        s += 400;
        getElementByXpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]').scrollBy(0, 400);
        setTimeout(updateNumbers, 50);
    } else {
        var cleaned_numbers = Array.from(numbers).map(function(e) {
            return e.replace(/'/g, '').replace(/-/g, '').replace(/\\+/g, '').replace(/ /g, '');
        });
        var result = cleaned_numbers.join('\\n');
        document.body.setAttribute('data-numbers', result);
    }
}

numbers = new Set();
s = 0;
updateNumbers();
"""

# Paste and execute the JavaScript code in the browser console
driver.execute_script(js_code)

# Wait for the JavaScript to finish collecting numbers
timeout = time.time() + 60  # 1 minute timeout
numbers_collected = False
while time.time() < timeout:
    # Check if the numbers are ready
    result = driver.execute_script("return document.body.getAttribute('data-numbers')")
    if result:
        numbers_collected = True
        break
    time.sleep(1)  # Wait for 1 second before checking again

# Save the output to a CSV file if numbers were collected
if numbers_collected:
    cleaned_numbers = result.split('\n')
    with open('whatsapp_numbers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for number in cleaned_numbers:
            writer.writerow([number])
    print("Numbers saved in whatsapp_numbers.csv")
else:
    print("No numbers collected or timed out")

# Close the browser
driver.quit()
