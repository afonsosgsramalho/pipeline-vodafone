# Vodafone Stock Notification Pipeline

## Overview
This project aims to address the issue encountered with the Vodafone website, which lacked email notifications for products that were out of stock. To solve this problem, a simple pipeline was created to periodically check the availability of products and send email notifications when items come back in stock.
This products have to passed 

## Functionality
The pipeline consists of the following components:
1. **Web Scraper**: A script that periodically scrapes the Vodafone website to check the availability of specified products.
2. **Airflow**: Utilized to host the web scraping script and execute it at regular intervals.
3. **Email Notification Service**: Used SMTP to send email notifications to specified recipients when products are back in stock.

## Notes
This pipeline is designed specifically to address the stock notification issue on the Vodafone website. 
To use the env file, rename it to .env and pass you credentials there.

