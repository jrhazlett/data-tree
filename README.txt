-----DRAFT-----
-----DRAFT-----
-----DRAFT-----
-----DRAFT-----
James Hazlett
james.hazlett.python@gmail.com

Welcome to the Data Tree!

Link to pip repository: https://pypi.org/project/data-tree/

A practical tree for those short on time.

Note: I’m treating this as a living project, and definitely in its alpha stage.

The mission of this tree is to provide a user friendly interface, balancing ease of use, performance,
and flexibility. This is a Python-based dictionary tree designed to exploit the language’s strengths and
avoid design approaches which would work well in other languages, but not Python.

This library grew out of a project that needed a data tree that could work in parallel with a GUI on mobile
devices without significant slowdown. After investigating several options, each brought about its own series
of risks which distracted from the core development of the app. As a result, I conducted a series of timed
tests and memory to see if there was a Python tree that could be both fast and not require a data science-
intensive background on behalf of the user.

To accomplish this, the public-facing methods use plain language to describe their actions. They also benefit
from extensive documentation. Behind the scenes, the tree dumps traditional method recursion in favor of stack
recursion, avoids generators, unnecessary method calls, and uses list comprehensions whenever possible.

The tree isn’t meant to replace existing solutions, so much as occupy the niche for the “I need convenience” crowd.



FEATURES

-Pure Python data tree

-Prioritizes explicit, plain language for all methods and variables

-Extensively documented

-Supports dict-like interaction ( i.e. _data_tree[ “1.2.3” ] = _node )

-Flexible pathing logic supports both strings, lists, and even nested lists

-Optimized code for fastest average performance

-Supports functional programming ( passing functions as objects )

-No hard-coded limits; the tree can keep expanding as long as the hardware supports it

-Supports Cython and compiling

-Can convert to and from native data structures

Examples Python libraries tested with this tree:
json
xml.etree cElementTree (xml)

-Modularized and easily inherited by other classes

-Designed for safe and easy memory management

-Bi-directional traversal support

-Intelligent nodes, which can dynamically take on tree management responsibilities, removing the need for additional support classes

-Comprehensive exception handling for easier debugging


TABLE OF CONTENTS

CONTACT INFORMATION
DISCLAIMERS
INSTALLATION
COMPATIBILITY
TERMINOLOGY
CLASS DESCRIPTIONS
METHODS EXPLAINED
NAMING CONVENTIONS
RECURRING OPTIONAL PARAMETERS
PUBLIC METHODS AND DESCRIPTIONS
-APPEND
-CLEAR
-DELETE
-GET
-LOGIC
-POP
-PRINT
-SET
-SETUP
INHERITANCE
PERFORMANCE NOTES
PERFORMANCE NOTES - TUPLES
PERFORMANCE NOTES - GENERATORS
KNOWN ISSUES
FUTURE PLANS
LICENSE (MIT)
HELPFUL LINKS


CONTACT INFORMATION

James Hazlett
james.hazlett.python@gmail.com

I plan to add a github repository after this initial post.

Feel free to reach out via email with library-related questions, suggestions, feature requests, cool ideas,
stories about how it helped you, something I might find interesting (wildly subjective, I know), etc.

Also, once I get this up on github, I want it open to community input.

Fair warning (only because its necessary): Any emails with easily Google-able questions about the Python language
will be ignored outright.



DISCLAIMERS

As covered in the MIT license I make no guarantees about this library. Its still considered in an 'alpha' state,
and will stay that way for the foreseeable future.

I'd like to open it up to collaborative development once the github page is up and running.

I encourage cautious coding. The tree is setup to be as flexible as possible, with what came to mind. I'm certain
there are more than a few ways to break it that I haven't thought of yet.

The detailed exception handling *should* help keep the pain factor down to a minimum, but I can only think of
so many ways to break things.

All interactions with the library by external sources should be handled through the library's public methods,
since they handle the overhead for ensuring all of its respective attributes remain in sync with each other.



INSTALLATION

Via pip...

pip install data-tree


Via source...

-You can also download the source from github https://github.com/jrhazlett/data-tree.

-Click "Clone or download" and "Download Zip"

-Decompress the zip file

-Navigate to the directory within a terminal and run: python setup.py install

If the install process fails, the KNOWN ISSUES section documents some of the possible install challenges
and potential solutions.


COMPATIBILITY

Environment support:

    Debian Linux - tested

    Mac OS - tested

    Windows - untested, but should work

Python versions:

    Python 3.7 - tested
    Python 3.5 - tested

    Python 3.4 - should work

    No compatibility for versions less than 3

Cython support:

    Recommended version: >0.27

    The modules in this library use PEP-484/526 annotations since...
    A. They're standardized (in theory)
    B. In timed tests, binaries compiled from these were actually faster than using the classic Cython approach



TERMINOLOGY

PATHS VS KEYS

"Keys" are the same thing as a "dictionary key." Each node tracks its immediate child nodes via dictionary.

"Paths" are a collection of keys used to traverse across multiple nodes.



PATHS DETAILED

Paths can be a list / tuple type iterable or a delimited string. The list-like iterable is the most flexible
when it comes to data types. If the dev plans to use delimited string paths, then the stored keys in the tree
should also be strings.

Example on how to pass paths as arguments:

In a situation where the has a simple tree setup like this:

{ ‘1’ : { ‘2’ : { ‘3’ : ‘test’ } } }

For a path made out of a list of keys, you would use this:

item_node.get_node_at_path( [ “1”, “2”, “3”, ] )

Nested lists will also work:

item_node.get_node_at_path( [ “1”, [ “2”, “3”, ], ] )

In this case, since all the keys are strings, a delimited string path is a reliable option:

item_node.get_node_at_path( “1.2.3” )

Note: By default, string-based paths use a period character “.” as their delimiter. Developers can override this at two points:

-Change the class variable via set_string_delimiter_for_path_default_for_all_classes( arg_string_delimiter_for_path_default )

This method sets the global variable for the class, so all classes in the library use this. The library doesn't attempt to reconcile
this change with pre-existing node instances. To protect against future errors, this method is setup to raise exceptions if at least
one node instance already exists, or if its called more than once. The dev can override both exceptions, but its not recommended.

-Pass arg_string_delimiter_for_path as an argument to the initializer for a new node

This ONLY sets the delimiter for the new node and all node children created by it.



Pathing: absolute vs sub-tree

For convenience, each node can take either a path meant for a child node, or an absolute path for the entire tree. The user
can tell the node which type of path it is via a boolean flag.

Note: When the tree's root node is of type Data_tree_node_with_quick_lookup, this will also trigger a dictionary key lookup
for the path, rather than the node-by-node traversal.


Pathing and data types: recommended coding practices

I recommend cautious coding when it comes to key data types within the tree. To preserve the tree’s speed, I didn’t include
any automatic data type reconciliation in the pathing algorithms.

