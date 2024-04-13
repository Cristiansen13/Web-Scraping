import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from postal.parser import parse_address


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def parse(address_string):
    """ Use the parse_address function from the postal.parser library to parse the address string. """
    parsed_address = parse_address(address_string)
    
    """" Initialize a dictionary to hold the components of the parsed address. """
    components = {
        "country": "",
        "region": "",
        "city": "",
        "postcode": "",
        "road": "",
        "house_number": ""
    }
    """ Iterate over the parsed address components. """
    for component_type, value in parsed_address:
        if value in components:
            components[value] = component_type
        elif value == "state":
            components["region"] = component_type
    cnt = 0
    for key, value in components.items():
        if value != "" and key != "postcode" and key != "house_number":
            cnt += 1
    if cnt == 0:
        return None
    return components

def get_html_content(domain):
    """Fetches the HTML content of a domain."""
    try:
        response = requests.get(f'https://{domain}', headers=HEADERS, timeout=3)
        return BeautifulSoup(response.text, 'html.parser').get_text()
    except Exception as e:
        print(f"Failed to retrieve information for domain '{domain}': {e}")
        return None

def clean_text(text):
    """Cleans the text content by removing extra spaces and newlines."""
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_addresses(text):
    """Extracts addresses from the text content."""
    pattern = r'\b\d{1,4}.{1,40}\d{5}\b'
    return re.findall(pattern, text)

def parse_address_components(addresses):
    """Parses the components of each address."""
    components = ['country', 'region', 'city', 'postcode', 'road', 'house_number']
    return {component: [parse(address).get(component) for address in addresses if parse(address) is not None] for component in components}
def get_domain_info(domain):
    """Fetches and processes the information of a domain."""
    html_content = get_html_content(domain)
    if html_content:
        text_content = clean_text(html_content)
        addresses = extract_addresses(text_content)
        if addresses:
            domain_info = parse_address_components(addresses)
            domain_info['Addresses'] = addresses
            return domain_info
    return None

def process_domains(domains):
    """Processes a list of domains in parallel."""
    domain_info_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        future_to_domain = {executor.submit(get_domain_info, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                domain_info = future.result()
                if domain_info:
                    domain_info['Domain'] = domain
                    domain_info_list.append(domain_info)
            except Exception as exc:
                print(f"Failed to retrieve information for domain '{domain}': {exc}")
    return domain_info_list

def main():
    """Main function to read the input data, process the domains, and save the results."""
    df = pd.read_parquet('list of company websites.snappy.parquet')
    domains = df['domain'].tolist()
    domain_info_list = process_domains(domains)
    df = pd.DataFrame(domain_info_list)
    
    columns_order = ['Domain', 'country', 'region', 'city', 'postcode', 'road', 'house_number', 'Addresses']
    df = df[columns_order]
    
    df.to_csv('domain_info.csv', index=False)


if __name__ == "__main__":
    main()