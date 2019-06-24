# Sample Code
The following repo contains some of the code i have written while working at Paya,
you will find examples of my Python and Powershell scripting skills.

## Powershell
In here you will find:
   * **File Finder:** This script can be run inside a server and it will scan all config file and search for matches to a 
   specific regex provided.
   * **Load Balancer Test:** Used a along another file it would perform a get a metadata page of a server and validate that sticky session are working as expected.
   * **Log Retriever:** This ps script can return log given a specific location and name or group of servers and copy them into you Desktop.

## Python
In here you will find:
   * **API Testing Automation:** This is a Behave test automation gear towards testing apis and validating their responses.
   it contains a Config file where you put all data to be used thru all of the testing.
   * **Web App Automation:** like the last one this is a behave test automation but used to simulate user interaction with a web application.
    its also capable of Creating an account and validating its own email making use of a temporary email service called Guerrilla emails
   * **Web Scraper:** Uses Selenium to Search thru BitBucket finding files that meet a given regex and then searches inside of them to find another particular Regex,
   in this case its setup to search for .config files and see if there is hard coded ips in our connections strings.
