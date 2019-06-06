#!python
#cython: language_level=3
""""""
#
# Libraries - native
#
import os
import sys
#
# Libraries - native - collections
#
# Used for node traversals
from collections import deque
#
# Libraries - native - typing
#
# <any notated types go here>
#
#
# Libraries - custom
#
# Best of both worlds...
# This attempts one import strategy, and switches to the other if it fails
try:

    # Reminder: This approach works when running module from shell / virtual environment, but fails during compile
    from .data_tree_node import Data_tree_node

except:

    # Reminder: This approach works for compiling, but fails when running module from shell / virtual environment
    sys.path.append(os.path.dirname(__file__))

    from data_tree_node import Data_tree_node
#
# Config
#
_SET_OF_TYPES_WHICH_ARE_IMMUTABLE = {
    bool, bytes, complex, float, frozenset, int, tuple, }
#
# Class
#


class Data_tree_node_with_quick_lookup(Data_tree_node):
    """
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
    """
    #
    # Public
    #
    #
    # Public - clear
    #

    def clear(self, **kwargs):
        """
        This method does two types of clearing...

        -Reset of the node (standard)
        -Clear only the dicts used for pathing

        Arguments:

        arg_bool_only_dicts_for_pathing - If True, this only clears the dicts for pathing. This is called by
        self._integrate_set_node_parent()
        """
        if kwargs.get("arg_bool_only_dicts_for_pathing", False, ):

            for item_dict_for_pathing in self._list_of_dicts_for_pathing:

                item_dict_for_pathing.clear()
        #
        # Standard clear
        #
        else:
            #
            # Reminder:
            #
            # -Sets self._object_stored_in_node = None
            # -All objects in self._list_of_attributes_to_clear; for this class, it includes all pathing dicts
            #
            super().clear()
    #
    # Public - delete
    #

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

        In cases where the entire tree is involved, this method does a dict key lookup rather than traverse the
        nodes directly.
        """
        if self is self._node_root and arg_bool_search_sub_tree:

            _path = self.get_path_to_node_child(arg_node_child=arg_node_child)

            if _path == None:

                self._raise_error_because_node_child_is_not_in_tree(arg_node_child=arg_node_child,
                                                                    arg_node_root=self._node_root, )

            else:

                self._integrate_deallocate_node(arg_node=arg_node_child,
                                                arg_key=_path[-1], )

        elif arg_bool_search_entire_tree:

            self._node_root.delete_node_child(arg_node_child=arg_node_child,
                                              arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                              arg_bool_search_sub_tree=arg_bool_search_sub_tree, )

        else:

            super().delete_node_child(arg_node_child=arg_node_child,
                                      arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                      arg_bool_search_sub_tree=arg_bool_search_sub_tree, )

    def delete_path_to_node_child(self, arg_path, arg_bool_path_is_absolute=False):
        """
        This method breaks all internal references to the node located at the path. This does not affect the other nodes along the path.

        This raises an exception if the path is not found.

        This method does not return a value.

        Arguments:

        arg_path - can be either a list of keys, or a delimited string.

        arg_bool_path_is_absolute - If True, then the root node's

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _node = None

            try:

                _node = self._dict_of_paths_and_nodes[self.get_tuple_of_keys_from_path(
                    arg_path)]

            except:

                self._raise_error_because_key_or_path_failed(arg_key_or_path=arg_path,
                                                             arg_node_start=self._node_root, )

            self._integrate_deallocate_node(arg_key=self._get_key_that_is_last_in_path(arg_path),
                                            arg_node=_node, )

        elif arg_bool_path_is_absolute:

            self._node_root.delete_path_to_node_child(arg_path=arg_path,
                                                      arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            super().delete_path_to_node_child(arg_path=arg_path,
                                              arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
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

        arg_default_value_to_return - The value returned of the path does not exist.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _path = self.get_tuple_of_keys_from_path(arg_path)

            if _path in self._dict_of_paths_and_nodes.keys():

                _node = self._dict_of_paths_and_nodes[_path]

                if _node._dict_of_keys_and_node_children:

                    return _node

                else:

                    return _node._object_stored_in_node

            else:

                return arg_default_value_to_return

        elif arg_bool_search_entire_tree:

            return self._node_root.get(arg_path=arg_path,
                                       arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                       arg_default_value_to_return=arg_default_value_to_return, )

        else:

            return super().get(arg_path=arg_path,
                               arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                               arg_default_value_to_return=arg_default_value_to_return, )
    #
    # Public - get - dict
    #

    def get_dict_of_paths_and_node_children(self, arg_bool_search_sub_tree=True, arg_bool_search_entire_tree=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
        Returns a dict, with paths as keys and nodes as values.

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:
            #
            # Returns a copy, to keep the same behavior as the parent class
            #
            if arg_callable_filter:
                #
                # arg_callable_filter - yes, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    _dict_to_return = {}

                    for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items():

                        if arg_callable_filter(item_path_child, item_node_child, ):

                            item_value_to_return = arg_callable_formatter(
                                item_path_child, item_node_child, )

                            try:

                                _dict_to_return.__setitem__(
                                    *item_value_to_return)

                            except (TypeError, ValueError, ) as _error_message:

                                self._raise_error_because_attempt_to_add_dict_item_triggered_type_error(arg_path=item_path_child,
                                                                                                        arg_node=item_node_child,
                                                                                                        arg_dict=_dict_to_return,
                                                                                                        arg_value_returned_by_formatter=item_value_to_return,
                                                                                                        arg_error_message=_error_message, )

                    return _dict_to_return
                #
                # arg_callable_filter - yes, arg_callable_formatter - no
                #
                else:

                    return {item_path_child: item_node_child for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()
                            if arg_callable_filter(self.get_list_of_keys_from_path(item_path_child), item_node_child, )}

            else:
                #
                # arg_callable_filter - no, arg_callable_formatter - yes
                #
                if arg_callable_formatter:

                    _dict_to_return = {}

                    for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items():

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
                #
                # arg_callable_filter - no, arg_callable_formatter - no
                #
                else:

                    return {item_path: item_node for item_path, item_node in self._dict_of_paths_and_nodes.items()}

        elif arg_bool_search_entire_tree:

            return self._node_root.get_dict_of_paths_and_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                       arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                                       arg_callable_filter=arg_callable_filter,
                                                                       arg_callable_formatter=arg_callable_formatter, )

        else:

            return super().get_dict_of_paths_and_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                               arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                               arg_callable_filter=arg_callable_filter,
                                                               arg_callable_formatter=arg_callable_formatter, )
    #
    # Public - get - id
    #

    def get_id_for_object_stored_in_node(self, arg_object):
        """
        RECOMMENDED_FOR_CUSTOM_OVERRIDES

        WARNING: EXPERIMENTAL

        WARNING: The ids generated by this method's default and alternative definitions are
        purely theoretical based on research. It's recommended users change this definition
        based on their needs and the demands of their chosen interpreter.

        Method explanation:

        Data_tree_node_with_quick_lookup calls this method whenever it interacts with
        self._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids

        This method's intent is to return a hashable unique key to use in a dict regardless of arg_object's data type.

        Notes specific to this particular definition...

        This is a simple approach designed to provide both consistent and unique keys.

        This method causes the tree to track immutable objects by value, and mutable objects by instance id. This 'default'
        approach is meant to be a compromise between mutable and immutable objects.

        Notes:

        -*Should* work in Python interpreters which create more than one instance of the same immutable. Although this isn't the
        case with CPython, other interpreters reportedly do create multiple instances.

        -Faster, takes up less memory, and more explicitly tries to avoid collisions than some of the alternatives considered

        -Avoids potential collisions between mutable instance ids and integers

        Explored alternatives:

        -Use id() for all objects
        Pros: Fast
        Cons: Difficult to predict if non-CPython interpreters keep ids constant for immutable values

        -Incorporate blake2b
        Pros: Similar returned value types in all use cases
        Cons: Need way to address collisions; Not as efficient as alternatives; Seemed unnecessarily redundant since
        returned value is meant to be used as a dict key
        """
        return arg_object if type(arg_object) in _SET_OF_TYPES_WHICH_ARE_IMMUTABLE else ("MUTABLE_OBJECT", id(arg_object), )
    #
    # Public - get - int
    #

    def get_int_count_for_node_children(self, arg_bool_search_sub_tree=False, arg_bool_search_entire_tree=False, arg_callable_filter=None, arg_callable_formatter=None):
        """
        Returns the number of nodes in the tree.

        This does not count the root node of either search type.

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Note: a True value for this parameter supersedes arg_bool_search_sub_tree's value

        arg_bool_search_sub_tree - If True, searches sub tree. If False, searches only immediate node children.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.

        arg_callable_filter - This method interprets the returned value of this callable as True / False.

        arg_callable_formatter - This method returns an int value, which is added to the total count returned by
        get_int_count_for_node_children()
        """
        if self == self._node_root:

            if arg_callable_filter:

                if arg_callable_formatter:

                    return sum([arg_callable_formatter(item_node) for item_node in self._dict_of_paths_and_nodes.values() if arg_callable_filter(item_node)])

                else:

                    return len([item_node for item_node in self._dict_of_paths_and_nodes.values() if arg_callable_filter(item_node)])

            else:

                if arg_callable_formatter:

                    return sum([arg_callable_formatter(item_node) for item_node in self._dict_of_paths_and_nodes.values()])

                else:

                    return len(self._dict_of_paths_and_nodes)

        elif arg_bool_search_entire_tree:

            return self._node_root.get_int_count_for_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                   arg_bool_search_entire_tree=arg_bool_search_entire_tree, )

        else:

            return super().get_int_count_for_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                           arg_bool_search_entire_tree=arg_bool_search_entire_tree, )
    #
    # Public - get - list
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

        Node: all paths are in list format when the current method calls the argument.

        Example of a valid lambda:

        # Returns False unless the path only contains one key
        _example_lambda = lambda arg_path, arg_node : len( arg_path ) == 1
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

            if self is self._node_root:

                if arg_callable_filter:
                    #
                    # arg_callable_filter - yes, arg_callable_formatter - yes
                    #
                    if arg_callable_formatter:

                        return [arg_callable_formatter(item_path_child, item_node_child, ) for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items() if arg_callable_filter(item_path_child, item_node_child, )]
                    #
                    # arg_callable_filter - yes, arg_callable_formatter - no
                    #
                    else:

                        return [[list(item_path_child), item_node_child, ] for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items() if arg_callable_filter(item_path_child, item_node_child, )]

                else:
                    #
                    # arg_callable_filter - no, arg_callable_formatter - yes
                    #
                    if arg_callable_formatter:

                        return [arg_callable_formatter(item_path_child, item_node_child, ) for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()]
                    #
                    # arg_callable_filter - no, arg_callable_formatter - no
                    #
                    else:

                        return [[list(item_path_child), item_node_child, ] for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()]

            elif arg_bool_search_entire_tree:

                return self._node_root.get_list_of_pairs_paths_and_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                                 arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                                                 arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                 arg_callable_filter=arg_callable_filter, )
        #
        # If none of the above triggers, run the parent method
        #
        return super().get_list_of_pairs_paths_and_node_children(arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                 arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                                 arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                 arg_callable_filter=arg_callable_filter, )

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

        Node: all paths are in list format when the current method calls the argument.

        Example of a valid lambda:

        # Returns False unless the path only contains one key
        _example_lambda = lambda arg_path, arg_node : len( arg_path ) == 1
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

            if self is self._node_root:

                if arg_callable_filter:

                    if arg_callable_formatter:

                        return [arg_callable_formatter(item_path_child, item_node_child, )
                                for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()
                                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ) and arg_callable_filter(item_path_child, item_node_child, )]

                    else:

                        return [[list(item_path_child), item_node_child, ]
                                for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()
                                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, ) and arg_callable_filter(item_path_child, item_node_child, )]

                else:

                    if arg_callable_formatter:

                        return [arg_callable_formatter(item_path_child, item_node_child, )
                                for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()
                                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, )]

                    else:

                        return [[list(item_path_child), item_node_child, ]
                                for item_path_child, item_node_child in self._dict_of_paths_and_nodes.items()
                                if self.logic_objects_match(item_node_child._object_stored_in_node, arg_object, )]

            elif arg_bool_search_entire_tree:

                return self._node_root.get_list_of_pairs_paths_and_node_children_relevant_to_object(arg_object=arg_object,
                                                                                                    arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                                                    arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                                                                    arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                                    arg_callable_filter=arg_callable_filter, )
            #
            # If none of the above triggers, run the parent method
            #
            return super().get_list_of_pairs_paths_and_node_children_relevant_to_object(arg_object=arg_object,
                                                                                        arg_bool_search_sub_tree=arg_bool_search_sub_tree,
                                                                                        arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                                                        arg_bool_get_paths_as_strings=arg_bool_get_paths_as_strings,
                                                                                        arg_callable_filter=arg_callable_filter, )
    #
    # Public - get - node
    #

    def get_node_child_at_path(self, arg_path, arg_default_value_to_return=None, arg_bool_path_is_absolute=False):
        """
        Returns the node located at arg_path.

        If the path doesn’t exist in the tree, then the method will return arg_default_value_to_return.

        If arg_bool_path_is_absolute is False, then the method assumes the path starts with a key use by one of
        the calling node’s children. If its True, then the method starts with the root node.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _path = self.get_tuple_of_keys_from_path(arg_path)

            if _path in self._node_root._dict_of_paths_and_nodes.keys():

                return self._node_root._dict_of_paths_and_nodes[_path]

            else:

                return arg_default_value_to_return

        elif arg_bool_path_is_absolute:

            return self._node_root.get_node_child_at_path(arg_path=arg_path,
                                                          arg_default_value_to_return=arg_default_value_to_return,
                                                          arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            return super().get_node_child_at_path(arg_path=arg_path,
                                                  arg_default_value_to_return=arg_default_value_to_return,
                                                  arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Public - get - object
    #

    def get_object_at_path(self, arg_path, arg_default_value_to_return=None, arg_bool_path_is_absolute=False):
        """
        Returns the object stored within the node located at the path.

        If the path does not exist, then the method will return arg_default_value_to_return.

        If arg_bool_path_is_absolute is False, then the method assumes arg_path begins
        with a key to one of the calling node’s children. If True, then the method starts with the root node.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _path = self.get_tuple_of_keys_from_path(arg_path)

            if _path in self._dict_of_paths_and_nodes.keys():

                return self._dict_of_paths_and_nodes[_path]._object_stored_in_node

            else:

                return arg_default_value_to_return

        elif arg_bool_path_is_absolute:

            return self._node_root.get_object_at_path(arg_path=arg_path,
                                                      arg_default_value_to_return=arg_default_value_to_return,
                                                      arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            return super().get_object_at_path(arg_path=arg_path,
                                              arg_default_value_to_return=arg_default_value_to_return,
                                              arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Public - get - path
    #

    def get_path_to_node_child(self, arg_node_child, arg_bool_search_entire_tree=False, arg_bool_raise_error_if_node_is_not_in_tree=True, arg_default_value_to_return=None, arg_bool_get_path_as_string=False):
        """
        Returns a list of keys in the path to the node by default, since not all tree instances are guaranteed to have exclusively strings as keys.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        If arg_bool_raise_error_if_node_is_not_in_tree is True, then the method will raise an exception if its unable to find the node.

        arg_default_value_to_return is the value returned if arg_bool_raise_error_if_node_is_not_in_tree is False.

        Note: If arg_bool_raise_error_if_node_is_not_in_tree is True, then arg_default_value_to_return will not be honored.

        Setting arg_bool_get_path_as_string to True, returns a delimited string instead of a list.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            if arg_bool_raise_error_if_node_is_not_in_tree:

                try:

                    _path = self._dict_of_nodes_and_paths[arg_node_child._id_for_node]

                except KeyError:

                    self._raise_error_because_node_child_is_not_in_tree(arg_node_child=arg_node_child._id_for_node,
                                                                        arg_node_root=self._node_root, )

                    # Here to quiet the IDE. The above method calls raise() and accounts for the needed wait time to avoid
                    # error text inter-mingling with other text.
                    raise()

                return self._string_delimiter_for_path.join([str(item_path_part) for item_path_part in _path]) if arg_bool_get_path_as_string else list(_path)

            else:

                _id_for_node = arg_node_child._id_for_node

                if not _id_for_node in self._dict_of_nodes_and_paths.keys():

                    return arg_default_value_to_return

                else:

                    _path = self._dict_of_nodes_and_paths[_id_for_node]

                    return self._string_delimiter_for_path.join([str(item_path_part) for item_path_part in _path]) if arg_bool_get_path_as_string else list(_path)

        elif arg_bool_search_entire_tree:

            return self._node_root.get_path_to_node_child(arg_node_child=arg_node_child,
                                                          arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                          arg_bool_raise_error_if_node_is_not_in_tree=arg_bool_raise_error_if_node_is_not_in_tree,
                                                          arg_default_value_to_return=arg_default_value_to_return,
                                                          arg_bool_get_path_as_string=arg_bool_get_path_as_string, )

        else:

            return super().get_path_to_node_child(arg_node_child=arg_node_child,
                                                  arg_bool_get_path_as_string=arg_bool_get_path_as_string,
                                                  arg_bool_search_entire_tree=arg_bool_search_entire_tree,
                                                  arg_bool_raise_error_if_node_is_not_in_tree=arg_bool_raise_error_if_node_is_not_in_tree,
                                                  arg_default_value_to_return=arg_default_value_to_return, )
    #
    # Public - logic
    #

    def logic_path_exists(self, arg_path, arg_bool_path_is_absolute=False):
        """
        Returns True, if the path exists within the tree, and False if not.

        Arguments:

        arg_path - Can be a delimited string or list of keys.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            return self.get_tuple_of_keys_from_path(arg_path) in self._dict_of_paths_and_nodes.keys()

        elif arg_bool_path_is_absolute:

            return self._node_root.logic_path_exists(arg_path=arg_path,
                                                     arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            return super().logic_path_exists(arg_path=arg_path,
                                             arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

    def logic_path_is_leaf_node(self, arg_path, arg_bool_path_is_absolute=False):
        """
        Returns True, if the path exists in the tree, and the node at the path has no children.

        Arguments:

        arg_path - This can be a delimited string, or a list of keys.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _tuple_path = self.get_tuple_of_keys_from_path(arg_path)

            if _tuple_path in self._dict_of_paths_and_nodes.keys():

                return not self._dict_of_paths_and_nodes[_tuple_path]._dict_of_keys_and_node_children

            else:

                return False

        elif arg_bool_path_is_absolute:

            return self._node_root.logic_path_is_leaf_node(arg_path=arg_path,
                                                           arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            return super().logic_path_is_leaf_node(arg_path=arg_path,
                                                   arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Public - pop
    #

    def pop_node_child(self, arg_node_child, arg_default_value_to_return=None, arg_bool_search_entire_tree=False):
        """
        Returns the path to the node; and removes the node. If arg_node doesn’t exist, returns arg_default_value_to_return.

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        Rational behind returning the path:

        If the dev is using the node object, then they already have access to the object stored
        within the node. The info that isn't necessarily easy to come by is what gets returned, which in this case would be the path.

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _id_for_node = arg_node_child._id_for_node

            if _id_for_node in self._dict_of_nodes_and_paths.keys():

                _path = self._dict_of_nodes_and_paths[_id_for_node]

                self._integrate_deallocate_node(arg_key=_path[-1],
                                                arg_node=arg_node_child, )

                return _path

            else:

                return arg_default_value_to_return

        elif arg_bool_search_entire_tree:

            return self._node_root.pop_node_child(arg_node_child=arg_node_child,
                                                  arg_default_value_to_return=arg_default_value_to_return,
                                                  arg_bool_search_entire_tree=arg_bool_search_entire_tree, )

        else:

            return super().pop_node_child(arg_node_child=arg_node_child,
                                          arg_default_value_to_return=arg_default_value_to_return,
                                          arg_bool_search_entire_tree=False, )

    def pop_path_to_node_child(self, arg_path, arg_default_value_to_return=None, arg_bool_path_is_absolute=False):
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

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        if self is self._node_root:

            _path = self.get_tuple_of_keys_from_path(arg_path)

            if _path in self._dict_of_paths_and_nodes.keys():

                _node = self._dict_of_paths_and_nodes[_path]

                self._integrate_deallocate_node(arg_key=self._get_key_that_is_last_in_path(_path),
                                                arg_node=_node, )

                return _node

            else:

                return arg_default_value_to_return

        if arg_bool_path_is_absolute:

            return self.pop_path_to_node_child(arg_path=arg_path,
                                               arg_default_value_to_return=arg_default_value_to_return,
                                               arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

        else:

            return super().pop_path_to_node_child(arg_path=arg_path,
                                                  arg_default_value_to_return=arg_default_value_to_return,
                                                  arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Public - print
    #

    def print_pathing_dicts(self):
        """
        Prints the pathing dicts to output.

        Notes:
            Taking the getattr() approach is more resilient against changes. This method should only
            really be used for debugging anyways, so speed really shouldn't be a concern.
        """
        _list_of_names_for_dicts_in_node_root = [item_name_for_attribute
                                                 for item_name_for_attribute in dir(self._node_root)
                                                 if item_name_for_attribute.startswith("_dict_")]

        for item_name_for_attribute_dict in _list_of_names_for_dicts_in_node_root:

            item_dict = getattr(
                self._node_root, item_name_for_attribute_dict, )

            if not item_dict is self._node_root._dict_of_keys_and_node_children:

                self.print_object(arg_object=item_dict,
                                  arg_name_for_object="".join(["self._node_root.", item_name_for_attribute_dict, ]), )
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

        If current node is the root for the tree, then path is referenced by dict key. If the
        current node isn't the root node, but the boolean statement for checking the whole tree
        is True, then this method is called in the root node.

        If all of the above is False, then call the parent class' method.
        """
        #
        # If there's no specified path, assign the object to our host node
        #
        if arg_path == None:

            if self is self._node_root:

                self._object_stored_in_node = arg_object

            else:

                self._integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(arg_node=self,
                                                                                                                                              arg_node_root=self._node_root, )

                self._object_stored_in_node = arg_object

                self._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                    arg_node=self)

            return self

        else:

            if self is self._node_root:
                #
                # If there's a specified path, then process it...
                #
                #
                # Make sure the path is in a usable format
                #
                _path = self.get_tuple_of_keys_from_path(arg_path)
                #
                # If the path is already present, then set the object within the node at that path.
                #
                if _path in self._dict_of_paths_and_nodes.keys():

                    _node = self._dict_of_paths_and_nodes[_path]

                    self._integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(arg_node=_node,
                                                                                                                                                  arg_node_root=self._node_root, )

                    _node._object_stored_in_node = arg_object

                    self._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                        arg_node=_node)

                    return _node
                #
                # If the path does not already exist, then trace through the nodes and fill in the blanks.
                #
                else:

                    _node = self.get_node_child_at_path(arg_path)

                    self._integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(arg_node=_node,
                                                                                                                                                  arg_node_root=self._node_root, )

                    _node._object_stored_in_node = arg_object

                    self._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                        arg_node=_node)

                    return _node

            elif arg_bool_path_is_absolute:

                return self._node_root.set_object_stored_in_node(arg_object=arg_object,
                                                                 arg_path=arg_path,
                                                                 arg_bool_path_is_absolute=arg_bool_path_is_absolute, )

            else:

                return super().set_object_stored_in_node(arg_object=arg_object,
                                                         arg_path=arg_path,
                                                         arg_bool_path_is_absolute=arg_bool_path_is_absolute, )
    #
    # Private
    #
    #
    # Private - integrate
    #
    #
    # Private - integrate - allocate
    #

    def _integrate_allocate_node(self, arg_key, arg_node, arg_node_parent, arg_bool_apply_changes_to_node_children=True):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method integrates arg_node in arg_node_parent's tree

        In addition to root and parent connections, this also adds arg_node's data to:
        - _dict_of_nodes_and_paths
        - _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
        - _dict_of_paths_and_nodes
        """
        if self is self._node_root:
            #
            # Add arg_node as a child to the current node
            #
            # Reminder: This calls arg_node._integrate_set_node_parent()
            super()._integrate_allocate_node(arg_key=arg_key,
                                             arg_node=arg_node,
                                             arg_node_parent=arg_node_parent,
                                             arg_bool_apply_changes_to_node_children=False, )
            #
            # If arg_node_parent is _node_root, then the path to arg_node should be a key. If this isn't the case, then the path
            # should be absolute.
            #
            _list_path_to_arg_node = [arg_key] if arg_node_parent is arg_node_parent._node_root else [
                *self._dict_of_nodes_and_paths[arg_node_parent._id_for_node], arg_key, ]
            #
            # Update _dict_of_nodes_and_paths
            #
            self._dict_of_nodes_and_paths[arg_node._id_for_node] = _list_path_to_arg_node
            #
            # Update _dict_of_paths_and_nodes
            #
            self._dict_of_paths_and_nodes[self.get_tuple_of_keys_from_path(
                _list_path_to_arg_node)] = arg_node
            #
            # Update paths for children
            #
            if arg_bool_apply_changes_to_node_children:

                self._integrate_allocate_node_children(arg_node=arg_node)
            #
            # Update _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
            #
            self._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                arg_node)
        #
        # If the current node isn't root, then call root's _integrate_allocate_node
        #
        else:

            self._node_root._integrate_allocate_node(arg_key=arg_key,
                                                     arg_node=arg_node,
                                                     arg_node_parent=arg_node_parent,
                                                     arg_bool_apply_changes_to_node_children=arg_bool_apply_changes_to_node_children, )

    def _integrate_allocate_node_children(self, arg_node):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method checks if contained children, and if so, migrates its pathing data to the
        root node of its new tree.

        This assumes 'self._node_root' is already the new root node. This way, the method behaves
        more like a 'sync.'
        """
        #
        # If arg_node has children, then allocate them to root node's paths
        #
        if arg_node._dict_of_keys_and_node_children:

            _node_root = self._node_root

            _path_to_node = self._node_root._dict_of_nodes_and_paths[arg_node._id_for_node]
            #
            # Store _node_root's pathing dicts locally for easy referencing
            #
            _dict_of_nodes_and_paths = _node_root._dict_of_nodes_and_paths

            _dict_of_paths_and_nodes = _node_root._dict_of_paths_and_nodes
            #
            # Cycle through each child node and add them to root's pathing
            #
            _stack_to_process_pairs_paths_and_nodes = deque(
                [[_path_to_node, arg_node, ]])

            while _stack_to_process_pairs_paths_and_nodes:

                item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

                for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                    item_node_child._node_root = _node_root

                    item_path_child = [*item_path, item_key_child, ]
                    #
                    # Prep next iteration
                    #
                    _stack_to_process_pairs_paths_and_nodes.append(
                        [item_path_child, item_node_child, ])
                    #
                    # Update _dict_of_nodes_and_paths
                    #
                    _dict_of_nodes_and_paths[item_node_child._id_for_node] = item_path_child
                    #
                    # Update _dict_of_paths_and_nodes
                    #
                    _dict_of_paths_and_nodes[tuple(
                        item_path_child)] = item_node_child
                    #
                    # Update _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
                    #
                    self._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                        item_node_child)

    def _integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(self, arg_node):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method adds the id for the object to self._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids.

        _get_id_for_object_stored_in_tree assigns a unique and consistent key for the value

        The method then stores the node at the generated key.

        Note: This activity occurs enough in the code to justify its own method.

        Called by:
        - _integrate_allocate_node
        - _integrate_allocate_node_children
        - set_object_stored_in_node
        """
        if hasattr(self._node_root, "_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids", ):

            _key_for_object_stored_in_node = self.get_id_for_object_stored_in_node(
                arg_node._object_stored_in_node)
            #
            # Append key to self._node_root._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
            #
            _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids = self._node_root._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
            #
            # If the key doesn't already exist, create a new list at that location
            #
            if not _key_for_object_stored_in_node in _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids.keys():

                _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[_key_for_object_stored_in_node] = [
                    arg_node]
            #
            # If the key already exists, then append arg_node to its list
            #
            else:

                _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[_key_for_object_stored_in_node].append(
                    arg_node)
    #
    # Private - integrate - deallocate
    #

    def _integrate_deallocate_node(self, arg_key, arg_node, arg_bool_apply_changes_to_node_children=True):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method removes arg_node in arg_node_parent's tree

        In addition to root and parent connections, this also adds arg_node's data to:
        - _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
        - _dict_of_nodes_and_paths
        - _dict_of_paths_and_nodes
        """
        if self is self._node_root:
            #
            # Abort if arg_node is None
            #
            if arg_node == None:

                return
            #
            # Continue with deallocation
            #
            #
            # Scan through the paths and nodes
            # Find which ones have the path to arg_node as a prefix
            # - Add them to the lists for removal
            # - Migrate them to arg_node's dicts, since its now root node for its respective tree
            #
            if arg_bool_apply_changes_to_node_children:

                if arg_node._dict_of_keys_and_node_children:

                    self._integrate_deallocate_node_children(arg_node=arg_node)
            #
            # Break the link between arg_node and its node parent
            #
            _node_root_prev = arg_node._node_root
            #
            # Deallocate children first
            #
            # Reminder: This calls arg_node._set_parent()
            super()._integrate_deallocate_node(arg_key=arg_key,
                                               arg_node=arg_node,
                                               arg_bool_apply_changes_to_node_children=False, )
            #
            # Update _dict_of_nodes_and_paths
            #
            _list_path_to_arg_node = _node_root_prev._dict_of_nodes_and_paths.pop(
                arg_node._id_for_node)
            #
            # Update _dict_of_paths_and_nodes
            #
            del _node_root_prev._dict_of_paths_and_nodes[self.get_tuple_of_keys_from_path(
                _list_path_to_arg_node)]
            #
            # Update _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
            #
            self._integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(arg_node=arg_node,
                                                                                                                                          arg_node_root=_node_root_prev, )
        #
        # If the current node isn't root, then call root's _integrate_deallocate_node
        #
        else:

            self._node_root._integrate_deallocate_node(arg_key=arg_key,
                                                       arg_node=arg_node,
                                                       arg_bool_apply_changes_to_node_children=arg_bool_apply_changes_to_node_children, )

    def _integrate_deallocate_node_children(self, arg_node):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method migrates child data from the root node to arg_node ahead of severing arg_node's connections to the host tree.
        """
        _node_root_new = arg_node
        #
        # Check for attributes in _node_root_new, and add what's possible
        #
        _bool_has_attribute_dict_of_nodes_and_paths = hasattr(
            _node_root_new, "_dict_of_nodes_and_paths", )

        _bool_has_attribute_dict_of_paths_and_nodes = hasattr(
            _node_root_new, "_dict_of_paths_and_nodes", )

        _bool_has_attribute_integrate_allocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids = hasattr(
            _node_root_new, "_integrate_allocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids", )
        #
        # Prep for updating the new root node
        #
        _node_root_prev = arg_node._node_root

        _list_path_to_arg_node = self.get_list_of_keys_from_path(
            _node_root_prev._dict_of_nodes_and_paths[arg_node._id_for_node])

        _int_length_of_path_to_node = len(_list_path_to_arg_node)

        _stack_to_process_nodes = deque([[_list_path_to_arg_node, arg_node, ]])
        #
        # Cycle through the nodes in arg_node's sub-tree and break the links between them and node root
        #
        while _stack_to_process_nodes:
            #
            # Reminder: This approach guarantees a one-time pass through all the children, between new / prev root nodes
            # Other approaches kept resulting in two passes. With small data sets, this isn't really an issue, but if someone
            # gets ambitious, I'd rather the tree have a shot at standing up to the challenge.
            #
            item_path, item_node = _stack_to_process_nodes.pop()

            for item_key_child, item_node_child in item_node._dict_of_keys_and_node_children.items():

                item_path_to_child_list = [*item_path, item_key_child, ]
                #
                # Prep next iteration
                #
                _stack_to_process_nodes.append(
                    [item_path_to_child_list, item_node_child, ])
                #
                # Add child to new tree
                #
                item_path_child_new_list = item_path_to_child_list[_int_length_of_path_to_node:]
                #
                # Add to _dict_of_nodes_and_paths
                #
                item_id_for_node_child = item_node_child._id_for_node

                if _bool_has_attribute_dict_of_nodes_and_paths:

                    _node_root_new._dict_of_nodes_and_paths[item_id_for_node_child] = item_path_child_new_list
                #
                # Add to _dict_of_paths_and_nodes
                #
                if _bool_has_attribute_dict_of_paths_and_nodes:

                    _node_root_new._dict_of_paths_and_nodes[self.get_tuple_of_keys_from_path(
                        item_path_child_new_list)] = item_node_child
                #
                # Break links / paths between arg_node and node root
                #
                #
                # Break link _dict_of_nodes_and_paths
                #
                if item_id_for_node_child in _node_root_prev._dict_of_nodes_and_paths.keys():

                    del _node_root_prev._dict_of_nodes_and_paths[item_id_for_node_child]
                #
                # Break link _dict_of_paths_and_nodes
                #
                item_path_to_child_tuple = tuple(item_path_to_child_list)

                if item_path_to_child_tuple in _node_root_prev._dict_of_paths_and_nodes.keys():

                    del _node_root_prev._dict_of_paths_and_nodes[item_path_to_child_tuple]
                #
                # Remove the node from _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
                #
                self._integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(arg_node=item_node_child,
                                                                                                                                              arg_node_root=_node_root_prev, )
                #
                # Integrate item_node_child's object stored in node if possible
                #
                if _bool_has_attribute_integrate_allocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids:

                    _node_root_new._integrate_allocate_object_stored_in_node_to_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(
                        item_node_child)

    def _integrate_deallocate_object_stored_in_node_from_dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids(self, arg_node, arg_node_root):
        """
        IMPORTANT_FOR_BUILDING_TREE

        This method removes arg_node from the list of nodes stored at the id for the object stored within it.

        Steps:

        -Get id for object stored in node
        -Use id to fetch node from _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
        -Delete the index that list for arg_node

        Note: This activity occurs enough in the code to justify its own method.

        Called by:

        - _integrate_deallocate_node
        - _integrate_deallocate_node_children
        - set_object_stored_in_node
        """
        _key_for_object_stored_in_node = self.get_id_for_object_stored_in_node(
            arg_node._object_stored_in_node)
        #
        # Pop key in arg_node_root._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
        #
        # Reminder: Trees don't store root node's value in _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
        if not arg_node is arg_node_root:
            #
            # Store dict locally for easy referencing
            #
            _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids = arg_node_root._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids
            #
            # Get list of node's with the object in question
            #
            _list_of_nodes_with_objects = _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[
                _key_for_object_stored_in_node]
            #
            # Create a new list without arg_node
            #
            _list_of_nodes = [
                item_node_with_object for item_node_with_object in _list_of_nodes_with_objects if not item_node_with_object is arg_node]
            #
            # If the list still contains nodes, store it
            #
            if _list_of_nodes:

                _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[
                    _key_for_object_stored_in_node] = _list_of_nodes
            #
            # If the list is empty, delete the key in the dict
            #
            else:

                del _dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids[
                    _key_for_object_stored_in_node]
    #
    # Private - set
    #

    def _integrate_set_node_parent(self, arg_node_parent):
        """
        IMPORTANT_FOR_BUILDING_TREE

        Reminder: At least in this class' case, this method is called by
        super()._integrate_allocate_node() and super()._integrate_deallocate_node()
        """
        super()._integrate_set_node_parent(arg_node_parent)

        # Reminder: Left here as a visual reference
        # if arg_node_parent == None :

        # Normally pathing updates would go here, but that would result in
        # two tree traversals instead of one. Instead, the pathing data is updated
        # in _integrate_allocate_node_children().

        # else :
        if not arg_node_parent == None:

            self.clear(arg_bool_only_dicts_for_pathing=True)
    #
    # Private - setup
    #

    def __init__(self, **kwargs):
        """
        IMPORTANT_FOR_BUILDING_TREE
        """
        super().__init__(**kwargs)

        self._id_for_node = id(self)
        #
        # Each node containing a certain value other than None, is referenced here for quick searches
        #
        self._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids = {}

        self._dict_of_nodes_and_paths = {}

        self._dict_of_paths_and_nodes = {}
        #
        # Reminder: clear() iterates through this list and calls the items' respective clear() methods.
        #
        self._list_of_dicts_for_pathing = [self._dict_of_nodes_and_paths,
                                           self._dict_of_lists_for_objects_stored_in_nodes_and_list_of_relevant_node_ids,
                                           self._dict_of_paths_and_nodes, ]

        self._list_of_attributes_to_clear.extend(
            self._list_of_dicts_for_pathing)

        self._node_root = self


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
