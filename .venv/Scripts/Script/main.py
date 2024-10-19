import re
from xml.etree import ElementTree as ET
import html  # Import to handle HTML escape sequences
import os  # Import to work with file paths

# Function to read XML file
def load_xml_file(filename):
    with open(filename, 'r') as file:
        xml_content = file.read().strip()  # Strip any leading/trailing whitespace
    return xml_content

# Function to merge header and message content
def merge_header_message(header, message):
    # Get content from header and message
    header_content = header.get('content', '')
    message_content = message.get('content', '')

    # Unescape any HTML entities (e.g., &lt; becomes <)
    header_content = html.unescape(header_content)
    message_content = html.unescape(message_content)

    # Replace the <messageid> placeholder in the header with the message id1
    message_id1 = message.get('id1', '')  # Use message id1 for <messageid> placeholder
    merged_content = re.sub(r'<messageid>', message_id1, header_content)

    # Replace the !payload placeholder in the header content with the message content
    merged_content = re.sub(r'<!payload>(?:\s*:[\w\d]*)?', message_content, merged_content)

    # Remove any caret symbols (^) from the merged content
    merged_content = merged_content.replace('^', '')

    return merged_content

# Main function to process the XML and create all combinations of headers and messages
def process_xml_file(filename):
    xml_content = load_xml_file(filename)

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Split headers and messages
    headers = [elem for elem in root if elem.tag == 'HEADER']
    messages = [elem for elem in root if elem.tag == 'MESSAGE']

    # Create all combinations of headers and messages
    all_combinations = []

    for header in headers:
        for message in messages:
            # Merge each header with each message
            merged_content = merge_header_message(header.attrib, message.attrib)
            all_combinations.append({'merged_content': merged_content})

    # Generate output filename
    base_filename = os.path.basename(filename)
    output_filename = f"output_{base_filename}"

    # Write merged combinations to output file
    with open(output_filename, 'w') as output_file:
        for combo in all_combinations:
            output_file.write(f"{combo['merged_content']}\n")

    print(f"Results have been saved to {output_filename}")

# Example usage
input_filename = 'vmware_esx_esximsg.xml'  # Path to your XML file
process_xml_file(input_filename)
