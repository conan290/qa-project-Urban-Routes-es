# Automated Tests for Urban Routes

## Project Description

This project contains a suite of automated tests for the Urban Routes website, a city routes application that allows users to request taxis. The tests verify various functionalities such as route selection, taxi fares, adding a credit card, and sending messages to the driver. Additionally, they include advanced interactions such as handling counters to select ice cream and activating special options like requesting a blanket and tissues.

## Technologies and Techniques Used

- **Language**: Python
- **Test execution**: Pytest
- **Test automation**: Selenium WebDriver
- **Design pattern**: Page Object Model (POM)
- **Wait handling**: WebDriverWait to synchronize interactions with page elements.
- **Advanced DOM interaction**: Use of JavaScript to scroll to non-visible elements and execute background commands.
- **Assertions**: Result validation using assert in Python.

## Prerequisites

Before running the tests, make sure you have the following tools installed:

1. **Python 3.x**
2. **Google Chrome** (Latest version)
3. **ChromeDriver** compatible with the installed Chrome version.

Install the necessary dependencies using the following command:

pip install selenium

## Project Structure

- **main.py**: Contains the UrbanRoutesPage and TestUrbanRoutes classes that implement the tests.
- **data.py**: Contains the data used in the tests, such as URLs, addresses, phone numbers, and more.
- **README.md**: Project documentation (this file).

## Instructions to Run the Tests

### Step 1: ChromeDriver Setup

1. Download [ChromeDriver](https://sites.google.com/chromium.org/driver) and place it in an accessible folder.
2. Make sure to add the ChromeDriver directory to your PATH environment variable, or ensure that it is in the same folder as the project.

### Step 2: Running the Tests

1. Clone the repository or download the project files.
2. From a terminal, navigate to the folder containing the project.
3. Run the following command to execute the tests:

    
bash
    pytest main.py


    This will run the entire suite of automated tests. Make sure Google Chrome is closed before starting the tests, as WebDriver will open a new browser instance for each test.

### Step 3: Verifying the Results

At the end of the test execution, you will receive a report in the terminal indicating whether the tests have passed or if any have failed. You can analyze the detailed errors to troubleshoot potential issues in the tests or on the website.