To help protect the user from this type of issue, I included data type-specific exception messaging for KeyExceptions.

Here is an example KeyException exception message:

_data_tree = Data_tree_node()

_data_tree.append_path( [ 1, 2, 3, ] )

_node = _data_tree[ “1.2.3” ]

This will cause an exception with the following message:

Error: arg_key_or_path failed.

arg_key_or_path = 1.2.3

type( arg_key_or_path ) = <class 'str'>

Path parts present in tree =
[ , ]

Path parts missing from tree =
[ '1',
  '2',
  '3', ]

List of pairs, path_parts : ( bool ) if they failed due to data type discrepancy...

1 : True
2 : True
3 : True



CLASS DESCRIPTIONS



Data_tree_node


This is the base node type for this library.

It handles all node traversals by iterating across the nodes directly.

Each node tracks the following:
-It's unique object instance ID
-Node parent
-Immediate child nodes
-Root node for the entire tree
-An "object stored in node" variable, which contains the data meant
for the node at a given path.


Import instructions...
from data_tree import Data_tree_node




Data_tree_node_with_quick_lookup


This node type tracks all child nodes and their paths as long as its the root node for its data tree.

Import instructions...
from data_tree import Data_tree_node_with_quick_lookup

Behavior: root node vs child node

Each node of this type contains three dictionaries, explained in further detail later in this description.
The node only fills these dictionaries with information if its the root node. If the node is something
other than root, it empties its dictionaries to reduce its memory footprint. Conversely, if a child node
suddenly becomes the root node of its own independent tree, then it auto-populates with the necessary
tree information.

Behavior: sub-trees vs entire trees

Whenever a node within a data tree that has this class as its root node, it will prioritize dictionary
lookups over traversing nodes individually, as much as possible.

What typically triggers this behavior:

-Any path or search attempted by the root node

-Any absolute path / search involving the whole tree by a child node

Note: after extensive tests, this behavior should occur regardless if the child node is a data_tree_node
or data_tree_node_with_quick_lookup.

Information tracked:

-Dictionary for all paths, stored as keys, and their associated nodes stored as dictionary values.

Note: The keys for the above dictionary are stored in tuple format to avoid any data type clashing.

Example: self._dict_of_paths_and_nodes[ ( 1, 2, 3, ) ] = node_three

-Dictionary that's a reverse of the above, and uses instance ids for distinguishing between nodes.

Note: The paths are stored as lists of path keys. This minimizes the chances of loops iterating
across slower tuples.

Example: self._dict_of_nodes_and_paths[ <unique instance id for node three> ] = [ 1, 2, 3, ]

-Dictionary for all objects stored within nodes

Details...

Basic idea:

Each time set_object_stored_in_node( arg_object ) runs, the code attempts to create a unique id for the
object. In its default form, this process first attempts a hash of arg_object and if that fails, it gets
the object's instance id and uses that instead.

The id is then stored in a dictionary as a key. The corresponding value for that key is a list of node
objects. Each of those node objects contain the same values / object instances.

Example:
self._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[ <hash from arg_object> ] = [ node_one, node_two, ]






Class interoperability...

-After extensive testing, both nodes should have no issues working seamlessly together.

-The main difference between the two is if the root node of a tree is not of type Data_tree_with_quick_lookup,
then there's no dictionary key lookup during full-tree traversals.

-Regardless of the child node's class type, as long as the root node of the tree is of type
Data_tree_with_quick_lookup, passing an absolute path to the child will still trigger the dictionary key lookup.



-----METHODS EXPLAINED-----

Both Data_tree_node and Data_tree_node_with_quick_lookup have the exact same public methods, with the exact same
arguments. This makes them interchangeable. All differences in behavior take place, seemlessly, behind the scenes.



NAMING CONVENTIONS

To keep with (mostly) plain language, context, and predictability, this convention makes it easier to guess a method’s
name well enough for the IDE to suggest the correct one, or to support iterating through class attributes, while filtering
for key words.

Typically, each of the methods follow:

“verb”_”subject / data type”_”preposition”_”indirect object”

i.e. get_node_at_path()

All parameters start with “arg” at the beginning. This way, if you forget the parameters, and want *something* to show up,
type ‘arg’ and if you are using an IDE with the functionality, it will list out the arguments available.

i.e. “arg_key” and “arg_path”

The only exception to this rule is ‘kwargs’ because its already kind of standard, but all the arguments packed
within it, start with ‘arg’.

Each parameter has the following general layout:

arg_”data type ( if relevant )”_”topic”

The data type isn’t mentioned if the parameter can tolerate more than one data type, or the data
type is already implied by the topic.

Examples:

arg_path can take a string or a list, so no data type is given in the parameter name.

arg_bool_is_sub_tree_path mentions bool, since it’s exclusively used as a True / False statement.
Since “arg_is_sub_tree_path” could still be a little ambiguous about the exactly its value is used,
‘bool’ is added to the name to make it clear.



RECURRING OPTIONAL PARAMETERS

arg_bool_path_is_absolute / arg_bool_search_entire_tree

These are used to differentiate between searching only what is in the node's sub-tree, versus the
entire data tree.


arg_bool_search_sub_tree

This differentiates between immediate child nodes, versus all nodes in the given node's sub-tree.


arg_default_value_to_return

This is similar to the optional default value you would pass to a method like _dict.get( “key”, “default_value”, )
except it’s an explicitly named parameter.

Example:
_dict.get( “key”, arg_default_value_to_return = “default_value”, )

Note: I tried to simulate the original way, but it cut down on flexibility, as well as became a liability while
adding the additional optional arguments to each method.


arg_callable_filter

This takes callable objects ( functions / methods / lambdas ) and applies them during a method's internal
loop to filter. Each method's descriptor explains the process in detail.


arg_callable_formatter

This takes callable objects ( functions / methods / lambdas ) and applies them during a method's
internal loop to modify returned values. Each method's descriptor and associated "template" methods
explains the process in detail.


Additional information on "arg_callable" parameters...

Note: Each method which accepts callables handles them slightly differently based on their return type. Each
of these methods have partner methods prefixed with "template_example_arg_callable". These provide in-depth
information about their requirements.

The callables exist to provide the following benefits:

-Single-pass processing

Since the callables are active at the same time as their host method executes its data collection, both their
processing and the data collection occur at the same time. Otherwise, the developer would have to do subsequent
iterations on the returned data to filter / reformat it.

-Add functionality not already explicitly defined within the library

The developer can expand the methods to do just about anything.

Example:

Let's say, you call get_list_of_pairs_paths_and_node_children(), but instead of pairs of "paths and nodes,"
you actually want "paths and the objects stored within the nodes..."

One way you can do it is declare a method:

def get_pair_path_and_object_stored_in_node( arg_path, arg_node ) :

    return [ arg_path, arg_node._object_stored_within_node, ]

