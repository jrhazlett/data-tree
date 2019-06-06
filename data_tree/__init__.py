''''''
#
# Libraries - native
#
import warnings
#
# Libraries - custom
#
# This suppresses a deprecation warning:
# DeprecationWarning: Deprecated since Python 3.4. Use importlib.util.find_spec() instead.
# This warning is related to setuptools, and its a known python issue.
with warnings.catch_warnings():

    warnings.simplefilter("ignore", category=DeprecationWarning, )

    # Here for convenience
    from .src.data_tree_node import Data_tree_node

    # Here because its necessary
    from .src.data_tree_node_with_quick_lookup import Data_tree_node_with_quick_lookup
