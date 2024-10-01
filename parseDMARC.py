#!/bin/python

import xml.etree.ElementTree as ET
import argparse
import gzip


def parse_dmarc_report(file_path):
    print("\n---------------------------------------------------------")
    print(f"\nParsing DMARC report: {file_path}")

    try:
        # Check if the file is compressed (.gz) or a regular XML file
        if file_path.endswith('.gz'):
            # Open and decompress the .gz file
            with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                tree = ET.parse(file)
        else:
            # Open the regular XML file
            tree = ET.parse(file_path)

        # Parse the XML tree
        root = tree.getroot()

        # Extract information from the <report_metadata> section
        report_metadata = root.find('report_metadata')
        if report_metadata is not None:
            report_id = report_metadata.find('report_id').text
            org_name = report_metadata.find('org_name').text
            email = report_metadata.find('email').text
            print(f"Report ID: {report_id}")
            print(f"Organization: {org_name}")
            print(f"Email: {email}")

        # Extract information from the <policy_published> section
        policy_published = root.find('policy_published')
        if policy_published is not None:
            domain = policy_published.find('domain').text
            policy = policy_published.find('p').text
            subdomain_policy = policy_published.find('sp').text if policy_published.find(
                'sp') is not None else 'None'

            if "reject" in policy.lower() or args.verbose:
                print(f"Domain: {domain}")
                print(f"Policy: {policy}")
                print(f"Subdomain Policy: {subdomain_policy}")


        # Extract individual records
        records = root.findall('record')
        for record in records:
            ip = record.find('row/source_ip').text
            count = record.find('row/count').text
            disposition = record.find('row/policy_evaluated/disposition').text
            dkim = record.find('row/policy_evaluated/dkim').text
            spf = record.find('row/policy_evaluated/spf').text

            if "reject" in disposition.lower() or args.verbose:
                print("\nRecord:")
                print(f"Source IP: {ip}")
                print(f"Message Count: {count}")
                print(f"Disposition: {disposition}")
                print(f"DKIM: {dkim}")
                print(f"SPF: {spf}")

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Parse DMARC XML or .gz compressed XML reports.)
    parser.add_argument('--verbose', '-v', action='store_true', default=0, help="Show passes in addition to fails.")
    parser.add_argument('files', nargs='+', help="The paths to one or more DMARC XML or .gz compressed XML files.)

    # Parse the arguments
    args = parser.parse_args()


    # Call the function to parse each DMARC report file
    for file_path in args.files:
        parse_dmarc_report(file_path)