...then pass the method as an object, to get_list_of_pairs_paths_and_node_children().

In this case, since you're 'formatting' the returned data, you would pass this via 'arg_callable_formatter.'

Example:

get_list_of_pairs_paths_and_node_children( arg_callable_formatter = get_pair_path_and_object_stored_in_node )

Then, let's say you have a nodes located at keys "1" and "2", the objects stored in each node is "TEST_ONE" and "TEST_TWO" respectively.

Instead of getting:

[ [ "1", <node_one>, ],
  [ "2", <node_two>, ], ]

You would get this instead:

[ [ "1", "TEST_ONE", ],
  [ "2", "TEST_TWO", ], ]

For developers not already aware, lambdas are also a good choice for this:

Instead of...

def get_pair_path_and_object_stored_in_node( arg_path, arg_node ) :

    return [ arg_path, arg_node._object_stored_within_node, ]

You'd create a lambda object

get_pair_path_and_object_stored_in_node = lambda arg_path, arg_node : [ arg_path, arg_node._object_stored_within_node, ]

Either of these will work.



PUBLIC METHODS AND DESCRIPTIONS



append_key( arg_key, arg_node = None )
    
    Returns the node stored at arg_key.
    If the node doesn't exist, this method creates on and stores it at the key.
    If the node already exists, return the one that already exists.
    
    Argument:
    
    arg_key - obeys the same rules as a regular dictionary key.
    
    arg_node - If this equals None, the method auto-generates a new node of the same type as the one calling this method. Otherwise,
    this argument is another instanced node.
    

append_path( arg_path, arg_bool_path_is_absolute = False, arg_node = None )
    
    Returns the node at the path.
    If the path already exists, the method returns the node at the path.
    If the path doesn't exist, the method creates it and adds it to the tree.
    
    Arguments:
    
    arg_path - can be either a list of keys, or a delimited string.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    
    arg_node - If this equals None, the method auto-generates a new node of the same type as the one calling this method. Otherwise,
    this argument is another instanced node.
    
    arg_bool_raise_error_if_node_child_is_not_same_as_type_used_for_node_children - If True, the method will guard itself against adding
    potentially incompatible nodes. If False, the validation doesn't happen.
    

clear( **kwargs )
    
    Resets the node.
    
    Clears both the object stored within it, and clears all
    objects stored in self._list_of_attributes_to_clear.
    
    For this class specifically, the only item in
    self._list_of_attributes_to_clear is self._dict_of_keys_and_node_children.
    
    Note: This method does not attempt to sever the connection between this node
    and its parent tree. This can only happen if the tree removes the node.
    
    Arguments:
    
    kwargs is used here for specialized data clearing. If a class inherits this
    node, and passes variable names to this method, then its seeking to clear
    specific information, rather than the standard process.
    

copy( )
    
    Returns a new instance of a tree, consisting of new node instances.
    
    WARNING: This process only changes the reference for _object_stored_in_node. It does not attempt to do deep copies.
    
    Reasons:
    
    -Python's default process for deep copying many objects is prohibitively slow at run-time
    
    -This keeps with the general "pass by value" approach
    

delete_key_to_node_child( arg_key )
    
    This method deletes the key, and severs the connection to the child.
    
    This does not return a value.
    
    This will raise an exception if the key isn’t found.
    
    Argument:
    
    arg_key - This has the same behavior as a native dict key
    

delete_node_child( arg_node_child, arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False )
    
    This method looks for and then breaks the connection between the tree and the child node.
    
    By default, this method only looks for the arg_node_child in the host node’s immediate children.
    
    If the node is not found, the method will throw an exception.
    
    This method does not return a value.
    
    Arguments:
    
    arg_node_child - This is a node instance which already exists within the tree.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    

delete_path_to_node_child( arg_path, arg_bool_path_is_absolute = False )
    
    This method breaks all internal references to the node located at the path. This does not affect the other nodes along the path.
    
    This raises an exception if the path is not found.
    
    This method does not return a value.
    
    Arguments:
    
    arg_path - can be either a list of keys, or a delimited string.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

get( arg_path, arg_bool_search_entire_tree = False, arg_default_value_to_return = None )
    
    Returns the node located at arg_path if the node has children. Otherwise, method returns the object stored
    within the node.
    
    If the path does not exist, method returns arg_default_value_to_return
    
    Arguments:
    
    arg_path - can be either a list of keys, or a delimited string.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    arg_default_value_to_return - The value returned of the path does not exist.
    

