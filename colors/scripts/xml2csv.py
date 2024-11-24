#!/usr/bin/env python

import sys
import csv
import xml.etree.ElementTree as ET

def xml2csv(xmlcolors):
    tree = ET.parse(xmlcolors)
    root = tree.getroot()

    csvcolors = xmlcolors.replace(".xml", ".csv")

    # Open CSV file to write
    with open(csvcolors, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Iterate through the COLOR elements and write their attributes to the CSV
        for color in root.findall('COLOR'):
            name = color.attrib['NAME']
            c = color.attrib['C']
            m = color.attrib['M']
            y = color.attrib['Y']
            k = color.attrib['K']
            writer.writerow([name.replace("_cmyk", ""), name, "{:.2f}".format(float(c)), "{:.2f}".format(float(m)), "{:.2f}".format(float(y)), "{:.2f}".format(float(k))])

    print("Conversion completed and saved to {}".format(csvcolors))

if __name__ == "__main__":

    if len(sys.argv) < 2:
            print("Usage: python xml2csv.py colors.xml")
            sys.exit(1)

    for i in range(1, len(sys.argv)):
        xmlcolors = sys.argv[i]
        xml2csv(xmlcolors)

