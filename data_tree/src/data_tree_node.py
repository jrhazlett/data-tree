#!python
#cython: language_level=3
""""""
#
# Libraries - native
#
import pprint
import sys
import time
#
# Libraries - native - collections
#
# Used for node traversals
from collections import deque

# Used to elaborate on raised exceptions
from collections.abc import Hashable

# Base class for Data_tree_node
from collections import UserDict
#
# Libraries - native - typing
#
# <any notated types go here>
#
# Config
#
# Support values for printing information
#
# Note: These are global variables meant to remain unchanged during execution. Since they are
# static in nature, they are stored here to ensure only a single instance exists.
#
_LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END = ["]",
                                                           "}", ]

_SET_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END = set(
    _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END)
#
# Sets up pprint with friendly display settings
#
_PPRINT = pprint.PrettyPrinter(compact=True,

                               indent=2,

                               # This ensures all sub-structures print vertically.
                               width=1, )
#
# The pop methods use this object to raise errors. This allows the user to pass 'None' as an argument.
#
_OBJECT_FOR_RAISING_ERRORS = object()
#
# This is the default value set for all instances, unless either set_string_delimiter_for_path_default_for_all_classes() or
# the delimiter is set at the node's creation.
#
_STRING_DELIMITER_FOR_PATH_DEFAULT = "."
#
# Class
#