get_data_in_format_for_export( arg_bool_search_entire_tree = False )
    
    Default behavior:
    
    Returns a nested dict that mimics the tree’s design, as opposed to the class-specific nodes.
    If the node is a leaf node, the method will add the object stored within it, rather than a dict.
    
    Note: This is meant to put the data structure in a format that can be easily converted to other
    data formats through built-in parsers.
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Example use with json:
    
    import json
    
    _data_tree = Data_tree_node()
    
    _node = _data_tree.append_path( "1.2.3" )
    
    _node.set_object_stored_in_node( "TEST" )
    
    print( json.dumps( _data_tree.get_data_in_format_for_export() )
    
    # Output: {"1": {"2": {"3": "TEST"}}}
    

get_deque_of_nodes( arg_bool_search_entire_tree = False, arg_bool_search_sub_tree = False, arg_bool_first_item_popped_is_leaf_node = False )
    
    Returns a stack / deque of nodes within the tree.
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    

get_dict_of_keys_and_node_children( )
    
    Returns a dict of the current node’s children and their associated keys.
    
    Note: This is intentionally meant to be a super simple method. For advanced
    functionality, use get_dict_of_string_paths_and_node_children()
    

get_dict_of_paths_and_node_children( arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False, arg_callable_filter = None, arg_callable_formatter = None )
    
    Returns a dict, with paths as keys and nodes as values.
    
    Arguments:
    
    arg_bool_search_sub_tree - If True, this method searches all nodes within this node's sub-tree.
    Otherwise, it only searches immediate children.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: If arg_bool_search_entire_tree is True, this method ignored arg_bool_search_sub_tree's value
    
    
    arg_callable_filter - This is a callable object that returns a value which will be interpreted as a boolean
    value.
    
    For additional details, review...
    template_for_arg_callable_filter_in_get_dict_of_paths_and_node_children( self, arg_iterable_path, arg_node )
    
    
    arg_callable_formatter - It a callable object which formats the returned data.
    
    For additional details, review...
    template_for_arg_callable_formatter_in_get_dict_of_paths_and_node_children( self, arg_iterable_path, arg_node )
    

get_id_for_object_stored_in_node( arg_object )
    
    RECOMMENDED_FOR_CUSTOM_OVERRIDES
    
    This method is used to generate and return unique ids for arg_object.
    
    This definition exists as a place holder, and not used in Data_tree_node.
    
    To see a functional definition for this method, check its definition in
    Data_tree_node_with_quick_lookup.
    

get_int_count_for_node_children( arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False, arg_callable_filter = None, arg_callable_formatter = None )
    
    Returns the number of nodes in the tree.
    
    This does not count the root node of either search type.
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    
    arg_callable_filter - This method interprets the returned value of this callable as True / False.
    
    arg_callable_formatter - This method returns an int value, which is added to the total count returned by
    get_int_count_for_node_children()
    

get_key_for_node_child( arg_node_child )
    
    Returns the key linking to the node if it’s found. If not, the method returns None.
    
    Argument:
    
    arg_node_child - This is a pre-existing node instance in the current node's immediate children.
    

get_list_of_keys_from_path( *args )
    
    This returns a flat list comprised of the keys to navigate from this node to
    the node at the path.
    
    I settled on this approach to balance execution time and flexibility.
    
    Reminder about competing approaches and performance:
    
    List with basic append requires a list reversal at the end, followed by
    a reconversion to a list. This makes the approach slower.
    
    List with insert( 0, item, ) is slightly faster than above, but slower than
    the stack option actually implemented here.
    

get_list_of_pairs_paths_and_node_children( arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False, arg_callable_filter = None, arg_callable_formatter = None )
    
    Returns a list of pairs: [ path, node, ]
    
    Arguments:
    
    arg_bool_search_sub_tree - If True, method searches the nodes within the current node's sub-tree
    
    Note: arg_bool_search_sub_tree is True by default.
    
    arg_bool_search_entire_tree - If True, searches the whole tree
    
    If both arg_bool_search_sub_tree and arg_bool_search_entire_tree are False, method only
    searches the immediate child nodes.
    
    arg_bool_get_paths_as_strings - If set to True, the method formats paths into delimited strings
    
    arg_callable_filtering - If passed, this needs to be a callable object. This method
    passes two arguments to the callable: path, and node.
    
    For additional details, review...
    template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children( self, arg_iterable_path, arg_node )
    
    arg_callable_formatter - This callable edits the returned values to a custom format described within it.
    
    For additional details, review...
    template_example_for_arg_callable_formatter_in_get_list_of_pairs_paths_and_node_children( self, arg_iterable_path, arg_node )
    
    Example of a valid callable:
    
    # Causes this method to return all leaf nodes
    _example_lambda = lambda arg_path, arg_node : not arg_node._dict_of_keys_and_node_children
    

get_list_of_pairs_paths_and_node_children_relevant_to_object( arg_object, arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False, arg_callable_filter = None, arg_callable_formatter = None )
    
    Returns a list of pairs [ path, node, ] consisting of nodes containing objects matching arg_object.
    
    Arguments:
    
    arg_object - The method matches this argument against the object stored in each node. It does so
    by calling get_id_for_object_stored_in_node(). This returns a hash value if possible, or an instance
    id.
    
    arg_bool_search_sub_tree - If True, method searches the nodes within the current node's sub-tree
    
    Note: arg_bool_search_sub_tree is True by default.
    
    arg_bool_search_entire_tree - If True, searches the whole tree
    
    If both arg_bool_search_sub_tree and arg_bool_search_entire_tree are False, method only
    searches the immediate child nodes.
    
    arg_bool_get_paths_as_strings - If set to True, the method formats paths into delimited strings
    
    arg_callable_filtering - If passed, this needs to be a callable object. This method
    passes two arguments to the callable: path, and node.
    
    
    template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children_relevant_to_object( self, arg_iterable_path, arg_node )
    
    Example of a valid callable:
    
    # Causes this method to return all leaf nodes
    _example_lambda = lambda arg_path, arg_node : not arg_node._dict_of_keys_and_node_children
    

get_list_path_from_arguments( *args )
    
    Returns args in the form of a list based on args' contents.
    

get_node_child_at_key( arg_key, arg_default_value_to_return = None )
    
    Returns the child node located at arg_key if it exists; otherwise, returns arg_default_value_to_return.
    
    arg_key - The target key for the node child in question.
    
    arg_default_value_to_return - This is the automatically returned value if the key does not exist in the tree.
    

get_node_child_at_path( arg_path, arg_bool_path_is_absolute = False, arg_default_value_to_return = None )
    
    Returns the node located at arg_path.
    
    If the path doesn’t exist in the tree, then the method will return arg_default_value_to_return.
    
    Arguments:
    
    arg_path - can be either a list of keys, or a delimited string.
    
    arg_default_value_to_return - This is the automatically returned value if the path does not exist in the tree.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree of the current node.
    

get_node_new_instance( )
    
    IMPORTANT_FOR_BUILDING_TREE
    
    Typically called by the following methods if no arg_node provided...
    append_key()
    append_path()
    
    Creates a new node, which uses the same delimiter as the node creating it.
    
    Reminder: This specific call happens enough to justify its own method for safety reasons.
    

get_node_parent( )
    
    Returns the node’s parent node, if it exists, otherwise, the returned value is None.
    

get_node_root( )
    
    Returns the root node for the entire tree.
    
    Note: If the root node calls this method, it will return itself.
    

get_object_at_key( arg_key, arg_default_value_to_return = None )
    
    Returns the object stored within the child node located at the key.
    
    If the key doesn’t exist, then the method will return arg_default_value_to_return.
    

get_object_at_path( arg_path, arg_bool_path_is_absolute = False, arg_default_value_to_return = None )
    
    Returns the object stored within the node located at the path.
    
    If the path does not exist, then the method will return arg_default_value_to_return.
    
    Arguments:
    
    arg_path - can be either a list of keys, or a delimited string.
    
    arg_default_value_to_return - This is the default value returned if the path does not exist.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

get_object_stored_in_node( arg_path = None, arg_bool_path_is_absolute = False, arg_default_value_to_return = None )
    
    Returns the object stored within node.
    
    If arg_path is None, then the method returns the object stored in the current node.
    
    Arguments:
    
    arg_path - can either a list of keys, a delimited string, or None. If the value is None, this method returns the value in
    arg_default_value_to_return.
    
    Note: arg_default_value_to_return is not honored if arg_path is None.
    
    If arg_path is defined, then the method will retrieve the object stored in the node at the path.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

get_path_to_node_child( arg_node_child, arg_bool_search_entire_tree = False, arg_bool_raise_error_if_node_is_not_in_tree = True, arg_default_value_to_return = None, arg_bool_get_path_as_string = False )
    
    Returns a list of keys in the path to the node by default, since not all tree instances are guaranteed to have exclusively strings as keys.
    
    Arguments:
    
    arg_node_child - This needs to be a node which already exists in the tree.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    arg_bool_raise_error_if_node_is_not_in_tree - If True, then the method will raise an exception if its unable to find the node. If False,
    the method will raise an exception and display the details for why arg_node_child wasn't found.
    
    arg_default_value_to_return is the value returned if arg_bool_raise_error_if_node_is_not_in_tree is False.
    
    Note: If arg_bool_raise_error_if_node_is_not_in_tree is True, then arg_default_value_to_return is ignored.
    
    Note: If arg_bool_raise_error_if_node_is_not_in_tree is True, then arg_default_value_to_return will not be honored.
    
    arg_bool_get_path_as_string - If True, returns path as a string. If False, returns path as a list of keys.
    

get_string_delimiter_for_string_paths( )
    
    Returns self._string_delimiter_for_path so users can use without
    explicitly having to know what it is.
    

get_string_path_from_arguments( *args )
    
    This takes *args in whatever format, and attempts to form a delimited string out of it.
    
    This method can handle nested data structures.
    
    Examples of valid arguments (not comprehensive):
    
    get_string_path_from_arguments( 1, 2, 3 )
    
    get_string_path_from_arguments( "1", "2", "3" )
    
    get_string_path_from_arguments( [ 1, 2, 3, ] )
    
    get_string_path_from_arguments( [ 1, [[[ 2 ]], [ 3 ]], ] )
    

get_tuple_of_keys_from_path( *args )
    
    Returns a tuple compiled from args.
    
    args can be multiple objects, even nested within each other.
    
    Data_tree_node_with_quick_lookup makes use of this method for hashing.
    

get_type_to_use_for_node_children( )
    
    RECOMMENDED_FOR_CUSTOM_OVERRIDES
    
    Returns the type used for new child nodes generated within this tree.
    

items( arg_bool_search_sub_tree = False, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False )
    
    This method is designed to behave similarly to dict.items(), and yields a list pair, with the path in index 0, and the
    corresponding node in index 1.
    
    Arguments:
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    arg_bool_get_paths_as_strings - If True, yields the path as a string, otherwise, the method returns the path
    as a list of keys.
    

keys( arg_bool_search_sub_tree = False, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False )
    
    This method supports iterating across the tree, similarly to dict.keys()
    
    Arguments:
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_get_paths_as_strings - If True, the method returns paths as delimited strings. If False, this returns
    the paths as lists of keys.
    

logic_data_is_in_correct_format( arg_data )
    
    Returns True if arg_data is in one of the three formats setup_tree_based_on_data_structure() takes.
    
    This is here primarily for debugging and data validation.
    
    For this method to return True, arg_data needs to be one of the following:
    
    -A simple dict
    -A nested dict
    -A list of nested dicts
    -Another data_tree_node
    

logic_key_exists( arg_key )
    
    Returns True, if the key exists for a child node.
    
    Argument:
    
    arg_key - obeys the same rules as regular dictionary keys.
    

logic_objects_match( arg_object_one, arg_object_two )
    
    RECOMMENDED_FOR_CUSTOM_OVERRIDES
    
    Typically called by...
    _get_list_of_pairs_paths_and_node_children_relevant_to_object()
    _get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter()
    _get_list_of_pairs_paths_as_strings_and_node_children_relevant_to_object()
    _get_list_of_pairs_paths_as_strings_and_node_children_relevant_to_object_with_filter()
    get_list_of_pairs_paths_and_node_children_relevant_to_object()
    
    This is a drop-in method for potential custom comparisons in inheriting classes.
    

logic_path_exists( arg_path, arg_bool_path_is_absolute = False )
    
    Returns True, if the path exists within the tree, and False if not.
    
    Arguments:
    
    arg_path - Can be a delimited string or list of keys.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

logic_path_is_leaf_node( arg_path, arg_bool_path_is_absolute = False )
    
    Returns True, if the path exists in the tree, and the node at the path has no children.
    
    Arguments:
    
    arg_path - This can be a delimited string, or a list of keys.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

nodes( arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False )
    
    This method supports iteration similarly to dict.values().
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    

paths( arg_bool_search_sub_tree = True, arg_bool_search_entire_tree = False, arg_bool_get_paths_as_strings = False )
    
    This method supports iteration similarly to dict.keys()
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    arg_bool_get_paths_as_strings - If True, returns each path as a delimited string. If False, the
    returned path is a list of keys.
    

pop( arg_path, arg_default_value_to_return = _OBJECT_FOR_RAISING_ERRORS, arg_bool_path_is_absolute = False )
    
    This method behaves similarly to dict.pop()
    
    Returns the object stored in the node located at arg_path; then removes the node and all its
    sub nodes. If arg_path doesn’t exist, returns arg_default_value_to_return.
    
    Arguments:
    
    arg_default_value_to_return - This is the returned value, if arg_path isn't in the tree.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    
    Note: This is a wrapper to mimic dict’s pop method.
    

pop_key( arg_key, arg_default_value_to_return = _OBJECT_FOR_RAISING_ERRORS )
    
    Returns the object stored in the child node at arg_key; and removes the node and all its sub nodes as well. If arg_key doesn’t exist,
    returns arg_default_value_to_return.
    
    If arg_key does not exist, and arg_default_value_to_return isn't set, then this method will raise an error.
    
    Arguments:
    
    arg_key - This obeys the same rules as a key used in a dict.
    
    arg_default_value_to_return - This is the default value returned if the key does not exist.
    

pop_key_to_node_child( arg_key, arg_default_value_to_return = _OBJECT_FOR_RAISING_ERRORS )
    
    Returns the child node located at arg_key; and removes the node and all its sub nodes.
    If arg_key doesn’t exist, returns arg_default_value_to_return.
    
    Note: This method is an explicit request for the node, instead of the object stored within it.
    
    Arguments:
    
    arg_key - This obeys the same rules as a normal dict key.
    
    arg_default_value_to_return - This is the default value returned if arg_key doesn't exist.
    

pop_node_child( arg_node_child, arg_bool_search_entire_tree = False, arg_default_value_to_return = None )
    
    Returns the path to the node; and removes the node. If arg_node doesn’t exist, returns arg_default_value_to_return.
    
    Arguments:
    
    arg_default_value_to_return - This is the default value returns if arg_node_child doesn't exist within the searched area.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Rational behind returning the path:
    
    If the dev is using the node object, then they already have access to the object stored within the node. The info
    that isn't necessarily easy to come by is what gets returned, which in this case would be the path.
    

pop_path( arg_path, arg_bool_path_is_absolute = False, arg_default_value_to_return = _OBJECT_FOR_RAISING_ERRORS )
    
    This method is an explicit wrapper for pop()
    
    If the node has no children, then this method return's the node stored at that location.
    
    Otherwise, it returns the node itself.
    
    Arguments:
    
    arg_path - This is the path to the node. It can either be a delimited string, or a list of keys.
    
    arg_default_value_to_return - This is the default value returned if arg_path does not exist in the searched area.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

pop_path_to_node_child( arg_path, arg_bool_path_is_absolute = False, arg_default_value_to_return = _OBJECT_FOR_RAISING_ERRORS )
    
    Returns the node located at the path, and removes this node.
    
    Any child nodes remain attached to popped node, and no longer considered
    part of the original data tree.
    
    Example:
    
    If the tree has the address: "1.2.3.4" and the user pops the node "1.2.3"
    then "3" is removed from the tree. The node at "4" remains attached to the node
    at "3", and becomes inaccessible to the tree popping the path.
    
    Node at address "1.2" remains unaffected, other than its connection to node "3"
    is severed.
    
    Arguments:
    
    arg_path - This is the path to the node. It can either be a delimited string, or a list of keys.
    
    arg_default_value_to_return - This is the default value returned if arg_path does not exist in the searched area.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

print_object( arg_object, arg_name_for_object = None )
    
    This method prints information in a reasonably easy to read format, and
    compensates for some formatting challenges in pprint.
    
    Reminder: Processes like Cythonize do not like a self.print() method, so this
    had to be changed to print_object.
    
    Arguments:
    
    arg_object - This can be pretty much anything.
    
    arg_name_for_object - If this contains a value, then the name provided
    is displayed above arg_object's printed information. If this value is None
    then only arg_object's info will print.
    

print_tree( arg_bool_search_entire_tree = False, arg_names_for_attributes_to_print = None )
    
    Prints output for the data tree.
    
    Example code and output…
    
    Code:
    
    _dict_tree = Dict_tree_node()
    
    _dict_tree.append_path( [ 1, 2, 3, ] )
    
    _dict_tree.print_tree()
    
    Output:
    
    ---PRINTING TREE---
    
    --- PATH: (root) ---
    
    --- PATH: 1 ---
    
    --- PATH: 1.2 ---
    
    --- PATH: 1.2.3 —
    
    Code:
    
    _dict_tree = Dict_tree_node()
    
    _node = _dict_tree.append_path( [ 1, 2, 3, ] )
    
    _node.set_object_stored_in_node( "EXAMPLE" )
    
    _dict_tree.print_tree( arg_names_for_attributes_to_print = "_object_stored_in_node" )
    
    Output:
    
    ---PRINTING TREE---
    
    --- PATH: (root) ---
    
    _object_stored_in_node = None
    
    --- PATH: 1 ---
    
    _object_stored_in_node = None
    
    --- PATH: 1.2 ---
    
    _object_stored_in_node = None
    
    --- PATH: 1.2.3 ---
    
    _object_stored_in_node = EXAMPLE
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    arg_names_for_attributes_to_print can be a single string, or a list of strings. This will include the attributes in the print output.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

set_object_stored_in_node( arg_object, arg_path = None, arg_bool_path_is_absolute = False )
    
    Stores arg_object in a node within the tree. If arg_path is not defined, arg_object is stored in the
    current node. If arg_path is defined, then the method will store arg_object in the node located at the path.
    
    Note: In keeping with dict’s regular behavior, if the path doesn’t exist, then the method will create create
    the path.
    
    Arguments:
    
    arg_object - This can be any object that could be stored in a variable.
    
    arg_path - This can be a delimited string, list of keys, or None. If the value is None, then the object set is an
    attribute of the current node.
    
    arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
    the sub tree.
    

set_string_delimiter_for_path_default_for_all_classes( cls, arg_string_delimiter_for_path_default, **kwargs ) 
    
    This method sets the global default delimiter for Data_tree_node and all inheriting classes.
    
    CAUTION: This method should only really run before any nodes exists.
    
    It will raise errors if used after first node created, or ran a 2nd time. These errors
    can be overridden in the arguments by setting either of these arguments to True:
    
    -arg_bool_override_safety_against_multiple_assignments
    -arg_bool_override_safety_against_setting_global_value_after_first_node_creation
    

setup_tree_based_on_data_structure( arg_data, arg_keys_for_categorizing_nodes = None, arg_bool_search_entire_tree = False )
    
    This method takes arg_data, and builds the data tree based on arg_data’s contents.
    
    arg_data can be one of the following:
    -dict
    -nested dict
    -list of dicts
    -another tree node
    
    Note:
    
    For users who want to use this library for importing data, I recommend Python’s built-in json
    library for json data, and xml.etree cElementTree ( xml ) for actual parsing. Produce a nested dict,
    or list of dicts from the data using these, and then pass it to setup_tree_based_on_data_structure
    as arg_data.
    
    Arguments:
    
    arg_data - This can be any of the following types:
    
    -Simple dict
    -Nested dict
    -List of dicts
    -Another data_tree
    
    arg_keys_for_categorizing_nodes - This can be either a list, or a single key.
    
    This argument is meant for "lists of dicts."
    
    If the code calling this method passes a list of dicts to arg_data, this method will use the arg_keys_for_categorizing_nodes
    to reference the corresponding values in the dicts. If arg_keys_for_categorizing_nodes is a list, the method will continue
    sub-dividing the categories until there are no keys left.
    
    Example:
    
    arg_data = [
    
    # Exists at index 0 of list
    { "key_1" : "value_1",
    "key_2" : "value_2",
    "key_3" : "value_3", },
    
    # Exists at index 1 of list
    { "key_1" : "value_4",
    "key_2" : "value_5",
    "key_3" : "value_6", },
    ]
    
    arg_keys_for_categorizing_nodes = [ "key_1", "key_2", ]
    
    Resulting tree:
    
    { "value_1" : { "value_2" : arg_data[ 0 ] },
    "value_4" : { "value_5" : arg_data[ 1 ] }, }
    
    Note: There's no hard limit to the resulting tree's depth, aside from the hardware running this library.
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    
    Example uses with python parsing libraries...
    
    Example use for xml with cElementTree:
    
    from xml.etree import cElementTree
    
    tree = cElementTree.parse('your_file.xml')
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    
    Or, if you want to use an XML string:
    
    root = cElementTree.XML(xml_string)
    xml_dict = XmlDictConfig(root)
    
    setup_tree_based_on_data_structure( arg_data = xml_dict )
    
    
    Example use with json
    
    import json
    
    _list_of_dicts = json.loads( json_string )
    
    setup_tree_based_on_data_structure( arg_data = _list_of_dicts, arg_keys_for_categorizing_nodes = [ "key_0", "key_1", ], )
    

template_example_for_arg_callable_filter_in_get_int_count_for_node_children( arg_node )
    
    This is a support method for get_int_count_for_node_children(), and provides a working example
    of a valid object for arg_callable_filter.
    
    Callable requirements:
    
    -Accepts one argument: arg_node
    
    arg_node is any node that exists within the scope of get_int_count_for_node_children()'s actions.
    
    -Returned value interpreted as boolean logic
    
    This callable's value is assessed in an if statement.
    
    If this callable returns True value, then the counter increments by 1. If False, the count does
    not increment.
    
    Action specific to this template:
    
    This callable will cause get_int_count_for_node_children() to provide a count for only nodes which
    contain data other than None.
    
    Equivalent lambda:
    
    lambda arg_node : not arg_node._object_stored_in_node == None
    

template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children( *args )
    
    This method is a template / example for what to pass via arg_callable_filter to get_list_of_pairs_paths_and_node_children()
    
    get_list_of_pairs_paths_and_node_children() interprets this method's returned value as boolean logic.
    
    Any callable passed this way has the following requirements:
    
    -Must accommodate two arguments: arg_iterable_path and arg_node
    
    First argument - This is the iterable of keys leading to arg_node when traversing the tree
    
    2nd argument - This is the node located at the end of arg_list_path
    
    -Returned value is always assessed as boolean logic
    
    Details specific to this example:
    
    This callable causes get_list_of_pairs_paths_and_node_children() to return only leaf nodes
    
    Equivalent lambda:
    lambda *args : not args[ 1 ]._dict_of_keys_and_node_children
    

template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children_relevant_to_object( *args )
    
    This method is a template / example for what to pass via arg_callable_filter to
    get_list_of_pairs_paths_and_node_children_relevant_to_object()
    
    get_list_of_pairs_paths_and_node_children_relevant_to_object() interprets this method's returned value as boolean logic.
    
    Any callable passed this way has the following requirements:
    
    -Must accommodate two arguments
    
    First argument - This is the iterable of keys leading to arg_node when traversing the tree
    
    2nd argument - This is the node located at the end of arg_list_path
    
    -Returned value is always assessed as boolean logic
    
    Details specific to this example:
    
    This callable causes get_list_of_pairs_paths_and_node_children_relevant_to_object() to return only leaf nodes
    
    Equivalent lambda:
    lambda arg_iterable_path, arg_node : not arg_node._dict_of_keys_and_node_children
    

template_example_for_arg_callable_formatter_in_get_int_count_for_node_children( arg_node )
    
    This is a support method for get_int_count_for_node_children(), and provides a working example
    of a valid object for arg_callable_filter.
    
    Callable requirements:
    
    -Accepts one argument: arg_node
    
    arg_node is any node that exists within the scope of get_int_count_for_node_children()'s actions.
    
    -Returned value is an int
    
    This callable's value is the count returned by get_int_count_for_node_children().
    
    Action specific to this template:
    
    This callable causes get_int_count_for_node_children() to sum the lengths of each node's _object_stored_in_node
    attribute.
    
    Nodes with iterable objects have the lengths of the iterables counted instead.
    
    Nodes storing only None, aren't counted.
    
    All other values for _object_stored_in_node return 1.
    

template_example_for_arg_callable_formatter_in_get_list_of_pairs_paths_and_node_children( *args )
    
    This method is a template / example for what to pass via arg_callable_formatter to get_list_of_pairs_paths_and_node_children()
    
    Any callable passed this way has the following requirements:
    
    -Must accommodate two arguments: arg_iterable_path and arg_node
    
    First argument - This is the iterable of keys leading to arg_node when traversing the tree
    
    2nd argument - This is the node located at the end of arg_list_path
    
    -Returned value: despite get_list_of_pairs_paths_and_node_children()'s name, the returned value can be pretty much
    anything. Despite this, its still recommended that a callable passed this way returns a pair consisting of a path and node.
    
    Details specific to this example:
    
    This callable causes get_list_of_pairs_paths_and_node_children() to return a list of pairs:
    -String paths
    
    -Objects stored in the nodes at each path
    
    Equivalent lambda:
    lambda arg_iterable_path, arg_node : [ self._string_delimiter_for_path.join( [ str( item_path_part ) for item_path_part in arg_iterable_path ] ), arg_node._object_stored_in_node, ]
    

template_example_for_arg_callable_formatter_in_get_list_of_pairs_paths_and_node_children_relevant_to_object( *args )
    
    This method is a template / example for what to pass via arg_callable_formatter to
    get_list_of_pairs_paths_and_node_children_relevant_to_object()
    
    Any callable passed this way has the following requirements:
    
    -Must accommodate two arguments
    
    First argument - This is the iterable of keys leading to arg_node when traversing the tree
    
    2nd argument - This is the node located at the end of arg_list_path
    
    -Returned value: despite get_list_of_pairs_paths_and_node_children_relevant_to_object()'s name, the returned value can be
    pretty much anything. Despite this, its still recommended that a callable passed this way returns a pair consisting of a
    path and node.
    
    Details specific to this example:
    
    This callable causes get_list_of_pairs_paths_and_node_children_relevant_to_object() to return a list of pairs:
    -String paths
    
    -Objects stored in the nodes at each path
    
    Equivalent lambda:
    lambda arg_iterable_path, arg_node : [ self._string_delimiter_for_path.join( [ str( item_path_part ) for item_path_part in arg_iterable_path ] ), arg_node._object_stored_in_node, ]
    

template_for_arg_callable_filter_in_get_dict_of_paths_and_node_children( arg_iterable_path, arg_node )
    
    This method is a template / example of the type of callable to pass to get_dict_of_string_paths_and_node_children()
    via arg_callable_filter
    
    General requirements for any callable passed this way:
    -Must be able to support two arguments. The arguments can have any name, but the first will always be
    a path ( list of keys ) to reach arg_node within the tree.
    
    -get_dict_of_string_paths_and_node_children() will always interpret this callable's returned value as boolean logic
    
    Details specific to this example:
    
    This filter returns True, if arg_node has no child nodes, causing get_list_of_node_children() to return
    only leaf nodes.
    
    Equivalent lambda:
    
    lambda arg_iterable_path, arg_node : not arg_node._dict_of_keys_and_node_children
    

template_for_arg_callable_formatter_in_get_dict_of_paths_and_node_children( arg_iterable_path, arg_node )
    
    This method is a template / example of the type of callable to pass to arg_callable_formatter
    in get_dict_of_string_paths_and_node_children()
    
    It determines what values are actually stored in the returned dict.
    
    In order for this type of callable to work in get_dict_of_string_paths_and_node_children(), it
    must satisfy the following requirements:
    
    -Accept two arguments: arg_list_path and arg_node
    
    arg_iterable_path - This is always an iterable of keys to traverse the tree to reach arg_node
    
    arg_node - This is always the node stored at the end of arg_list_path
    
    -This must always return a pair, and the value at index 0, must be a hashable type, the value at index 1 can be anything.
    
    Note: since arg_list_path is always a list, it can't be returned as-is without triggering an error.
    
    Notes for this specific example:
    
    This callable causes get_dict_of_string_paths_and_node_children() to return a dict of paths and the objects stored in
    each corresponding node.
    
    [ _string_path_hashable, arg_node._object_stored_in_node, ]
    
    Equivalent lambda:
    
    lambda arg_iterable_path, arg_node : [ self._string_delimiter_for_path.join( [ str( item_path_part ) for item_path_part in arg_iterable_path ] ), arg_node._object_stored_in_node, ]
    

values( arg_bool_search_sub_tree = False, arg_bool_search_entire_tree = False )
    
    Supports iteration similarly to dict.values()
    
    Arguments:
    
    arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.
    
    Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value
    
    arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
    



INHERITANCE

To help with adapting the library to more custom uses, the descriptors contain labels to help identify safe methods for
overriding, as well as understanding how each method factors into actions such as tree building.

IMPORTANT_FOR_BUILDING_TREE

This marker exists in descriptors for methods which play active roles in adding and removing nodes.

RECOMMENDED_FOR_CUSTOM_OVERRIDES

Methods with this tag carry out common operations, and are low risk to change.

Example: The code typically calls logic_objects_match() when comparing objects stored in nodes. Instead of doing
a direct comparison, the code calls this method.



PERFORMANCE NOTES

Disclaimer: all of these design decisions are based off timed tests across Python 3.4 - 3.7. None of it
is 'set in stone,' since the performance advantages could change in a future Python version.


Python versions

Python 3.7 definitely has the fastest overall execution, so a lot of the research focused on this.


Compiling

-Packaging employs wheels to support compiling to binary format

-Cython builds C files from annotated Python source

Note: Annotations don't exist in the basic Python source (.py) since in speed tests, they appeared to
slow down "pure python" execution.

Note: In timed tests, binaries produced from Python-annotated files had higher average speeds than binaries
produced using Cython's original code


Loops

-There's no method recursion. Its impractically slow, and runs the risk of colliding with one of Python's
hard-limits.

-The code handles recursion through deques / stacks since they benefit from quick append / pop methods.

-The minimalist recursion loops exist in four variations:
--Basic - no callables or logic checks. This is the fastest execution.
--Filter only / Formatter only - both of these only make one call to their callable object, each iteration
--Both filter and formatter - these loops call both callable once per iteration

-Since there are four combinations, all logic checks for optional parameters occur only once, to select
which loop to use

-The methods prioritize list comprehensions whenever possible / reasonable.

-All paths exist as lists internally, except where hashable keys are necessary. In cases involving hashes,
list-to-string conversions still had the fastest average execution.

-While the library can support them as arguments, the library doesn't use tuples or generators internally,
since they both come with significant speed penalties.

--Note: Generators are only practical when a single-instance list can threaten to hit the memory threshold.
Since Python 3+ deletes local variables as soon as they fall out of scope, the chances of actually needing
a generator is incredibly unlikely, and not worth the speed penalty.


Data structures

-Generally, all things key-related are handled by dicts

-Lists handle everything that doesn't benefit from a hash

-Tuples exist exclusively to support hashes

-In cases where Data_tree_node_with_quick_lookup is the root node of the tree, any paths / searches / etc. are
handled through dictionary lookups rather than node traversals.

Note: The dictionaries are only populated for the root node, so this mitigates potential performance and memory
impacts in the event a node is modified within the tree.


Exception handling

-Try / excepts exist only where actual exceptions can occur. Except rare single instances like importing modules,
there is no point where exceptions can happen during an 'error free' run.



Notes on testing criteria:

-Time comparisons were calculated as 'averages' across 50-100 automatic repetitions of various tests

-Each comparison simulated similar conditions between two or more approaches as closely as possible



Risk mitigation for memory leaks...

Since this is a tree, there are safeguards against unintentionally preserved internal references.

All methods responsible for adding or removing nodes from the tree have "_integrate" as their
prefix. This narrows the potential internal causes for memory leaks to the following...

Data_tree_node - 4 methods ( 2 of 6 "_integrate" methods are simple wrappers )

Data_tree_node_with_quick_lookup - 7 methods



Garbage collection…

The tree works off Python’s existing process, and focuses on removing key references within the tree.

Examples:

Data_tree_node: If you pop a node with child nodes, the tree severs the links to and from its parent.

Data_tree_fast_absolute_paths: This class severs the links like Data_tree_node, and also removes all absolute path
references to both the popped node and all its children.

Note: weakref is never used to prevent broken links.



KNOWN ISSUES

-Silenced deprecation warning

The actual message is: “DeprecationWarning: Deprecated since Python 3.4. Use importlib.util.find_spec() instead.”

This is a known issue with using setuptools for compiling. I’ve only seen this on Mac OS, using Python 3.7, with binaries. Under all other conditions
( i.e. Debian Linux, pure python, etc. ), this warning doesn’t appear.

To work around this issue, I left __init__.py out of list of files to compile and added code to the module to silence deprecation warnings. Since
this library only uses official packages, this shouldn’t escalate beyond just the warning message.


-Untested Windows support

There's no reason for this library not to work on Windows OS, but its untested.

Since all the libraries used in this package’s creation are native to Python, and the binaries are compiled from pure python modules, this shouldn’t
be a problem.


-Mac OS possible header version issue

If upgrading a Mac OS version, its possible an error might come up which states something along the lines of:

"...error: uknown enumerated scalar
platform:     zippered
clang: error: linker command failed with exit code 1
error: command 'gcc' failed with exit status 1"

Solution: Need to install "MacOS headers in the base system." In Mac OS' case, this would be "macOS_SDK_headers_for_macOS_<version>.pkg"
This changes between OS versions, so you need to look up the correct target for your version.



FUTURE PLANS

-The future plans are still to focus on the main three areas: usability, flexibility, and performance.

-Parallel processing...

Need to investigate further. It's theoretically fast, but in timed tests it didn't compare well against sequential processing (cores tested: 4).

-Annotations...

Although a lot of the code is already annotated, there's still plenty of room for enhancements here.

-Additional features...

Any requests are welcome.

-Data science elements...

Obviously these have their use, and are certainly considered "in-scope." The only caveat is this library isn't meant to replace other existing data
science libraries, so there's no plan for trying to indiscriminately match them "feature-by-feature."


-Features considered out of scope:

--Data parsing from sources such as files / strings / binary

Raw data parsing is out of scope for the foreseeable future. There's too much potential variation, and any assumptions made wouldn't work in all cases.

I am open to adding support for additional structured data types provided by other libraries.


--Python 2.7 compatibility

There are no plans for retroactive compatibility. This library is designed more for exploiting performance boosts from each consecutive version of Python,
and in order to do so reliably, it needs to stay future-facing.



LICENSE (MIT)

MIT License

Copyright (c) 2019 James Hazlett

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



HELPFUL LINKS

Lambdas
https://www.w3schools.com/python/python_lambda.asp

Garbage collector
https://docs.python.org/3/library/gc.html





-----DRAFT-----
-----DRAFT-----
-----DRAFT-----
-----DRAFT-----
