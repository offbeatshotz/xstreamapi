# -*- coding: utf-8 -*-

import os
import hashlib
import sys

"""
    Generates a new addons.xml file from each addons addon.xml file
    and a new addons.xml.md5 hash file. Must be run from the root of
    the checked-out repo. Only handles single depth folder structure.
"""
class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        #
        print("Finished updating addons xml and md5 files")


    def _generate_addons_file( self ):
        # addon list
        addons = os.listdir( "." )
        # final addons.xml file
        addons_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
        # loop thru addons
        for addon in addons:
            try:
                # skip any file or .svn folder
                if ( not os.path.isdir( addon ) or addon == ".svn" ): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new xml
                new_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    new_xml += line.rstrip() + "\n"
                # we succeeded so add to final xml
                addons_xml += new_xml.rstrip() + "\n\n"
            except Exception as e:
                # oops
                print("Excluding %s for %s" % ( _path, e, ))
        # clean and write file
        addons_xml = addons_xml.strip() + "\n</addons>\n"
        self._save_file( addons_xml.encode( "UTF-8" ), file="addons.xml" )


    def _generate_md5_file( self ):
        try:
            # create a new md5 hash
            m = hashlib.md5( open( "addons.xml" , 'rb').read() ).hexdigest()
            # save file
            self._save_file( m.encode('UTF-8'), file="addons.xml.md5" )
        except Exception as e:
            # oops
            print("An error occurred creating addons.xml.md5 file!\n%s" % ( e, ))


    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "wb" ).write( data )
        except Exception as e:
            # oops
            print("An error occurred saving %s file!\n%s" % ( file, e, ))

if ( __name__ == "__main__" ):
    # start
    Generator()
