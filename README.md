# 🌐 Domain Info Extractor

![Project Banner](https://socialify.git.ci/Cristiansen13/Web-Scraping/image?language=1&name=1&owner=1&theme=Dark)

This Python script extracts address information from a list of company websites. It utilizes web scraping techniques to fetch HTML content from each domain, then extracts and parses addresses found within the text content of the website. The parsed address components are saved into a CSV file for further analysis.

## 📚 Prerequisites

Make sure you have the following libraries installed:

- pandas
- requests
- BeautifulSoup (bs4)
- postal
- concurrent.futures

You can install these libraries using pip:

```bash
pip install pandas requests beautifulsoup4 postal
```

## 🚀 Usage

**Input Data:** Provide a list of company websites in Parquet format named 'list of company websites.snappy.parquet'. This file should contain a column named 'domain' which lists the domain names of the company websites.

**Run the Script:** Execute the `main()` function in the script. This will process the domains listed in the input file and generate a CSV file named 'domain_info.csv' containing the extracted address information.

```bash
python domain_info_extractor.py
```
## 🛠️ Description of Functions

- `parse(address_string)`: Parses the components of an address string using the `parse_address` function from the `postal.parser` library. This decision was made to leverage the parsing capabilities of the `postal` library, which is designed for handling address data efficiently.

- `get_html_content(domain)`: Fetches the HTML content of a domain using the `requests` library and extracts text content using `BeautifulSoup`. This choice was made to retrieve the textual content of the web page, which may contain address information.

- `clean_text(text)`: Cleans the text content by removing extra spaces and newlines. This step is necessary to preprocess the text content before extracting addresses, ensuring better accuracy in address extraction.

- `extract_addresses(text)`: Extracts addresses from the text content using regular expressions. Regular expressions were chosen for their flexibility and efficiency in pattern matching, suitable for extracting address patterns from textual data.

- `parse_address_components(addresses)`: Parses the components of each address using the `parse` function and returns a dictionary containing the components. This function organizes the parsed address components into a structured format for further analysis and storage.

- `get_domain_info(domain)`: Fetches and processes the information of a domain by calling the above functions. This function orchestrates the data retrieval and processing pipeline for each domain, ensuring consistency and modularity in the extraction process.

- `process_domains(domains)`: Processes a list of domains in parallel using multithreading and returns a list of domain information dictionaries. This decision was made to improve performance by fetching and processing multiple domains simultaneously, leveraging the computational resources efficiently.

- `main()`: Main function to read the input data, process the domains, and save the results into a CSV file. This function serves as the entry point of the script, coordinating the overall execution flow and handling input/output operations.

## 📝 Notes

- This script utilizes concurrent processing to speed up the extraction process by fetching and processing multiple domains simultaneously. Multithreading was chosen for its simplicity and effectiveness in handling I/O-bound tasks like web scraping.

- The output CSV file contains columns for the domain name, country, region, city, postcode, road, house number, and a list of addresses found on the website. This structured format facilitates further analysis and visualization of the extracted address information.

- The accuracy of address extraction may vary depending on the quality and structure of the web page content. The script aims to extract address patterns based on common conventions but may not capture all address instances accurately.
