'''
This module is responsible for setting up PURE PYTHON packages.

Note: I tried the regular 'procedural' approach I've seen most setup.py set up like,
and I found the class approach much easier to test, organize, and re-use for other projects.
'''
#
# Libraries - native
#
import contextlib
import os
import pprint
from setuptools import setup
from setuptools.extension import Extension

try :

    from Cython.Build import cythonize

    _BOOL_CYTHON_ACTIVE = True

except :

    _BOOL_CYTHON_ACTIVE = False
#
# Class
#
class Manager_setup_support():
    '''
    This class supports package creation. It provides methods for more complex functionality.

    It does not store values internally.

    Reminders: self.temporarily_set_current_directory() is called in each method so they
    can be used somewhat independently if necessary. The method call also keeps all the code explicit.
    '''
    #
    # Public
    #
    #
    # Public - get
    #
    def get_list_of_pairs_name_for_module_and_path_sub_for_module(self, arg_path_to_directory_for_source, arg_strings_valid_file_extensions, arg_names_with_extensions_for_files_to_filter_out):
        '''
        This returns a list consisting of pairs:

        -Names for packages are stored in index 0

        -Paths for packages are stored in index 1

        I hold off on building actual extensions here because in some cases they aren't necessary.
        '''
        #
        # Argument assignments
        #
        _set_of_strings_valid_file_extensions = self._get_set_converted_from_object( arg_strings_valid_file_extensions )

        _list_of_names_with_extensions_for_files_to_filter_out = self._get_list_converted_from_object( arg_names_with_extensions_for_files_to_filter_out )
        #
        # Initialize list
        #
        _list_of_pairs_name_for_module_and_path_sub_for_module = [ ]
        #
        # Populate list
        #

        for item_path_sub_for_directory, item_list_of_names_for_directory_children, item_list_of_names_for_files in os.walk( arg_path_to_directory_for_source ) :

            for item_name_for_file in item_list_of_names_for_files :

                if all( [ self.get_string_extension_from_path_to_file( item_name_for_file ) in _set_of_strings_valid_file_extensions,
                          not item_name_for_file in _list_of_names_with_extensions_for_files_to_filter_out, ] ) :

                    item_path_sub_to_module = os.path.join( item_path_sub_for_directory, item_name_for_file, )

                    item_name_for_module = self.get_name_for_module( item_path_sub_to_module )

                    _list_of_pairs_name_for_module_and_path_sub_for_module.append( [ item_name_for_module, item_path_sub_to_module, ] )

        return _list_of_pairs_name_for_module_and_path_sub_for_module

    def get_name_for_module( self, arg_path_to_file_containing_source ):

        item_name_for_module = arg_path_to_file_containing_source[ 1 : ] if arg_path_to_file_containing_source.startswith( "." ) else arg_path_to_file_containing_source

        # Reminder: The str() conversion happens here to quiet an IDE warning
        item_name_for_module = str( item_name_for_module.split( "." )[ 0 ] )

        return item_name_for_module.replace( os.path.sep, ".", )[ 1 : ]

    def get_string_extension_from_path_to_file( self, arg_path_to_file ):

        return os.path.basename( arg_path_to_file ).split( ".", 1, )[ 1 ]
    #
    # Public - print
    #
    def print_info( self, arg_object, arg_name_for_object = None ) :
        '''
        Reminder: Processes like Cythonize do not like a self.print() method, so this
        had to be changed.
        '''
        if not arg_name_for_object == None :

            print( arg_name_for_object, "=", )

        print( "\n".join( self._print_info_get_list_of_strings_formatted( arg_object ) ), "\n\n", )
    #
    # Public - temporary set
    #
    @contextlib.contextmanager
    def temporarily_set_current_directory( self, arg_path_to_directory ) :

        path_directory_original = os.getcwd()

        os.chdir( arg_path_to_directory )

        yield

        os.chdir( path_directory_original )
    #
    # Private
    #
    #
    # Private - get
    #
    def _get_list_converted_from_object( self, arg_object ):

        if isinstance( arg_object, ( list, tuple, ), ) :

            # Reminder: if arg_object is a list, it still gets duplicated
            return list( arg_object )

        else :

            return [ arg_object ]

    def _get_set_converted_from_object( self, arg_object ):

        if isinstance( arg_object, ( list, tuple, ), ) :

            return set( arg_object )

        else :

            return { arg_object }
    #
    # Private - print
    #
    def _print_info_get_list_of_strings_formatted( self, arg_object ):

        _string = self._pprint.pformat( arg_object )

        _list = _string.split( "\n" )

        _list_new = []

        item_index = 0

        while item_index < len( _list ) :

            if item_index >= len( _list ) :

                break

            item_string_current = _list[ item_index ]

            item_string_current_with_no_leading_or_trailing_white_space = item_string_current.strip()

            if item_string_current_with_no_leading_or_trailing_white_space :

                for item_character in self._list_of_characters_which_indicate_a_data_structure_end :

                    item_sub_string_to_use_as_replacement = "".join( [ ", ", item_character, ] )

                    item_string_current = item_string_current.replace( item_character, item_sub_string_to_use_as_replacement, )
                #
                # Handle ':' for dicts
                #
                # if ": " in item_string_current : item_string_current = " : ".join( item_string_current.split( ": " ) )
                #
                # Handle spacing between lines
                #
                if item_string_current.endswith( "," ) :

                    if item_string_current[ -2 ] in self._set_of_characters_which_indicate_a_data_structure_end :

                        item_string_current = "".join( [ item_string_current, "\n", ] )

                elif item_string_current.endswith( " '" ) or item_string_current.endswith( " \"" ) :

                    item_index_next = item_index + 1

                    while ( item_string_current.endswith( " '" ) or item_string_current.endswith( " \"" ) ) and item_index_next < len( _list ) :

                                                         # Current
                        item_string_current = "".join( [ item_string_current.rstrip()[ : -1 ],

                                                         # Next
                                                         _list[ item_index_next ].lstrip()[ 1 : ], ] )

                        if item_string_current[ -1 ] in self._list_of_characters_which_indicate_a_data_structure_end :

                            item_string_current = "".join( [ item_string_current[ : -1 ], ", ", item_string_current[ -1 ], ] )

                        _list.pop( item_index_next )

            _list_new.append( item_string_current )

            item_index += 1

        return _list_new
    #
    # Private - setup
    #
    def __init__(self):

        self._pprint = pprint.PrettyPrinter( compact = True,

                                             indent = 2,

                                             # This ensures all sub-structures print vertically.
                                             width = 1, )

        self._list_of_characters_which_indicate_a_data_structure_end = [ "]",
                                                                         "}",
                                                                         # ")",
                                                                         ]

        self._set_of_characters_which_indicate_a_data_structure_end = set( self._list_of_characters_which_indicate_a_data_structure_end )
