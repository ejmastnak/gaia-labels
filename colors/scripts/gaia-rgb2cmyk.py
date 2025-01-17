#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Used to replace RGB colors with my handpicked CMYK replacements in Gaia labels.

Reads an input CSV of the form:

```csv
# rgb_name,cmyk_name,c,m,y,k
yellow300,yellow300_cmyk,3.15403982604715,8.26886396581979,78.9806973373007,0.0
slovenia_green,slovenia_green_cmyk,47.7698939497978,3.25932707713436,98.9684901197833,0.198367284657053
```

The script:

- Gets list of document's current color palette with `scribus.getColorNames()`
- Reads through input CSV file line by line. For each line:
  - Defines new CMYK color using `defineColorCMYKFloat(cmyk_name, c, m, y, k)`
  - If `rgb_name` exists in document's color palette, uses `replaceColor(rgb_name, cmyk_name)` to replace RGB color with corresponding CMYK color

Original license:

############################

LICENSE:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Author: Sebastian Stetter

please report bugs to: scribusscript@sebastianstetter.de
"""

from __future__ import division
import sys

__version__=1.1

try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
    import scribus
except ImportError as err:
    print ("This Python script is written for the Scribus scripting interface.")
    print ("It can only be run from within Scribus.")
    sys.exit(1)

#########################
# YOUR IMPORTS GO HERE  #
#########################
import csv
import os

PROGRESS_TOTAL = 1

def rgb2cmyk(csvfile):
    scribus.statusMessage("Replacing colors...")

    colorlist = scribus.getColorNames()
    failedReplacements = []

    scribus.progressTotal(PROGRESS_TOTAL)

    # Open the CSV file
    with open(csvfile, newline='') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if len(row) != 6:
                continue
            rgb_name = row[0]
            cmyk_name = row[1]
            try:
                c = float(row[2])
                m = float(row[3])
                y = float(row[4])
                k = float(row[5])
            except ValueError:
                failedReplacements.append(row)
                continue

            scribus.defineColorCMYKFloat(cmyk_name, c, m, y, k)
            if rgb_name in colorlist:
                try:
                    scribus.replaceColor(rgb_name, cmyk_name)
                except:
                    failedReplacements.append(f"{rgb_name} -> {cmyk_name}")

    scribus.progressSet(PROGRESS_TOTAL)
    return failedReplacements


def main(argv):
    if not scribus.haveDoc() > 0:
        scribus.messageBox("csv2color", "No document to import colors \n Please open one, first.")
        sys.exit()

    csvfile = scribus.fileDialog("gaia-rgb2cmyk",  "CSV files(*.csv *.CSV *.txt *.TXT)")
    while os.path.isdir(csvfile):
        csvfile=scribus.fileDialog("gaia-rgb2cmyk",  "CSV files(*.csv *.CSV *.txt *.TXT)")

    try:
        failedReplacements = rgb2cmyk(csvfile)
        scribus.docChanged(True)
        message = "Done!"
        if len(failedReplacements) > 0:
            message += f" (with {len(failedReplacements)} errors)"
            message += "\nFailed to replace the following colors:\n{}".format("\n".join(failedReplacements))
        scribus.messageBox("gaia-rgb2cmyk", message)
    except Exception as e:
        scribus.messageBox("gaia-rgb2cmyk", "{e}".format(), icon=scribus.ICON_WARNING)
        sys.exit()



def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        #scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)