class Data_tree_node(UserDict):
    """
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
    """
    #
    # Public
    #
    #
    # Public - wrappers
    #

    def __contains__(self, arg_path):
        """
        Returns True, if the path exists within the tree. This method is a wrapper for dict’s response
        when using an ‘in’ boolean check.

        Example:

        _bool_value = “1.2.3” in _dict_tree

        If arg_bool_path_is_absolute is False, then the method assumes arg_path
        begins with a key to one of the calling node’s children. If True, then the method starts with the root node.

        Argument:

        arg_path - Can be a list of keys or delimited string.
        """
        return self.logic_path_exists(arg_path=arg_path, arg_bool_path_is_absolute=False, )

    def __delitem__(self, arg_path):
        """
        This method uses delete_path_to_node_child to remove the path and sever the
        connection between this node and its parent tree.

        It is a wrapper for the ‘del’ command, designed to add
        dict-like functionality to the tree.

        Example:

        del dict_tree[ “1.2.3” ]

        This method does not return a value.

        This method does not make an explicit attempt to delete the node.

        Argument:

        arg_path - Can be a list of keys or delimited string.
        """
        self.delete_path_to_node_child(arg_path=arg_path,
                                       arg_bool_path_is_absolute=False, )

    def __getitem__(self, arg_path):
        """
        Returns the object stored within the current node, if no value is provided for arg_path.

        If a value for arg_path exists, the method will return the object stored in the node, if the node is a leaf;
        otherwise, it returns the node at the path.

        This method is intended to be a wrapper for similar dict functionality, and emulate dict behavior as closely as possible.
        In the case where a key is accessed within a dict, the value is returned. In a nested dict, this value can be another
        dict if there are multiple layers.

        Example:

        _data_tree = { “1” : { “2” : { “3” : “Example” } } }

        _node = _data_tree[ “1.2” ] # _node then contains { “3” : “Example” }

        _string = _data_tree[ “1.2.3” ] # _string then contains “Example”

        Argument:

        arg_path - Can be a list of keys or delimited string.
        """
        if arg_path == None:

            return self._object_stored_in_node

        else:

            _node = self.get_node_child_at_path(arg_path=arg_path,
                                                arg_bool_path_is_absolute=False, )

            if _node == None:

                self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_path,
                                                             arg_node_start=self, )

            else:

                if _node._dict_of_keys_and_node_children:

                    return _node

                else:

                    return _node._object_stored_in_node

    def __setitem__(self, arg_object, arg_path):
        """
        Stores arg_object in a node within the tree. If arg_path is not defined, arg_object is
        stored in the current node. If arg_path is defined, then the method will store arg_object
        in the node located at the path.

        Note: In keeping with dict’s regular behavior, if the path doesn’t exist, then the method
        will create create the path.


        Example:

        _dict_tree[ “1.2.3” ] = “example”
        """
        self.set_object_stored_in_node(arg_object=arg_object,
                                       arg_path=arg_path,
                                       arg_bool_path_is_absolute=False, )
    #
    # Public - append
    #

    def append_key(self, arg_key, arg_node=None):
        """
        Returns the node stored at arg_key.
        If the node doesn't exist, this method creates on and stores it at the key.
        If the node already exists, return the one that already exists.

        Argument:

        arg_key - obeys the same rules as a regular dictionary key.

        arg_node - If this equals None, the method auto-generates a new node of the same type as the one calling this method. Otherwise,
        this argument is another instanced node.
        """
        if arg_node == None:

            if arg_key in self.keys():

                return self._dict_of_keys_and_node_children[arg_key]

            else:

                _node_new = self.get_node_new_instance() if arg_node == None else arg_node

                self._integrate_allocate_node(arg_key=arg_key,
                                              arg_node=_node_new,
                                              arg_node_parent=self, )

                return _node_new

        else:

            self._integrate_allocate_node(arg_key=arg_key,
                                          arg_node=arg_node,
                                          arg_node_parent=self, )

            return arg_node

    def append_path(self, arg_path, arg_bool_path_is_absolute=False, arg_node=None):
        """
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
        """
        item_node = self._node_root if arg_bool_path_is_absolute else self

        _list_of_path_parts = self.get_list_of_keys_from_path(arg_path)

        _last_path_part = _list_of_path_parts.pop()

        for item_path_part in _list_of_path_parts:

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                item_node_new = self.get_node_new_instance()

                self._integrate_allocate_node(arg_key=item_path_part,
                                              arg_node=item_node_new,
                                              arg_node_parent=item_node, )

                item_node = item_node_new

        if arg_node == None:

            item_node_new = self.get_node_new_instance()

        else:

            item_node_new = arg_node

            if not item_node_new._node_parent == None:

                self._raise_error_because_node_child_is_still_part_of_another_tree(
                    item_node_new)

        self._integrate_allocate_node(arg_node=item_node_new,
                                      arg_node_parent=item_node,
                                      arg_key=_last_path_part, )

        return item_node_new
    #
    # Public - clear
    #

    def clear(self, **kwargs):
        """
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
        """
        if kwargs.get("arg_bool_do_standard_clear", True, ):

            self._object_stored_in_node = None

            for item_attribute in self._list_of_attributes_to_clear:

                item_attribute.clear()
    #
    # Public - copy
    #

    def copy(self):
        """
        Returns a new instance of a tree, consisting of new node instances.

        WARNING: This process only changes the reference for _object_stored_in_node. It does not attempt to do deep copies.

        Reasons:

        -Python's default process for deep copying many objects is prohibitively slow at run-time

        -This keeps with the general "pass by value" approach
        """
        return self.__class__(arg_data=self)
    #
    # Public - delete
    #

    def delete_key_to_node_child(self, arg_key):
        """
        This method deletes the key, and severs the connection to the child.

        This does not return a value.

        This will raise an exception if the key isn’t found.

        Argument:

        arg_key - This has the same behavior as a native dict key
        """
        if arg_key in self._dict_of_keys_and_node_children.keys():

            self._integrate_deallocate_node(arg_key=arg_key,
                                            arg_node=self._dict_of_keys_and_node_children[arg_key], )

        else:

            self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_key,
                                                         arg_node_start=self, )

    def delete_node_child(self, arg_node_child, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False):
        """
        This method looks for and then breaks the connection between the tree and the child node.

        By default, this method only looks for the arg_node_child in the host node’s immediate children.

        If the node is not found, the method will throw an exception.

        This method does not return a value.

        Arguments:

        arg_node_child - This is a node instance which already exists within the tree.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
        """
        if arg_bool_search_entire_tree or arg_bool_search_sub_tree:

            _stack_to_process_nodes = deque(
                [self._node_root if arg_bool_search_entire_tree else self])

            while _stack_to_process_nodes:

                item_node = _stack_to_process_nodes.pop()

                for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                    if item_node_child is arg_node_child:

                        self._integrate_deallocate_node(arg_node=item_node_child,
                                                        arg_key=item_key_child, )

                        return

                    _stack_to_process_nodes.append(item_node_child)
            #
            # Raise error because arg_node_child wasn't found.
            #
            self._raise_error_because_node_child_is_not_in_tree(arg_node_child=arg_node_child,
                                                                arg_node_root=self._node_root if arg_bool_search_entire_tree else self, )

        else:

            for item_key, item_node in self._dict_of_keys_and_node_children.items():

                if item_node is arg_node_child:

                    self._integrate_deallocate_node(arg_node=item_node,
                                                    arg_key=item_key, )

                    return
            #
            # Raise error if node wasn't found
            #
            self._raise_error_because_node_child_is_not_in_tree(arg_node_child=arg_node_child,
                                                                arg_node_root=self, )

    def delete_path_to_node_child(self, arg_path, arg_bool_path_is_absolute=False):
        """
        This method breaks all internal references to the node located at the path. This does not affect the other nodes along the path.

        This raises an exception if the path is not found.

        This method does not return a value.

        Arguments:

        arg_path - can be either a list of keys, or a delimited string.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        item_node = self._node_root if arg_bool_path_is_absolute else self

        _list_of_path_parts = self.get_list_of_keys_from_path(arg_path)

        for item_path_part in _list_of_path_parts:

            try:

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            except KeyError:

                self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_path,
                                                             arg_node_start=self._node_root if arg_bool_path_is_absolute else self, )

        self._integrate_deallocate_node(arg_node=item_node,
                                        arg_key=_list_of_path_parts[-1], )
    #
    # Public - get
    #

    def get(self, arg_path, arg_bool_search_entire_tree=False, arg_default_value_to_return=None):
        """
        Returns the node located at arg_path if the node has children. Otherwise, method returns the object stored
        within the node.

        If the path does not exist, method returns arg_default_value_to_return

        Arguments:

        arg_path - can be either a list of keys, or a delimited string.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        arg_default_value_to_return - The value returned of the path does not exist.
        """
        item_node = self._node_root if arg_bool_search_entire_tree else self

        for item_path_part in self.get_list_of_keys_from_path(arg_path):

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                return arg_default_value_to_return

        return item_node if item_node._dict_of_keys_and_node_children else item_node._object_stored_in_node
    #
    # Public - get - data
    #

    def get_data_in_format_for_export(self, arg_bool_search_entire_tree=False):
        """
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
        """
        _dict_from_tree = {}

        _node_start = self._node_root if arg_bool_search_entire_tree else self

        _stack_to_process_pairs_nodes_and_objects = deque(
            [[_node_start, _dict_from_tree, ]])

        while _stack_to_process_pairs_nodes_and_objects:

            item_node, item_object = _stack_to_process_pairs_nodes_and_objects.pop()
            #
            # Cycle through the sub-nodes for each sub node
            # If the sub node has children, then add it as a dict
            # If the sub node is a leaf node, then just add the object stored within it.
            #
            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                if item_node_child._dict_of_keys_and_node_children:

                    item_object_child = {}

                    item_object[item_key_child] = item_object_child

                    _stack_to_process_pairs_nodes_and_objects.append(
                        [item_node_child, item_object_child, ])

                else:

                    item_object[item_key_child] = item_node_child._object_stored_in_node

        return _dict_from_tree
    #
    # Public - get - deque
    #

    def get_deque_of_nodes(self, arg_bool_search_entire_tree=False, arg_bool_search_sub_tree=False, arg_bool_first_item_popped_is_leaf_node=False):
        """
        Returns a stack / deque of nodes within the tree.

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
        """
        if arg_bool_search_entire_tree or arg_bool_search_sub_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_return = deque([_node_start])

            _stack_to_process = deque([_node_start])

            while _stack_to_process:

                item_node = _stack_to_process.pop()

                for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():
                    #
                    # Next iteration
                    #
                    _stack_to_process.append(item_node_child)
                    #
                    # Append to stack to return
                    #
                    if arg_bool_first_item_popped_is_leaf_node:

                        _stack_to_return.append(item_node)

                    else:

                        _stack_to_return.appendleft(item_node)

            return _stack_to_return

        else:

            return deque(self._dict_of_keys_and_node_children.values())
    #
    # Public - get - dict
    #

    def get_dict_of_keys_and_node_children(self):
        """
        Returns a dict of the current node’s children and their associated keys.

        Note: This is intentionally meant to be a super simple method. For advanced
        functionality, use get_dict_of_string_paths_and_node_children()
        """
        return self._dict_of_keys_and_node_children
    #
    # Public - get - list - get_dict_of_string_paths_and_node_children
    #

    def get_dict_of_paths_and_node_children(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
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
        """
        if arg_bool_get_paths_as_strings:

            if arg_callable_formatter:

                self._raise_error_because_bool_get_paths_as_strings_and_callable_formatter_collide(arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                                   arg_callable_formatter=arg_callable_formatter, )

            else:

                def arg_callable_formatter(arg_path, arg_node): return [
                    self.get_string_path_from_arguments(arg_path), arg_node, ]

        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_dict_of_paths_and_node_children_with_filter_and_formatter(arg_node_start=_node_start,
                                                                                               arg_callable_filter=arg_callable_filter,
                                                                                               arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return self._get_dict_of_paths_and_node_children_with_filter(arg_node_start=_node_start,
                                                                                 arg_callable_filter=arg_callable_filter, )

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_dict_of_paths_and_node_children_with_formatter(arg_node_start=_node_start,
                                                                                    arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return self._get_dict_of_paths_and_node_children(arg_node_start=_node_start)

        else:

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    _dict_to_return = {}

                    for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items():

                        item_value_to_return = arg_callable_formatter(
                            [item_key_child], item_node_child, )

                        try:

                            _dict_to_return.__setitem__(*item_value_to_return)

                        except (TypeError, ValueError, ) as _error_message:

                            self._raise_error_because_attempt_to_add_dict_item_triggered_type_error(arg_path=item_key_child,
                                                                                                    arg_node=item_node_child,
                                                                                                    arg_dict=_dict_to_return,
                                                                                                    arg_value_returned_by_formatter=item_value_to_return,
                                                                                                    arg_error_message=_error_message, )

                    return _dict_to_return
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return {str(item_key_child): item_node_child
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()
                            if arg_callable_filter([item_key_child], item_node_child, )}

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    _dict_to_return = {}

                    for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items():

                        item_value_to_return = arg_callable_formatter(
                            [item_key_child], item_node_child, )

                        try:

                            _dict_to_return.__setitem__(*item_value_to_return)

                        except (TypeError, ValueError, ) as _error_message:

                            self._raise_error_because_attempt_to_add_dict_item_triggered_type_error(arg_path=item_key_child,
                                                                                                    arg_node=item_node_child,
                                                                                                    arg_dict=_dict_to_return,
                                                                                                    arg_value_returned_by_formatter=item_value_to_return,
                                                                                                    arg_error_message=_error_message, )

                    return _dict_to_return
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return {str(item_key_child): item_node_child
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()}
    #
    # Private - get - list - get_dict_of_string_paths_and_node_children - callable templates / examples
    #

    def template_for_arg_callable_filter_in_get_dict_of_paths_and_node_children(self, arg_iterable_path, arg_node):
        """
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
        """
        #
        # Return True, only when arg_node has no children
        #
        return not arg_node._dict_of_keys_and_node_children

    def template_for_arg_callable_formatter_in_get_dict_of_paths_and_node_children(self, arg_iterable_path, arg_node):
        """
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
        """
        #
        # Since get_dict_of_string_paths_and_node_children() returns a dict, the path needs to be hashable in the returned value.
        # Note: There's no tuple involved due to their time penalty
        #
        _string_path_hashable = self._string_delimiter_for_path.join(
            [str(item_path_part) for item_path_part in arg_iterable_path])
        #
        # The returned value needs to be an unpack-able pair
        #
        return [_string_path_hashable, arg_node._object_stored_in_node, ]
    #
    # Private - get - list - get_dict_of_string_paths_and_node_children - pseudo-overloaded methods
    #

    def _get_dict_of_paths_and_node_children(self, arg_node_start):
        """
        This is a support method for get_dict_of_paths_and_node_children()

        It returns a dict with paths as keys, and nodes as values.

        This method is the most basic and doesn't reference any callables.
        """
        _dict_to_return = {}

        _stack_to_process_paths_and_nodes = deque([[[], arg_node_start, ]])

        while _stack_to_process_paths_and_nodes:

            item_path, item_node = _stack_to_process_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = tuple([*item_path, item_key_child, ])

                _dict_to_return[item_path_child] = item_node_child

                _stack_to_process_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])

        return _dict_to_return

    def _get_dict_of_paths_and_node_children_with_filter(self, arg_node_start, arg_callable_filter):
        """
        This is a support method for get_dict_of_paths_and_node_children()

        It returns a dict with paths as keys, and nodes as values.

        This method references only arg_callable_filter.
        """
        _dict_to_return = {}

        _stack_to_process_paths_and_nodes = deque([[[], arg_node_start, ]])

        while _stack_to_process_paths_and_nodes:

            item_path, item_node = _stack_to_process_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = tuple([*item_path, item_key_child, ])

                if arg_callable_filter(item_path_child, item_node_child, ):

                    _dict_to_return[item_path_child] = item_node_child

                _stack_to_process_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])

        return _dict_to_return

    def _get_dict_of_paths_and_node_children_with_filter_and_formatter(self, arg_node_start, arg_callable_filter, arg_callable_formatter):
        """
        This is a support method for get_dict_of_paths_and_node_children()

        It returns a dict with paths as keys, and nodes as values.

        This method references arg_callable_filter and arg_callable_formatter.
        """
        _dict_to_return = {}

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = tuple([*item_path, item_key_child, ])
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add values to return
                #
                if arg_callable_filter(item_path_child, item_node_child, ):

                    item_value_to_return = arg_callable_formatter(
                        item_path_child, item_node_child, )

                    try:

                        _dict_to_return.__setitem__(*item_value_to_return)

                    except (TypeError, ValueError, ) as _error_message:

                        self._raise_error_because_attempt_to_add_dict_item_triggered_type_error(arg_path=item_path_child,
                                                                                                arg_node=item_node_child,
                                                                                                arg_dict=_dict_to_return,
                                                                                                arg_value_returned_by_formatter=item_value_to_return,
                                                                                                arg_error_message=_error_message, )

        return _dict_to_return

    def _get_dict_of_paths_and_node_children_with_formatter(self, arg_node_start, arg_callable_formatter):
        """
        This is a support method for get_dict_of_paths_and_node_children()

        It returns a dict with paths as keys, and nodes as values.

        This method references only arg_callable_formatter.
        """
        _dict_to_return = {}

        _stack_to_process_paths_and_nodes = deque([[[], arg_node_start, ]])

        while _stack_to_process_paths_and_nodes:

            item_path, item_node = _stack_to_process_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = tuple([*item_path, item_key_child, ])
                #
                # Prep next iteration
                #
                _stack_to_process_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Prep return values
                #
                item_value_to_return = arg_callable_formatter(
                    item_path_child, item_node_child, )

                try:
                    #
                    # Attempt to unpack item_value_to_return_formatted_to_iterable_if_necessary into __setitem__ arguments: 'key' and 'value'
                    #
                    _dict_to_return.__setitem__(*item_value_to_return)

                except (TypeError, ValueError) as _error_message:

                    self._raise_error_because_attempt_to_add_dict_item_triggered_type_error(arg_path=item_path_child,
                                                                                            arg_node=item_node_child,
                                                                                            arg_dict=_dict_to_return,
                                                                                            arg_value_returned_by_formatter=item_value_to_return,
                                                                                            arg_error_message=_error_message, )

        return _dict_to_return
    #
    # Public - get - id
    #

    def get_id_for_object_stored_in_node(self, arg_object):
        """
        RECOMMENDED_FOR_CUSTOM_OVERRIDES

        This method is used to generate and return unique ids for arg_object.

        This definition exists as a place holder, and not used in Data_tree_node.

        To see a functional definition for this method, check its definition in
        Data_tree_node_with_quick_lookup.
        """
        self._raise_error_because_method_needs_defined()
    #
    # Public - get - int
    #

    def get_int_count_for_node_children(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
        Returns the number of nodes in the tree.

        This does not count the root node of either search type.

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.

        arg_callable_filter - This method interprets the returned value of this callable as True / False.

        arg_callable_formatter - This method returns an int value, which is added to the total count returned by
        get_int_count_for_node_children()
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _int_count = 0

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_nodes = deque([_node_start])

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    while _stack_to_process_nodes:

                        item_node = _stack_to_process_nodes.pop()

                        for item_node_child in item_node._dict_of_keys_and_node_children.values():
                            #
                            # Prep next iteration
                            #
                            _stack_to_process_nodes.append(item_node_child)
                            #
                            # Filter
                            #
                            if arg_callable_filter(item_node_child):

                                _int_count += arg_callable_formatter(
                                    item_node_child)
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    while _stack_to_process_nodes:

                        item_node = _stack_to_process_nodes.pop()

                        for item_node_child in item_node._dict_of_keys_and_node_children.values():
                            #
                            # Prep next iteration
                            #
                            _stack_to_process_nodes.append(item_node_child)
                            #
                            # Filter
                            #
                            if arg_callable_filter(item_node_child):

                                _int_count += 1

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    while _stack_to_process_nodes:

                        item_node = _stack_to_process_nodes.pop()

                        for item_node_child in item_node._dict_of_keys_and_node_children.values():
                            #
                            # Prep next iteration
                            #
                            _stack_to_process_nodes.append(item_node_child)
                            #
                            # Increment count by value returned by arg_callable_formatter()
                            #
                            _int_count += arg_callable_formatter(
                                item_node_child)
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    while _stack_to_process_nodes:

                        item_node = _stack_to_process_nodes.pop()

                        for item_node_child in item_node._dict_of_keys_and_node_children.values():
                            #
                            # Prep next iteration
                            #
                            _stack_to_process_nodes.append(item_node_child)
                            #
                            # Increment count
                            #
                            _int_count += 1

            return _int_count

        else:

            return len(self._dict_of_keys_and_node_children)

    def template_example_for_arg_callable_filter_in_get_int_count_for_node_children(self, arg_node):
        '''
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
        '''
        return not arg_node._object_stored_in_node == None

    def template_example_for_arg_callable_formatter_in_get_int_count_for_node_children(self, arg_node):
        '''
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
        '''
        _object_stored_in_node = arg_node._object_stored_in_node

        if hasattr(_object_stored_in_node, "__len__", ):

            return len(_object_stored_in_node)

        elif _object_stored_in_node == None:

            return 0

        else:

            return 1
    #
    # Public - get - key
    #

    def get_key_for_node_child(self, arg_node_child):
        """
        Returns the key linking to the node if it’s found. If not, the method returns None.

        Argument:

        arg_node_child - This is a pre-existing node instance in the current node's immediate children.
        """
        _key = None

        for item_key, item_node_child in self._dict_of_keys_and_node_children.items():

            if item_node_child is arg_node_child:

                _key = item_key

                break

        return _key

    def get_list_of_keys_from_path(self, *args):
        """
        This returns a flat list comprised of the keys to navigate from this node to
        the node at the path.

        I settled on this approach to balance execution time and flexibility.

        Reminder about competing approaches and performance:

        List with basic append requires a list reversal at the end, followed by
        a reconversion to a list. This makes the approach slower.

        List with insert( 0, item, ) is slightly faster than above, but slower than
        the stack option actually implemented here.
        """
        if not args:

            return []

        else:

            _list = []

            _stack_to_process = deque(list(args))

            while _stack_to_process:

                item_object = _stack_to_process.pop()

                if isinstance(item_object, (deque, list, tuple, ), ):

                    _stack_to_process.extend(item_object)

                elif isinstance(item_object, str, ):

                    if self._string_delimiter_for_path in item_object:

                        _stack_to_process.extend(item_object.split(
                            self._string_delimiter_for_path))

                    else:

                        if item_object:

                            _list.insert(0, item_object, )

                else:

                    if item_object:

                        _list.insert(0, item_object, )

            return _list
    #
    # Public - get - list - get_list_of_pairs_paths_and_node_children
    #

    def get_list_of_pairs_paths_and_node_children(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
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
        """
        if arg_bool_get_paths_as_strings:
            #
            # Raise an exception if arg_bool_get_paths_as_strings collides with arg_callable_formatter
            # Reminder: Without this check, arg_bool_get_paths_as_strings rungs the risk of overriding the callable set for arg_callable_formatter
            #
            if arg_callable_formatter:

                self._raise_error_because_bool_get_paths_as_strings_and_callable_formatter_collide(arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                                   arg_callable_formatter=arg_callable_formatter, )

            else:

                def arg_callable_formatter(arg_path, arg_node): return [
                    self.get_string_path_from_arguments(arg_path), arg_node, ]

        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_list_of_pairs_paths_and_nodes_with_filter_and_formatter(arg_node_start=_node_start,
                                                                                             arg_callable_filter=arg_callable_filter,
                                                                                             arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return self._get_list_of_pairs_paths_and_nodes_with_filter(arg_node_start=_node_start,
                                                                               arg_callable_filter=arg_callable_filter, )

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_list_of_pairs_paths_and_nodes_with_formatter(arg_node_start=_node_start,
                                                                                  arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return self._get_list_of_pairs_paths_and_nodes(arg_node_start=_node_start)

        else:

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return [arg_callable_formatter([item_key_child], item_node_child, ) for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items() if arg_callable_filter(item_key_child, item_node_child, )]
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return [[[item_key_child], item_node_child, ] for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items() if arg_callable_filter(item_key_child, item_node_child, )]

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return [arg_callable_formatter([item_key_child], item_node_child, ) for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()]
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return [[[item_key_child], item_node_child, ] for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()]
    #
    # Private - get - list - get_list_of_pairs_paths_and_node_children - callable templates / examples
    #

    def template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children(self, *args):
        """
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
        """
        return not args[1]._dict_of_keys_and_node_children

    def template_example_for_arg_callable_formatter_in_get_list_of_pairs_paths_and_node_children(self, *args):
        """
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
        """
        _string_path = self._string_delimiter_for_path.join(
            [str(item_path_part) for item_path_part in args[0]])

        return [_string_path, args[1]._object_stored_in_node, ]
    #
    # Private - get - list - get_list_of_pairs_paths_and_node_children - pseudo-overloaded methods
    #

    def _get_list_of_pairs_paths_and_nodes(self, arg_node_start):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children()

        It returns a basic list of pairs without referencing any callables.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                _list_to_return.append([item_path_child, item_node_child, ])

        return _list_to_return

    def _get_list_of_pairs_paths_and_nodes_with_filter(self, arg_node_start, arg_callable_filter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children()

        It returns a list of pairs while only referencing arg_callable_filter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if arg_callable_filter(item_path_child, item_node_child, ):

                    _list_to_return.append(
                        [item_path_child, item_node_child, ])

        return _list_to_return

    def _get_list_of_pairs_paths_and_nodes_with_filter_and_formatter(self, arg_node_start, arg_callable_filter, arg_callable_formatter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children()

        It returns a list of pairs while referencing arg_callable_filter and arg_callable_formatter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if arg_callable_filter(item_path_child, item_node_child, ):

                    _list_to_return.append(arg_callable_formatter(
                        item_path_child, item_node_child, ))

        return _list_to_return

    def _get_list_of_pairs_paths_and_nodes_with_formatter(self, arg_node_start, arg_callable_formatter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children()

        It returns a list of pairs while only referencing arg_callable_formatter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                _list_to_return.append(arg_callable_formatter(
                    item_path_child, item_node_child, ))

        return _list_to_return
    #
    # Public - get - list - get_list_of_pairs_paths_and_node_children_relevant_to_object
    #

    def get_list_of_pairs_paths_and_node_children_relevant_to_object(self, arg_object, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
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
        """
        if arg_bool_get_paths_as_strings:
            #
            # Raise an exception if arg_bool_get_paths_as_strings collides with arg_callable_formatter
            # Reminder: Without this check, arg_bool_get_paths_as_strings rungs the risk of overriding the callable set for arg_callable_formatter
            #
            if arg_callable_formatter:

                self._raise_error_because_bool_get_paths_as_strings_and_callable_formatter_collide(arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                                   arg_callable_formatter=arg_callable_formatter, )

            else:

                def arg_callable_formatter(arg_path, arg_node): return [
                    self.get_string_path_from_arguments(arg_path), arg_node, ]

        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter_and_formatter(arg_object=arg_object,
                                                                                                                        arg_node_start=_node_start,
                                                                                                                        arg_callable_filter=arg_callable_filter,
                                                                                                                        arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return self._get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter(arg_object=arg_object,
                                                                                                          arg_node_start=_node_start,
                                                                                                          arg_callable_filter=arg_callable_filter, )

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return self._get_list_of_pairs_paths_and_node_children_relevant_to_object_with_formatter(arg_object=arg_object,
                                                                                                             arg_node_start=_node_start,
                                                                                                             arg_callable_formatter=arg_callable_formatter, )
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return self._get_list_of_pairs_paths_and_node_children_relevant_to_object(arg_object=arg_object,
                                                                                              arg_node_start=_node_start, )

        else:

            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return [arg_callable_formatter([item_key_child], item_node_child, )
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()
                            if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ) and arg_callable_filter([item_key_child], item_node_child, )]
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return [[[item_key_child], item_node_child, ]
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()
                            if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ) and arg_callable_filter([item_key_child], item_node_child, )]

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    return [[arg_callable_formatter([item_key_child], item_node_child, )]
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()
                            if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, )]
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return [[[item_key_child], item_node_child, ]
                            for item_key_child, item_node_child in self._dict_of_keys_and_node_children.items()
                            if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, )]
    #
    # Private - get - list - get_list_of_pairs_paths_and_node_children_relevant_to_object - callable templates / examples
    #

    def template_example_for_arg_callable_filter_in_get_list_of_pairs_paths_and_node_children_relevant_to_object(self, *args):
        """
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
        """
        return not args[1]._dict_of_keys_and_node_children

    def template_example_for_arg_callable_formatter_in_get_list_of_pairs_paths_and_node_children_relevant_to_object(self, *args):
        """
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
        """
        _string_path = self._string_delimiter_for_path.join(
            [str(item_path_part) for item_path_part in args[0]])

        return [_string_path, args[1]._object_stored_in_node, ]
    #
    # Private - get - list - get_list_of_pairs_paths_and_node_children_relevant_to_object - pseudo-overloaded methods
    #

    def _get_list_of_pairs_paths_and_node_children_relevant_to_object(self, arg_object, arg_node_start):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children_relevant_to_object()

        It returns a list of pairs, paths and nodes without referencing any callables.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ):

                    _list_to_return.append(
                        [item_path_child, item_node_child, ])

        return _list_to_return

    def _get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter(self, arg_object, arg_node_start, arg_callable_filter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children_relevant_to_object()

        It returns a list of pairs, paths and nodes, referencing arg_callable_filter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ):

                    if arg_callable_filter(item_path_child, item_node_child, ):

                        _list_to_return.append(
                            [item_path_child, item_node_child, ])

        return _list_to_return

    def _get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter_and_formatter(self, arg_object, arg_node_start, arg_callable_filter, arg_callable_formatter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children_relevant_to_object()

        It returns a list of pairs, paths and nodes, referencing arg_callable_filter and arg_callable_formatter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ):

                    if arg_callable_filter(item_path_child, item_node_child, ):

                        _list_to_return.append(arg_callable_formatter(
                            item_path_child, item_node_child, ))

        return _list_to_return

    def _get_list_of_pairs_paths_and_node_children_relevant_to_object_with_formatter(self, arg_object, arg_node_start, arg_callable_formatter):
        """
        This is a support method for get_list_of_pairs_paths_and_node_children_relevant_to_object()

        It returns a list of pairs, paths and nodes, referencing arg_callable_formatter.
        """
        _list_to_return = []

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], arg_node_start, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_child = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_pairs_paths_and_nodes.append(
                    [item_path_child, item_node_child, ])
                #
                # Add return values to return list
                #
                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ):

                    _list_to_return.append(arg_callable_formatter(
                        item_path_child, item_node_child, ))

        return _list_to_return
    #
    # Public - get - list - path
    #

    def get_list_path_from_arguments(self, *args):
        """
        Returns args in the form of a list based on args' contents.
        """
        return self._get_list_by_combining_arguments(*args)
    #
    # Public - get - node
    #

    def get_node_child_at_key(self, arg_key, arg_default_value_to_return=None):
        """
        Returns the child node located at arg_key if it exists; otherwise, returns arg_default_value_to_return.

        arg_key - The target key for the node child in question.

        arg_default_value_to_return - This is the automatically returned value if the key does not exist in the tree.
        """
        if arg_key in self._dict_of_keys_and_node_children.keys():

            return self._dict_of_keys_and_node_children[arg_key]

        else:

            return arg_default_value_to_return

    def get_node_child_at_path(self, arg_path, arg_bool_path_is_absolute=False, arg_default_value_to_return=None):
        """
        Returns the node located at arg_path.

        If the path doesn’t exist in the tree, then the method will return arg_default_value_to_return.

        Arguments:

        arg_path - can be either a list of keys, or a delimited string.

        arg_default_value_to_return - This is the automatically returned value if the path does not exist in the tree.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree of the current node.
        """
        item_node = self._node_root if arg_bool_path_is_absolute else self

        for item_path_part in self.get_list_of_keys_from_path(arg_path):

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                return arg_default_value_to_return

        return item_node

    def get_node_new_instance(self):
        """
        IMPORTANT_FOR_BUILDING_TREE

        Typically called by the following methods if no arg_node provided...
        append_key()
        append_path()

        Creates a new node, which uses the same delimiter as the node creating it.

        Reminder: This specific call happens enough to justify its own method for safety reasons.
        """
        if self._bool_string_delimiter_for_path_is_default:

            return self._type_to_use_for_node_children()

        # If the delimiter isn't the same as the default, then pass the custom delimiter to the new node.
        else:

            return self._type_to_use_for_node_children(arg_string_delimiter_for_path=self._string_delimiter_for_path)

    def get_node_parent(self):
        """
        Returns the node’s parent node, if it exists, otherwise, the returned value is None.
        """
        return self._node_parent

    def get_node_root(self):
        """
        Returns the root node for the entire tree.

        Note: If the root node calls this method, it will return itself.
        """
        return self._node_root
    #
    # Public - get - object
    #

    def get_object_at_key(self, arg_key, arg_default_value_to_return=None):
        """
        Returns the object stored within the child node located at the key.

        If the key doesn’t exist, then the method will return arg_default_value_to_return.
        """
        if arg_key in self._dict_of_keys_and_node_children.keys():

            return self._dict_of_keys_and_node_children[arg_key]

        else:

            return arg_default_value_to_return

    def get_object_at_path(self, arg_path, arg_bool_path_is_absolute=False, arg_default_value_to_return=None):
        """
        Returns the object stored within the node located at the path.

        If the path does not exist, then the method will return arg_default_value_to_return.

        Arguments:

        arg_path - can be either a list of keys, or a delimited string.

        arg_default_value_to_return - This is the default value returned if the path does not exist.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        item_node = self._node_root if arg_bool_path_is_absolute else self

        for item_path_part in self.get_list_of_keys_from_path(arg_path):

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                return arg_default_value_to_return

        return item_node._object_stored_in_node

    def get_object_stored_in_node(self, arg_path=None, arg_bool_path_is_absolute=False, arg_default_value_to_return=None):
        """
        Returns the object stored within node.

        If arg_path is None, then the method returns the object stored in the current node.

        Arguments:

        arg_path - can either a list of keys, a delimited string, or None. If the value is None, this method returns the value in
        arg_default_value_to_return.

        Note: arg_default_value_to_return is not honored if arg_path is None.

        If arg_path is defined, then the method will retrieve the object stored in the node at the path.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        if arg_path == None:

            return self._object_stored_in_node

        else:

            _node = self.get_node_child_at_path(
                arg_path=arg_path, arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

            if _node == None:

                return arg_default_value_to_return

            else:

                return _node._object_stored_in_node
    #
    # Public - get - path
    #

    def get_path_to_node_child(self, arg_node_child, arg_bool_search_entire_tree=False, arg_bool_raise_error_if_node_is_not_in_tree=True, arg_default_value_to_return=None, arg_bool_get_path_as_string=False):
        """
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
        """
        _deque_of_path_parts = deque()

        item_node = arg_node_child

        _node_to_check_is_self_or_parent = self._node_root if arg_bool_search_entire_tree else self

        _bool_current_node_detected_along_path = False

        while not item_node._node_parent == None:

            item_node_parent = item_node._node_parent
            #
            # Check to see if current node is found along the path
            #
            if item_node_parent is _node_to_check_is_self_or_parent:

                _bool_current_node_detected_along_path = True

            for item_key, item_node_child in item_node_parent._dict_of_keys_and_node_children.items():

                if item_node_child is item_node:

                    _deque_of_path_parts.appendleft(item_key)

            item_node = item_node_parent

        if _bool_current_node_detected_along_path:

            return self._string_delimiter_for_path.join(_deque_of_path_parts) if arg_bool_get_path_as_string else list(_deque_of_path_parts)

        else:

            if arg_bool_raise_error_if_node_is_not_in_tree:

                _node_to_check_is_self_or_parent._raise_error_because_node_child_is_not_in_tree(arg_node_child=arg_node_child,
                                                                                                arg_node_root=_node_to_check_is_self_or_parent, )

            else:

                return arg_default_value_to_return
    #
    # Public - get - string
    #

    def get_string_delimiter_for_string_paths(self):
        """
        Returns self._string_delimiter_for_path so users can use without
        explicitly having to know what it is.
        """
        return self._string_delimiter_for_path

    def get_string_path_from_arguments(self, *args):
        """
        This takes *args in whatever format, and attempts to form a delimited string out of it.

        This method can handle nested data structures.

        Examples of valid arguments (not comprehensive):

        get_string_path_from_arguments( 1, 2, 3 )

        get_string_path_from_arguments( "1", "2", "3" )

        get_string_path_from_arguments( [ 1, 2, 3, ] )

        get_string_path_from_arguments( [ 1, [[[ 2 ]], [ 3 ]], ] )
        """
        if args:

            return self._get_strings_combined(self.get_list_of_keys_from_path(*args),
                                              arg_delimiters=self._string_delimiter_for_path, )

        else:

            return ""
    #
    # Public - get - tuple
    #

    def get_tuple_of_keys_from_path(self, *args):
        """
        Returns a tuple compiled from args.

        args can be multiple objects, even nested within each other.

        Data_tree_node_with_quick_lookup makes use of this method for hashing.
        """
        return tuple(self.get_list_of_keys_from_path(*args))
    #
    # Public - get - type
    #

    def get_type_to_use_for_node_children(self):
        """
        RECOMMENDED_FOR_CUSTOM_OVERRIDES

        Returns the type used for new child nodes generated within this tree.
        """
        return self._type_to_use_for_node_children
    #
    # Public - items
    #

    def items(self, arg_bool_search_sub_tree=False, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False):
        """
        This method is designed to behave similarly to dict.items(), and yields a list pair, with the path in index 0, and the
        corresponding node in index 1.

        Arguments:

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        arg_bool_get_paths_as_strings - If True, yields the path as a string, otherwise, the method returns the path
        as a list of keys.
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_pairs_paths_and_nodes = deque(
                [[[], _node_start, ]])

            if arg_bool_get_paths_as_strings:

                while _stack_to_process_pairs_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield [self._string_delimiter_for_path.join([str(item_path_part) for item_path_part in item_path_child]),
                               item_node if item_node._dict_of_keys_and_node_children else item_node._object_stored_in_node]
                        #
                        # Next iteration
                        #
                        _stack_to_process_pairs_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

            else:

                while _stack_to_process_pairs_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield [item_path_child,
                               item_node if item_node._dict_of_keys_and_node_children else item_node._object_stored_in_node]
                        #
                        # Next iteration
                        #
                        _stack_to_process_pairs_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

        else:

            return self._dict_of_keys_and_node_children.items()
    #
    # Public - keys
    #

    def keys(self, arg_bool_search_sub_tree=False, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False):
        """
        This method supports iterating across the tree, similarly to dict.keys()

        Arguments:

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_get_paths_as_strings - If True, the method returns paths as delimited strings. If False, this returns
        the paths as lists of keys.
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_pairs_of_paths_and_nodes = deque(
                [[[], _node_start, ]])

            if arg_bool_get_paths_as_strings:

                while _stack_to_process_pairs_of_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_of_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield self._string_delimiter_for_path.join([str(item_path_part) for item_path_part in item_path_child])
                        #
                        # Prep next iteration
                        #
                        _stack_to_process_pairs_of_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

            else:

                while _stack_to_process_pairs_of_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_of_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield item_path_child
                        #
                        # Prep next iteration
                        #
                        _stack_to_process_pairs_of_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

        else:

            if arg_bool_get_paths_as_strings:

                for item_key_child in self._dict_of_keys_and_node_children.keys():

                    yield str(item_key_child)

            else:

                for item_key_child in self._dict_of_keys_and_node_children.keys():

                    yield [item_key_child]
    #
    # Public - logic
    #

    def logic_data_is_in_correct_format(self, arg_data):
        """
        Returns True if arg_data is in one of the three formats setup_tree_based_on_data_structure() takes.

        This is here primarily for debugging and data validation.

        For this method to return True, arg_data needs to be one of the following:

        -A simple dict
        -A nested dict
        -A list of nested dicts
        -Another data_tree_node
        """
        if isinstance(arg_data, dict, ):

            return True

        elif isinstance(arg_data, list, ):

            return all([isinstance(item, dict, ) for item in arg_data])

        elif isinstance(arg_data, self._type_to_use_for_node_children, ):

            return True

        return False

    def logic_key_exists(self, arg_key):
        """
        Returns True, if the key exists for a child node.

        Argument:

        arg_key - obeys the same rules as regular dictionary keys.
        """
        return arg_key in self._dict_of_keys_and_node_children.keys()

    def logic_objects_match(self, arg_object_one, arg_object_two):
        """
        RECOMMENDED_FOR_CUSTOM_OVERRIDES

        Typically called by...
        _get_list_of_pairs_paths_and_node_children_relevant_to_object()
        _get_list_of_pairs_paths_and_node_children_relevant_to_object_with_filter()
        _get_list_of_pairs_paths_as_strings_and_node_children_relevant_to_object()
        _get_list_of_pairs_paths_as_strings_and_node_children_relevant_to_object_with_filter()
        get_list_of_pairs_paths_and_node_children_relevant_to_object()

        This is a drop-in method for potential custom comparisons in inheriting classes.
        """
        return arg_object_one == arg_object_two

    def logic_path_exists(self, arg_path, arg_bool_path_is_absolute=False):
        """
        Returns True, if the path exists within the tree, and False if not.

        Arguments:

        arg_path - Can be a delimited string or list of keys.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        item_node = self._node_root if arg_bool_path_is_absolute else self

        for item_path_part in self.get_list_of_keys_from_path(arg_path):

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                return False

        return True

    def logic_path_is_leaf_node(self, arg_path, arg_bool_path_is_absolute=False):
        """
        Returns True, if the path exists in the tree, and the node at the path has no children.

        Arguments:

        arg_path - This can be a delimited string, or a list of keys.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        _node = self.get_node_child_at_path(arg_path=arg_path,
                                            arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        if _node == None:

            return False

        else:

            return not bool(_node._dict_of_keys_and_node_children)
    #
    # Public - nodes
    #

    def nodes(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False):
        """
        This method supports iteration similarly to dict.values().

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_nodes = deque([_node_start])

            while _stack_to_process_nodes:

                item_node = _stack_to_process_nodes.pop()

                for item_node_child in item_node._dict_of_keys_and_node_children.values():
                    #
                    # Yield value
                    #
                    yield item_node_child
                    #
                    # Prep next iteration
                    #
                    _stack_to_process_nodes.append(item_node_child)

        else:

            for item_node_child in self._dict_of_keys_and_node_children.values():

                yield item_node_child
    #
    # Public - paths
    #

    def paths(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_bool_get_paths_as_strings=False):
        """
        This method supports iteration similarly to dict.keys()

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        arg_bool_get_paths_as_strings - If True, returns each path as a delimited string. If False, the
        returned path is a list of keys.
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_pairs_paths_and_nodes = deque(
                [[[], _node_start, ]])

            if arg_bool_get_paths_as_strings:

                while _stack_to_process_pairs_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield self._string_delimiter_for_path.join([str(item_path_part) for item_path_part in item_path_child])
                        #
                        # Next iteration
                        #
                        _stack_to_process_pairs_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

            else:

                while _stack_to_process_pairs_paths_and_nodes:

                    item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

                    for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                        item_path_child = [*item_path, item_key_child, ]
                        #
                        # Yield value
                        #
                        yield item_path_child
                        #
                        # Next iteration
                        #
                        _stack_to_process_pairs_paths_and_nodes.append(
                            [item_path_child, item_node_child, ])

        else:

            if arg_bool_get_paths_as_strings:

                for item_key_child in self._dict_of_keys_and_node_children.keys():

                    yield str(item_key_child)

            else:

                for item_key_child in self._dict_of_keys_and_node_children.keys():

                    yield [item_key_child]
    #
    # Public - pop
    #

    def pop(self, arg_path, arg_default_value_to_return=_OBJECT_FOR_RAISING_ERRORS, arg_bool_path_is_absolute=False):
        """
        This method behaves similarly to dict.pop()

        Returns the object stored in the node located at arg_path; then removes the node and all its
        sub nodes. If arg_path doesn’t exist, returns arg_default_value_to_return.

        Arguments:

        arg_default_value_to_return - This is the returned value, if arg_path isn't in the tree.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.

        Note: This is a wrapper to mimic dict’s pop method.
        """
        _node = self._node_root if arg_bool_path_is_absolute else self

        return _node.pop_path(arg_path=arg_path,
                              arg_default_value_to_return=arg_default_value_to_return,
                              arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Public - pop - key
    #

    def pop_key(self, arg_key, arg_default_value_to_return=_OBJECT_FOR_RAISING_ERRORS):
        """
        Returns the object stored in the child node at arg_key; and removes the node and all its sub nodes as well. If arg_key doesn’t exist,
        returns arg_default_value_to_return.

        If arg_key does not exist, and arg_default_value_to_return isn't set, then this method will raise an error.

        Arguments:

        arg_key - This obeys the same rules as a key used in a dict.

        arg_default_value_to_return - This is the default value returned if the key does not exist.
        """
        _node_or_object = self.pop_key_to_node_child(arg_key=arg_key,
                                                     arg_default_value_to_return=arg_default_value_to_return, )

        if _node_or_object is arg_default_value_to_return:

            return _node_or_object

        else:

            if _node_or_object._dict_of_keys_and_node_children:

                return _node_or_object

            else:

                return _node_or_object._object_stored_in_node

    def pop_key_to_node_child(self, arg_key, arg_default_value_to_return=_OBJECT_FOR_RAISING_ERRORS):
        """
        Returns the child node located at arg_key; and removes the node and all its sub nodes.
        If arg_key doesn’t exist, returns arg_default_value_to_return.

        Note: This method is an explicit request for the node, instead of the object stored within it.

        Arguments:

        arg_key - This obeys the same rules as a normal dict key.

        arg_default_value_to_return - This is the default value returned if arg_key doesn't exist.
        """
        _node = None

        if arg_default_value_to_return is _OBJECT_FOR_RAISING_ERRORS:

            try:

                _node = self._dict_of_keys_and_node_children[arg_key]

            except KeyError:

                self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_key,
                                                             arg_node_start=self, )

        else:

            if arg_key in self._dict_of_keys_and_node_children.keys():

                _node = self._dict_of_keys_and_node_children[arg_key]

            else:

                return arg_default_value_to_return

        self._integrate_deallocate_node(arg_key=arg_key,
                                        arg_node=_node, )

        return _node
    #
    # Public - pop - node
    #

    def pop_node_child(self, arg_node_child, arg_bool_search_entire_tree=False, arg_default_value_to_return=None):
        """
        Returns the path to the node; and removes the node. If arg_node doesn’t exist, returns arg_default_value_to_return.

        Arguments:

        arg_default_value_to_return - This is the default value returns if arg_node_child doesn't exist within the searched area.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Rational behind returning the path:

        If the dev is using the node object, then they already have access to the object stored within the node. The info
        that isn't necessarily easy to come by is what gets returned, which in this case would be the path.
        """
        if arg_node_child._node_parent == None:

            return arg_default_value_to_return

        _path = self.get_path_to_node_child(arg_node_child=arg_node_child,
                                            arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                            arg_bool_raise_error_if_node_is_not_in_tree=False, )

        if _path == None:

            return arg_default_value_to_return

        else:

            self._integrate_deallocate_node(arg_key=_path[-1],
                                            arg_node=arg_node_child, )

            return _path
    #
    # Public - pop - path
    #

    def pop_path(self, arg_path, arg_bool_path_is_absolute=False, arg_default_value_to_return=_OBJECT_FOR_RAISING_ERRORS):
        """
        This method is an explicit wrapper for pop()

        If the node has no children, then this method return's the node stored at that location.

        Otherwise, it returns the node itself.

        Arguments:

        arg_path - This is the path to the node. It can either be a delimited string, or a list of keys.

        arg_default_value_to_return - This is the default value returned if arg_path does not exist in the searched area.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        _node_or_default_object = self.pop_path_to_node_child(arg_path=arg_path,
                                                              arg_bool_path_is_absolute=arg_bool_path_is_absolute,
                                                              arg_default_value_to_return=arg_default_value_to_return, )

        if _node_or_default_object is arg_default_value_to_return:

            return _node_or_default_object

        else:

            if _node_or_default_object._dict_of_keys_and_node_children:

                return _node_or_default_object

            else:

                return _node_or_default_object._object_stored_in_node

    def pop_path_to_node_child(self, arg_path, arg_bool_path_is_absolute=False, arg_default_value_to_return=_OBJECT_FOR_RAISING_ERRORS):
        """
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
        """
        _node_start = self._node_root if arg_bool_path_is_absolute else self

        item_node = _node_start

        _list_of_path_parts = self.get_list_of_keys_from_path(arg_path)

        if arg_default_value_to_return == _OBJECT_FOR_RAISING_ERRORS:

            for item_path_part in _list_of_path_parts:

                try:

                    item_node = item_node._dict_of_keys_and_node_children[item_path_part]

                except KeyError:

                    self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_path,
                                                                 arg_node_start=_node_start, )

        else:

            for item_path_part in _list_of_path_parts:

                if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                    item_node = item_node._dict_of_keys_and_node_children[item_path_part]

                else:

                    return arg_default_value_to_return

        self._integrate_deallocate_node(arg_key=_list_of_path_parts[-1],
                                        arg_node=item_node, )

        return item_node
    #
    # Public - print
    #

    def print_object(self, arg_object, arg_name_for_object=None):
        """
        This method prints information in a reasonably easy to read format, and
        compensates for some formatting challenges in pprint.

        Reminder: Processes like Cythonize do not like a self.print() method, so this
        had to be changed to print_object.

        Arguments:

        arg_object - This can be pretty much anything.

        arg_name_for_object - If this contains a value, then the name provided
        is displayed above arg_object's printed information. If this value is None
        then only arg_object's info will print.
        """
        if not arg_name_for_object == None:

            print(arg_name_for_object, "=", )

        print("\n".join(self._print_info_get_list_of_strings_formatted(
            arg_object)), "\n\n", )

    def print_tree(self, arg_bool_search_entire_tree=False, arg_names_for_attributes_to_print=None):
        """
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
        """
        _list_of_names_for_attributes_to_print = sorted(
            self._get_list_converted_from_object(arg_names_for_attributes_to_print))

        print("---PRINTING TREE---\n")

        _stack_to_process_pairs_paths_and_nodes = deque(
            [[[], self._node_root if arg_bool_search_entire_tree else self, ]])

        while _stack_to_process_pairs_paths_and_nodes:

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            if _list_of_names_for_attributes_to_print == None:

                self._print_node(arg_path=item_path,
                                 arg_node=item_node, )

            else:

                self._print_node(arg_path=item_path,
                                 arg_node=item_node,
                                 arg_list_of_names_for_attributes_to_print=_list_of_names_for_attributes_to_print, )

            if item_node._dict_of_keys_and_node_children:

                for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                    item_path_child = [*item_path, item_key_child, ]

                    _stack_to_process_pairs_paths_and_nodes.append(
                        [item_path_child, item_node_child, ])
    #
    # Public - set
    #

    def set_object_stored_in_node(self, arg_object, arg_path=None, arg_bool_path_is_absolute=False):
        """
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
        """
        _node = self._node_root if arg_bool_path_is_absolute else self

        if arg_path == None:

            _node._object_stored_in_node = arg_object

            return _node

        else:

            _node = _node.append_path(arg_path=arg_path)

            _node._object_stored_in_node = arg_object

            return _node
    #
    # Public - setup
    #

    def setup_tree_based_on_data_structure(self, arg_data, arg_keys_for_categorizing_nodes=None, arg_bool_search_entire_tree=False):
        """
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
        """
        _node_main = self._node_root if arg_bool_search_entire_tree else self
        #
        # Make sure tree is empty
        #
        _node_main.clear()
        #
        # Data analysis and conversion
        #
        # Dict
        #
        if isinstance(arg_data, dict, ):

            _stack_to_process_pairs_nodes_and_objects = deque(
                [[_node_main, arg_data, ]])

            while _stack_to_process_pairs_nodes_and_objects:

                item_node, item_dict = _stack_to_process_pairs_nodes_and_objects.pop()

                for item_key_child, item_object_child in item_dict.items():

                    item_node_child = _node_main.get_node_new_instance()
                    #
                    # Prep next iteration, or store object in node
                    #
                    if isinstance(item_object_child, dict, ):

                        _stack_to_process_pairs_nodes_and_objects.append(
                            [item_node_child, item_object_child, ])

                    else:

                        item_node_child._object_stored_in_node = item_object_child
                    #
                    # Allocate node in tree
                    #
                    # Reminder: This also handles integration with the root node
                    #
                    _node_main._integrate_allocate_node(arg_key=item_key_child,
                                                        arg_node=item_node_child,
                                                        arg_node_parent=item_node, )

            return
        #
        # List of dicts
        #
        # Reminder: we do this spot check, instead of running logic_data_is_in_correct_format(),
        # to keep processing times to a minimum.
        #
        if isinstance(arg_data, list, ):

            if arg_data:

                if isinstance(arg_data[0], dict, ):

                    if arg_keys_for_categorizing_nodes == None:

                        _node_main._dict_of_keys_and_node_children = {item_index: arg_data[item_index]
                                                                      for item_index in range(0, len(arg_data), )}

                        return

                    else:

                        _list_of_keys_for_categorizing_nodes = _node_main._get_list_converted_from_object(
                            arg_keys_for_categorizing_nodes)

                        for item_dict in arg_data:

                            item_node = _node_main

                            for item_key in _list_of_keys_for_categorizing_nodes:

                                item_node_new = _node_main.get_node_new_instance()

                                item_key_for_categorizing = item_dict[item_key]

                                _node_main._integrate_allocate_node(arg_key=item_key_for_categorizing,
                                                                    arg_node=item_node_new,
                                                                    arg_node_parent=item_node, )

                                item_node = item_node_new

                            item_node._object_stored_in_node = item_dict

                        return
        #
        # Another tree
        #
        # Reminder: This instance type check will work on classes inheriting this class.
        #
        if isinstance(arg_data, self._type_to_use_for_node_children, ):

            _stack_to_process_pairs_nodes_external_and_internal = deque(
                [[arg_data, _node_main, ]])

            while _stack_to_process_pairs_nodes_external_and_internal:

                item_node_external, item_node_internal = _stack_to_process_pairs_nodes_external_and_internal.pop()

                item_node_internal._object_stored_in_node = item_node_external._object_stored_in_node

                for item_key_child, item_node_external_child in item_node_external._dict_of_keys_and_node_children.items():

                    item_node_internal_child = _node_main.get_node_new_instance()

                    item_node_internal._dict_of_keys_and_node_children[
                        item_key_child] = item_node_internal_child

                    _stack_to_process_pairs_nodes_external_and_internal.append(
                        [item_node_external_child, item_node_internal_child, ])

            return

        _node_main._raise_error_because_arg_data_is_an_invalid_format(arg_data)
    #
    # Public - values
    #

    def values(self, arg_bool_search_sub_tree=False, arg_bool_search_entire_tree=False):
        """
        Supports iteration similarly to dict.values()

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.
        """
        if arg_bool_search_sub_tree or arg_bool_search_entire_tree:

            _node_start = self._node_root if arg_bool_search_entire_tree else self

            _stack_to_process_nodes = deque([_node_start])

            while _stack_to_process_nodes:

                item_node = _stack_to_process_nodes.pop()

                for item_node_child in item_node._dict_of_keys_and_node_children.values():
                    #
                    # Yield value
                    #
                    yield item_node_child
                    #
                    # Next iteration
                    #
                    _stack_to_process_nodes.append(item_node_child)

        else:

            for item_node_child in self._dict_of_keys_and_node_children.values():

                yield item_node_child
    #
    # Private
    #
    #
    # Private - get
    #

    def _get_key_that_is_last_in_path(self, arg_path):
        """
        This returns the last key in a path, regardless of its size or data type.
        """
        if isinstance(arg_path, str, ):

            return arg_path.rsplit(self._string_delimiter_for_path, 1, )[-1] if self._string_delimiter_for_path in arg_path else arg_path

        else:

            return arg_path[-1]
    #
    # Private - get - list
    #

    def _get_list_by_combining_arguments(self, *args):
        """
        This method returns a flat list of all arguments in args.

        args can be a single value, or any data type that supports indexes ( i.e. lists and tuples )

        If there's a nested list / tuple present, its flattened.
        Note: I tried the native equivalent of this functionality and it
        didn't seem to handle nested lists beyond two levels.

        There's no limit to how deep the nested list can be.

        Reminder:
        List with basic append requires a list reversal at the end, followed by
        a reconversion to a list. This makes the approach slower.

        List with insert( 0, item, ) is slightly faster than above, but slower than
        this stack option.

        Example of a nested argument:

        [ "1", [ "2", [ "3" ], [ [ "4" ] ], ], ]

        Result:

        [ "1", "2", "3", "4", ]
        """
        _list = []

        # Deque is notably faster than lists for stacks
        _stack = deque([item for item in args])

        while _stack:

            item = _stack.pop()

            if isinstance(item, (deque, list, tuple, ), ):

                _stack.extend(item)
            #
            # If its a tuple, then extend
            #
            else:

                _list.insert(0, item, )

        return _list

    def _get_list_converted_from_object(self, arg_object):
        """
        This method ensures we always know we're working with a list. Its a work-horse
        method for supporting multiple data types.

        If arg_object is None, it returns an empty list.

        If arg_object is a list-like iterable, it converts it to a list.

        In all other cases, it returns a list containing arg_object.

        Reminder: list() is slightly faster overall than list comprehension.

        Notes:

            Performance wise, lists appear to trounce most other data structures
            except in specific tasks, so in general, its better to default to
            these until there's a clear reason to use something else.
        """
        # All scenarios assume a list is coming out of this method, so if the
        # value is none, then make it an empty list
        if arg_object == None:

            return []

        # By default, this returns the list argument "as-is."  If we want the copy
        # however, this calls the copy library.
        elif isinstance(arg_object, (deque, list, set, tuple, ), ):

            return list(arg_object)

        # This creates a new list regardless of the scenario.
        else:

            return [arg_object]
    #
    # Private - get - name
    #

    def _get_name_for_host_method(self, arg_int_depth=1):
        '''
        if arg_int_depth == 0 : output = "get_string_name_method"

        if arg_int_depth == 1 : output = the name of the method calling get_string_name_method()
        '''
        return sys._getframe(arg_int_depth).f_code.co_name
    #
    # Private - get - strings
    #

    def _get_strings_combined(self, *args, arg_delimiters=""):
        """
        This method is virtually the same as "".join() except it can handle nested objects with infinite
        depth.

        Arguments:

        args - This can be multiple values, and supported nested data structures like lists within lists.

        arg_delimiters - This is the same as what you would put between the quotes in "".join()
        """
        return arg_delimiters.join([str(item) for item in self._get_list_by_combining_arguments(args)])
    #
    # Private - integrate
    #
    #
    # Private - integrate - allocate
    #

    def _integrate_allocate_node(self, arg_key, arg_node, arg_node_parent, arg_bool_apply_changes_to_node_children=True):
        """
        IMPORTANT_FOR_BUILDING_TREE
        Typically called by...
        append_key()
        append_path()

        This method integrates a new node into the data tree.

        All methods which add nodes should call this method to integrate them.
        """
        if self is self._node_root:
            #
            # Raise an error if attempting to add a node already part of another tree
            #
            if not arg_node._node_parent == None:

                self._raise_error_because_node_child_is_still_part_of_another_tree(
                    arg_node)
            #
            # Continue with allocating node
            #
            #
            # Add arg_node to children
            #
            arg_node_parent._dict_of_keys_and_node_children[arg_key] = arg_node
            #
            # Set _node_parent and _node_root
            #
            arg_node._integrate_set_node_parent(arg_node_parent)
            #
            # Update children
            #
            if arg_bool_apply_changes_to_node_children:

                if arg_node._dict_of_keys_and_node_children:

                    self._integrate_allocate_node_children(arg_node)

        else:

            self._node_root._integrate_allocate_node(arg_key=arg_key,
                                                     arg_node=arg_node,
                                                     arg_node_parent=arg_node_parent,
                                                     arg_bool_apply_changes_to_node_children=arg_bool_apply_changes_to_node_children, )

    def _integrate_allocate_node_children(self, arg_node):
        """
        IMPORTANT_FOR_BUILDING_TREE
        Typically called by _integrate_allocate_node()

        This method is a wrapper for _integrate_update_node_children().

        Since this class is fairly simple, it doesn't need to distinguish between
        _integrate_allocate_node_children() and _integrate_deallocate_node_children().

        For more complex classes, this isn't / won't be the case, so these
        methods are here as wrappers until overridden.
        """
        self._integrate_update_node_children(arg_node)
    #
    # Private - integrate - deallocate
    #

    def _integrate_deallocate_node(self, arg_key, arg_node, arg_bool_apply_changes_to_node_children=True):
        """
        IMPORTANT_FOR_BUILDING_TREE
        Typically called by all 'delete' and 'pop' methods.

        This method breaks all internal connections between a node and its host data tree.

        All methods which remove nodes should call this method.
        """
        if self is self._node_root:

            try:

                del arg_node._node_parent._dict_of_keys_and_node_children[arg_key]

            except KeyError:

                self.print_object(arg_object=arg_node._node_parent._dict_of_keys_and_node_children,
                                  arg_name_for_object="arg_node._node_parent._dict_of_keys_and_node_children", )

                self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_key,
                                                             arg_node_start=arg_node._node_parent, )

            arg_node._integrate_set_node_parent(None)
            #
            # Update children
            #
            if arg_bool_apply_changes_to_node_children:

                if arg_node._dict_of_keys_and_node_children:

                    self._integrate_deallocate_node_children(arg_node)

        else:

            self._node_root._integrate_deallocate_node(arg_key=arg_key,
                                                       arg_node=arg_node,
                                                       arg_bool_apply_changes_to_node_children=arg_bool_apply_changes_to_node_children, )

    def _integrate_deallocate_node_children(self, arg_node):
        """
        IMPORTANT_FOR_BUILDING_TREE
        Typically called by _integrate_deallocate_node()

        This method is a wrapper for _integrate_update_node_children().

        Since this class is fairly simple, it doesn't need to distinguish between
        _integrate_allocate_node_children() and _integrate_deallocate_node_children().

        For more complex classes, this isn't / won't be the case, so these
        methods are here as wrappers until overridden.
        """
        self._integrate_update_node_children(arg_node)

    def _integrate_set_node_parent(self, arg_node_parent):
        """
        IMPORTANT_FOR_BUILDING_TREE

        Typically called by _integrate_allocate_node() and _integrate_deallocate_node()

        The method consolidates some of the generic overhead to minimize redundant
        code, during inheritance.
        """
        self._node_parent = arg_node_parent

        if arg_node_parent == None:

            self._node_root = self

        else:

            self._node_root = arg_node_parent._node_root

    def _integrate_update_node_children(self, arg_node):
        """
        Typically called by _integrate_deallocate_node_children() and _integrate_allocate_node_children()

        This method goes through arg_node's sub-tree and updates all the nodes.
        """
        _node_root = arg_node._node_root

        if arg_node._dict_of_keys_and_node_children:

            _stack_to_process_nodes = deque([arg_node])

            while _stack_to_process_nodes:

                item_node = _stack_to_process_nodes.pop()

                for item_node_child in item_node._dict_of_keys_and_node_children.values():
                    #
                    # Prep next iteration
                    #
                    _stack_to_process_nodes.append(item_node_child)
                    #
                    # Set node root
                    #
                    item_node_child._node_root = _node_root
    #
    # Private - print
    #

    def _print_info_get_list_of_strings_formatted(self, arg_object):
        """
        This method returns a formatted string which displays in a friendlier format
        than pprint's default approach.

        This is exclusively a support method for print_object(). This is why it returns
        a string, but doesn't start with "get" in its attribute name.
        """
        _string = self._pprint.pformat(arg_object)

        _list = _string.split("\n")

        _list_new = []

        item_index = 0

        while item_index < len(_list):

            if item_index >= len(_list):

                break

            item_string_current = _list[item_index]

            item_string_current_with_no_leading_or_trailing_white_space = item_string_current.strip()

            if item_string_current_with_no_leading_or_trailing_white_space:

                for item_character in _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END:

                    item_sub_string_to_use_as_replacement = "".join(
                        [", ", item_character, ])

                    item_string_current = item_string_current.replace(
                        item_character, item_sub_string_to_use_as_replacement, )
                #
                # Handle ':' for dicts
                #
                # if ": " in item_string_current : item_string_current = " : ".join( item_string_current.split( ": " ) )
                #
                # Handle spacing between lines
                #
                if item_string_current.endswith(","):

                    if item_string_current[-2] in _SET_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END:

                        item_string_current = "".join(
                            [item_string_current, "\n", ])

                elif item_string_current.endswith(" '") or item_string_current.endswith(" \""):

                    item_index_next = item_index + 1

                    while (item_string_current.endswith(" '") or item_string_current.endswith(" \"")) and item_index_next < len(_list):

                                                         # Current
                        item_string_current = "".join([item_string_current.rstrip()[: -1],

                                                       # Next
                                                       _list[item_index_next].lstrip()[1:], ])

                        if item_string_current[-1] in _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END:

                            item_string_current = "".join(
                                [item_string_current[: -1], ", ", item_string_current[-1], ])

                        _list.pop(item_index_next)

            _list_new.append(item_string_current)

            item_index += 1

        return _list_new

    def _print_node(self, arg_node, arg_path, arg_list_of_names_for_attributes_to_print=None):
        """
        This method prints arg_node's information.

        arg_node is the node we want to see the information for.

        arg_path is the path to arg_node within the data tree.

        arg_names_for_attributes_to_print - This can be None, a single string attribute name,
        or a list of attribute names. If this argument is None, then only the path to the node prints.
        If this contains attribute names, then the method will attempt to print the name and the attribute's
        value.

        If the method fails to find a specific attribute, it will raise an exception and detail
        which attribute name failed and what attributes the node contains.
        """
        print("--- PATH:", arg_path if arg_path else "(root)", "---\n", )

        if not arg_list_of_names_for_attributes_to_print == None:

            try:

                _list_of_pairs_names_for_attributes_and_values_to_print = [[item_name_for_attribute, getattr(arg_node, item_name_for_attribute, ), ]
                                                                           for item_name_for_attribute in arg_list_of_names_for_attributes_to_print]

                for item_name_for_attribute, item_value in _list_of_pairs_names_for_attributes_and_values_to_print:

                    print(item_name_for_attribute, "=", item_value, )

            except AttributeError:

                self._raise_error_because_attribute_does_not_exist_in_node(arg_node=arg_node,
                                                                           arg_list_of_names_for_attributes=arg_list_of_names_for_attributes_to_print, )

        if arg_list_of_names_for_attributes_to_print:

            print("\n")
    #
    # Private - raise
    #

    def _raise_error(self):
        """
        Reduces the chances of terminal output inter-mingling with exception info.

        Since this method should only run when raising an exception, the artificial delay
        isn't an issue during proper library execution.
        """
        time.sleep(0.5)

        raise ()

    def _raise_error_because_arg_data_is_an_invalid_format(self, arg_data):
        """
        This method provides additional context if this library can't handle the data supplied to
        setup_tree_based_on_data_structure()
        """
        print("Error: arg_data is an invalid format.\n")

        print("Supported data formats and result ( format : bool )")

        print("Dict / nested dict:", isinstance(arg_data, dict, ), "\n", )

        _bool_is_list_of_dicts = isinstance(arg_data, list, )

        if _bool_is_list_of_dicts:

            _bool_is_list_of_dicts = isinstance(arg_data[0], dict, )

        print("List of dicts:", _bool_is_list_of_dicts, "\n", )

        self.print_object(arg_object=arg_data,
                          arg_name_for_object="arg_data", )

        self._raise_error()

    def _raise_error_because_attempt_to_add_dict_item_triggered_type_error(self, arg_path, arg_node, arg_dict, arg_value_returned_by_formatter, arg_error_message):
        """
        Prints out an info dump if something goes wrong with attempting to add a return value to the returned dict in
        get_dict_of_string_paths_and_node_children()

        Since arg_callable_formatter can be a bit of a wild card, its better to have more info than just the standard
        error message.
        """
        print("Error: TypeError occurred.\n")

        print("arg_error_message =", arg_error_message, "\n", )

        print("arg_path =", arg_path, "\n", )

        print("type( arg_path ) =", arg_path, "\n", )

        print("arg_node =", arg_node, "\n", )

        if hasattr(arg_node, "get_object_stored_in_node", ):

            print("arg_node.get_object_stored_in_node() =",
                  arg_node.get_object_stored_in_node(), "\n", )

        else:

            print("type( arg_node ) =", type(arg_node), "\n", )

            print("Has attribute: get_object_stored_in_node? =", hasattr(
                arg_node, "get_object_stored_in_node", ), "\n", )

        print("arg_value_returned_by_formatter =",
              arg_value_returned_by_formatter, "\n", )

        print("type( arg_value_returned_by_formatter ) =",
              type(arg_value_returned_by_formatter), "\n", )

        if hasattr(arg_value_returned_by_formatter, "__getitem__", ):

            print("Is value at index 0, hashable?", isinstance(
                arg_value_returned_by_formatter[0], Hashable, ), "\n", )

        if hasattr(arg_value_returned_by_formatter, "__len__", ):

            print("len( arg_value_returned_by_formatter ) =",
                  len(arg_value_returned_by_formatter), "\n", )

            print("Is arg_value_returned_by_formatter a pair of two items?", len(
                arg_value_returned_by_formatter) == 2, "\n", )

        else:

            print(
                "Warning: arg_value_returned_by_formatter is not an an object with a size.\n")

        self.print_object(arg_object=arg_dict,
                          arg_name_for_object="arg_dict", )

        self._raise_error()

    def _raise_error_because_attribute_does_not_exist_in_node(self, arg_node, arg_list_of_names_for_attributes):
        """
        This method provides additional info if an attribute lookup fails for a node.
        """
        print("Error: attribute does not exist in node.\n")

        print("arg_node =", arg_node, "\n", )

        print("List of names and whether or not name exists in node ( 'name : bool, is present?' ):\n")

        for item_name_for_attribute in sorted(arg_list_of_names_for_attributes):

            print(item_name_for_attribute, ":", hasattr(
                arg_node, item_name_for_attribute, ), )

        self.print_object(arg_object=sorted(dir(arg_node)),
                          arg_name_for_object="List of names for existing attributes in node", )

        print("\n")

        self._raise_error()

    def _raise_error_because_bool_get_paths_as_strings_and_callable_formatter_collide(self, arg_bool_get_paths_as_strings, arg_callable_formatter):

        print("Error: Argument collision detected. arg_bool_get_paths_as_strings is True and arg_callable_formatter is not None.\n")

        print("arg_bool_get_paths_as_strings =",
              arg_bool_get_paths_as_strings, "\n", )

        print("arg_callable_formatter =", arg_callable_formatter, "\n", )

        print("Note: If you want the paths returned as strings and custom formatting, leave arg_bool_get_paths_as_strings = False and \n",
              "include self.get_string_path_from_arguments( arg_path ) in your callable.\n")

        print(
            "Example: _lambda : lambda arg_path, arg_node : [ self.get_string_path_from_arguments( arg_path ), custom_formatting_method( arg_node ) ]\n\n")

        self._raise_error()

    def _raise_error_because_key_or_path_failed(self, arg_key_or_path, arg_node_start):
        """
        This provides supplemental information in cases when a key or path lookup fails.
        """
        print("Error: arg_key_or_path failed.\n")

        print("arg_key_or_path =", arg_key_or_path, "\n", )

        print("type( arg_key_or_path ) =", type(arg_key_or_path), "\n", )

        _list_of_path_parts_present = []

        _list_of_path_parts_missing = []

        _list_of_path_parts = self.get_list_of_keys_from_path(arg_key_or_path)

        item_node = arg_node_start

        _node_for_data_discrepancy_analysis = None

        for item_path_part in _list_of_path_parts:

            if item_path_part in item_node._dict_of_keys_and_node_children.keys():

                _list_of_path_parts_present.append(item_path_part)

                item_node = item_node._dict_of_keys_and_node_children[item_path_part]

            else:

                _list_of_path_parts_missing = _list_of_path_parts[len(
                    _list_of_path_parts_present):]

                for item_key in item_node._dict_of_keys_and_node_children.keys():

                    if str(item_path_part) == str(item_key):

                        _node_for_data_discrepancy_analysis = item_node

                        break

                break

        self.print_object(arg_object=_list_of_path_parts_present,
                          arg_name_for_object="Path parts present in tree", )

        self.print_object(arg_object=_list_of_path_parts_missing,
                          arg_name_for_object="Path parts missing from tree", )

        if not _node_for_data_discrepancy_analysis == None:

            _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected = []

            item_node = _node_for_data_discrepancy_analysis

            for item_path_part_missing in _list_of_path_parts_missing:

                for item_key, item_node_child in item_node._dict_of_keys_and_node_children.items():

                    if str(item_path_part_missing) == str(item_key):

                        _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected.append(
                            [item_path_part_missing, True, ])

                        item_node = item_node_child

            print(
                "List of pairs, path_parts : ( bool ) if they failed due to data type discrepancy...\n")

            for item_pair in _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected:

                print(item_pair[0], ":", item_pair[1], )

        self._raise_error()

    def _raise_error_because_method_needs_defined(self):

        print("Error: Calling method which needs defined.\n")

        print("Name for method:", self._get_name_for_host_method(
            arg_int_depth=2), "\n", )

        self._raise_error()

    def _raise_error_because_node_child_is_not_in_tree(self, arg_node_child, arg_node_root):
        """
        This method raises an exception when arg_node_child is not found within arg_node_root's tree.
        """
        print("Error: arg_node is not in this data tree.\n")

        print("arg_node_child =", arg_node_child, "\n", )

        _list_of_pairs_paths_and_nodes = arg_node_root.get_list_of_pairs_paths_and_node_children()

        def _lambda_sort_key_for_pairs(arg_pair): return arg_pair[0]

        _list_of_pairs_paths_and_nodes = sorted(_list_of_pairs_paths_and_nodes,
                                                key=_lambda_sort_key_for_pairs, )

        print("--Tree Debugging Info ( node id : True / False node is arg_node : path to node )--\n", )

        for item_path, item_node in _list_of_pairs_paths_and_nodes:

            print(item_node._id_for_node if hasattr(item_node, "_id_for_node", ) else id(item_node),
                  ":", item_node is arg_node_child,
                  ":", item_path, )

        self._raise_error()

    def _raise_error_because_node_child_is_still_part_of_another_tree(self, arg_node_child):
        """
        Raises an exception because arg_node_child is already part of another tree.

        Specifically: when the child's _node_parent value is not None.
        """
        print("Error: arg_node is still part of another tree. Pop it from its previous tree before proceeding.\n")

        print("id( arg_node_child ) =", arg_node_child, "\n", )

        print("arg_node_child._node_parent =",
              arg_node_child._node_parent, "\n", )

        print("arg_node_child._node_root.get_path_to_node_child( arg_node_child ) =",
              arg_node_child._node_root.get_path_to_node_child(arg_node_child), "\n", )

        self._raise_error()
    #
    # Private - setup
    #
    # Reminder: Ignore any warnings in this method. Since self.data isn't defined in pure Python, this triggers
    # a false positive.

    def __init__(self, **kwargs):
        """
        IMPORTANT_FOR_BUILDING_TREE

        NOTE: kwargs no longer auto-populates the data structure like it did in the native dict class.
        Instead, use "arg_data" for initial populating.

        kwargs supports the following optional arguments:

        arg_string_delimiter_for_path - This is the only way to change self._string_delimiter_for_path's value.
        This value can only be set at initialization.

        arg_type_to_use_for_node_children - This changes the type used for new node children created within
        this create. This value can only be set at initialization.

        arg_data - Adding this triggers self.setup_tree_based_on_data_structure()

        The following arguments are also honored if arg_data is present:
        arg_keys_for_categorizing_nodes
        arg_bool_search_entire_tree

        Note: Review setup_tree_based_on_data_structure's docstring for detailed information.
        """
        self._BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS = True
        #
        # Attributes which can initialize before __init__
        #
        self._id_for_node = id(self)

        # This is an internal reference to PrettyPrint
        self._pprint = _PPRINT

        # This stores the parent node which links to this node, if relevant.
        self._node_parent = None

        # By default, all nodes begin as 'root' nodes until they become a child within a tree.
        self._node_root = self

        # This is a universal container for whatever the node should store.
        self._object_stored_in_node = None

        self._string_delimiter_for_path = self._STRING_DELIMITER_FOR_PATH_DEFAULT

        # This exists for faster compares when determining whether or not to pass self._string_delimiter_for_path as
        # an initial argument to any internally-created new nodes.
        self._bool_string_delimiter_for_path_is_default = True

        # This is the default node type for any new node instances created in this class.
        # Declaring it this way always ensures the default class is the same as the node
        # instancing it.
        self._type_to_use_for_node_children = self.__class__
        #
        # Reminder: Passing objects to this initializer activates dict's default key and values formatting. Instead, this functionality is now handled through "arg_data"
        #
        super().__init__()
        #
        # Attributes which require __init__ to run first
        #
        # Reminder: This assignment takes place mainly for the inheriting classes.
        # The ide provides a false-positive about self.data being undefined. It makes sense to
        # make this small assignment here, where the class is simplest, and only have the false
        # positive show up in this module.
        self._dict_of_keys_and_node_children = self.data

        # This list tracks any attributes which should call clear() when this class calls clear().
        self._list_of_attributes_to_clear = [
            self._dict_of_keys_and_node_children]
        #
        # Any kwarg configurations
        #
        if kwargs:

            if "arg_string_delimiter_for_path" in kwargs.keys():

                _string_original_value = self._string_delimiter_for_path

                self._string_delimiter_for_path = kwargs["arg_string_delimiter_for_path"]

                self._bool_string_delimiter_for_path_is_default = self._string_delimiter_for_path == _string_original_value

            if "arg_type_to_use_for_node_children" in kwargs.keys():

                self._type_to_use_for_node_children = kwargs["arg_type_to_use_for_node_children"]

            if "arg_data" in kwargs.keys():

                # Reminder: The arguments are explicitly here for clarity.
                self.setup_tree_based_on_data_structure(arg_data=kwargs["arg_data"],
                                                        arg_keys_for_categorizing_nodes=kwargs.get(
                                                            "arg_keys_for_categorizing_nodes", None, ),
                                                        arg_bool_search_entire_tree=kwargs.get("arg_bool_search_entire_tree", False, ), )
    #
    # Class variables and class methods
    #
    # Note: These are in all caps and meant to change as little as possible.
    #
    # This variable becomes True upon the first ever instance in
    _BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS = False

    _BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT = True

    # Sets the class variable to the module global value for _STRING_DELIMITER_FOR_PATH_DEFAULT
    _STRING_DELIMITER_FOR_PATH_DEFAULT = _STRING_DELIMITER_FOR_PATH_DEFAULT

    @classmethod
    def set_string_delimiter_for_path_default_for_all_classes(cls, arg_string_delimiter_for_path_default, **kwargs):
        """
        This method sets the global default delimiter for Data_tree_node and all inheriting classes.

        CAUTION: This method should only really run before any nodes exists.

        It will raise errors if used after first node created, or ran a 2nd time. These errors
        can be overridden in the arguments by setting either of these arguments to True:

        -arg_bool_override_safety_against_multiple_assignments
        -arg_bool_override_safety_against_setting_global_value_after_first_node_creation
        """
        if not kwargs.get("arg_bool_override_safety_against_setting_global_value_after_first_node_creation", False, ):

            if cls._BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS:

                print(
                    "Error: Attempting to set the string delimiter for all paths after at least one node instance exists.\n")

                print("To avoid this error, do one of the following:")
                print(
                    "-Call set_string_delimiter_for_path_default_for_all_classes() before initializing any nodes.")
                print("-Set arg_bool_override_safety_against_setting_global_value_after_first_node_creation to True ( WARNING: DOES NOT UPDATE DELIMITERS FOR EXISTING PATHS! )\n")

                time.sleep(0.5)

                raise ()

        if not kwargs.get("arg_bool_override_safety_against_multiple_assignments", False, ):

            if not cls._BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT:

                print(
                    "Error: cls._STRING_DELIMITER_FOR_PATH_DEFAULT already set to non-default value.\n")

                print(
                    "If you intended to do this, set arg_bool_override_safety_against_multiple_assignments to True.\n")

                time.sleep(0.5)

                raise ()

        cls._STRING_DELIMITER_FOR_PATH_DEFAULT = arg_string_delimiter_for_path_default

        cls._BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT = False


"""
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
"""
