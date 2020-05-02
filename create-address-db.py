#!/usr/bin/env python

# create-address-db.py -- Bitcoin address database creator for seedrecover
# Copyright (C) 2017 Christopher Gurnee
#
# This file is part of btcrecover.
#
# btcrecover is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#
# btcrecover is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# If you find this program helpful, please consider a small
# donation to the developer at the following Bitcoin address:
#
#           3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4
#
#                      Thank You!

from __future__ import print_function


import sys
if sys.version_info <= (3, 5):
	sys.stdout.write("\n\n******************************************************************************\n\n")
	sys.stdout.write("Sorry, BTCRecover no longer supports Python2 as it is officially End-of-Life.\n\n")
	sys.stdout.write("You will need either to upgrade to at least Python 3.5 or download the final Python2 release.\n\n")
	sys.stdout.write("Note: Python2 versions of this tool are now unsupported and will not receive improvements or fixes\n\n")
	sys.stdout.write("Python2 releases and documentation for installing and using this tool with Python3 can be found at from https://github.com/3rdIteration/btcrecover.\n\n")
	sys.stdout.write("******************************************************************************\n\n")
	sys.exit(1)

from btcrecover import addressset
import argparse, atexit
from os import path

__version__ =  "1.2.0-CryptoGuide"

if __name__ == "__main__":
    print("Starting CreateAddressDB", __version__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--datadir",    metavar="DIRECTORY", help="the Bitcoin data directory (default: auto)")
    parser.add_argument("--update",     action="store_true", help="update an existing address database")
    parser.add_argument("--force",      action="store_true", help="overwrite any existing address database")
    parser.add_argument("--no-pause",   action="store_true", default=len(sys.argv)>1, help="never pause before exiting (default: auto)")
    parser.add_argument("--no-progress",action="store_true", default=not sys.stdout.isatty(), help="disable the progress bar (shows cur. blockfile instead)")
    parser.add_argument("--version", "-v", action="version", version="%(prog)s " + addressset.__version__)
    parser.add_argument("--dbyolo",     action="store_true", help="Disable checking whether input blockchain is compatible with this tool...")
    parser.add_argument("--addrs_to_text", action="store_true", help="Append all found addresses to address.txt in the working directory while creating addressDB (Useful for debugging, will slow down AddressDB creation and produce a really big file, about 4x the size of the required AddressDB, about 32GB as of Jan 2020)")
    parser.add_argument("--dblength", default=30, help="The Maximum Number of Addresses the AddressDB can old, as a power of 2. Default = 30 ==> 2^30 Addresses. (Enough for BTC Blockchain @ Nov 2019", type=int)
    parser.add_argument("--first-block-file", default=0, help="Start creating the AddressDB from a specific block file (Useful to keep DB size down)", type=int)
    parser.add_argument("--blocks-startdate", default="2009-01-01", help="Ignore blocks earlier than the given date, format must be YYYY-MM-DD (Useful to keep DB size down)")
    parser.add_argument("--blocks-enddate", default="3000-12-31", help="Ignore blocks later than the given date, format must be YYYY-MM-DD (Useful to keep DB size down)")
    parser.add_argument("dbfilename",   nargs="?", default="addresses.db", help="the name of the database file (default: addresses.db)")

    # Optional bash tab completion support
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()

    if not args.no_pause:
        atexit.register(lambda: input("\nPress Enter to exit ..."))

    if not args.update and not args.force and path.exists(args.dbfilename):
        sys.exit("Address database file already exists (use --update to update or --force to overwrite)")

    if args.datadir:
        blockdir = args.datadir
    elif sys.platform == "win32":
        blockdir = path.expandvars(r"%APPDATA%\Bitcoin")
    elif sys.platform.startswith("linux"):
        blockdir = path.expanduser("~/.bitcoin")
    elif sys.platform == "darwin":
        blockdir = path.expanduser("~/Library/Application Support/Bitcoin")
    else:
        sys.exit("Can't automatically determine Bitcoin data directory (use --datadir)")
    blockdir = path.join(blockdir, "blocks")

    addressset.create_address_db(args.dbfilename, blockdir, args.dblength, args.blocks_startdate, args.blocks_enddate, args.first_block_file, args.dbyolo, args.addrs_to_text, args.update, progress_bar=not args.no_progress)