#
# Public - instance of support class
#
manager_setup_support = Manager_setup_support()
#
# Create and store arguments for setup()
#
# Note: This is a flow-based argument assignment, and the dict
# stores the argument key and value as soon as its finalized.
# The dict itself is unpacked into setup()
#
_dict_of_arguments_for_setup = { }
#
# Public - values set via template
#
#
# Public - values set via template - name
#
_NAME_FOR_PACKAGE = "data_tree"
_dict_of_arguments_for_setup[ "name" ] = _NAME_FOR_PACKAGE

_NAME_FOR_DIRECTORY_CONTAINING_FILES_SOURCE_CODE = _NAME_FOR_PACKAGE.replace( "-", "_", )
#
# Public - values to set via template - paths
#
_PATH_TO_DIRECTORY_CONTAINING_SOURCE_FILES = "".join( [ "./", _NAME_FOR_DIRECTORY_CONTAINING_FILES_SOURCE_CODE ] )
#
# Setup ext_modules
#
_list_of_compilable_extensions = [ "c", "pyx", ]

_list_of_names_for_files_not_to_compile = [ "__init__.py" ]

_list_of_pairs_name_for_module_and_path_sub_for_module = \
    manager_setup_support.get_list_of_pairs_name_for_module_and_path_sub_for_module( arg_path_to_directory_for_source = _PATH_TO_DIRECTORY_CONTAINING_SOURCE_FILES,
                                                                                     arg_strings_valid_file_extensions = _list_of_compilable_extensions,
                                                                                     arg_names_with_extensions_for_files_to_filter_out = _list_of_names_for_files_not_to_compile, )



manager_setup_support.print_info( arg_object = _list_of_pairs_name_for_module_and_path_sub_for_module,
                                  arg_name_for_object = "_list_of_pairs_name_for_module_and_path_sub_for_module", )

_list_of_extensions_to_compile = [

    Extension( item_name_for_module, sources = [ item_path_for_module ], )

    for item_name_for_module, item_path_for_module in _list_of_pairs_name_for_module_and_path_sub_for_module

]

if _BOOL_CYTHON_ACTIVE :

    _dict_of_arguments_for_setup[ "ext_modules" ] = cythonize( _list_of_extensions_to_compile )
#
# Setup description
#
try :

    with open( "README.md", "r", ) as _file :

        _dict_of_arguments_for_setup[ "long_description" ] = _file.read()

        _dict_of_arguments_for_setup[ "long_description_content_type" ] = "text/markdown"

except :

    pass
#
# Execute setup
#
setup( **_dict_of_arguments_for_setup,
       author = "James Hazlett",
       author_email = "james.hazlett.python@gmail.com",

       #packages = setuptools.find_packages(),
       packages = [ "data_tree" ],

       package_dir = { "data_tree" : "data_tree" },

       package_data = { "data_tree" : [ "*",
                                        "src/*", ] },

       url = "https://github.com/jrhazlett/data_tree",

       version = "0.0.1",

       classifiers = [

           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",

       ],
)


'''
MIT License

Copyright (c) 2019 James Robert Hazlett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

































