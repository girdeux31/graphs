
import sys
import os
from inspect import stack

python_version = float(str(sys.version_info[0]) + '.' + str(sys.version_info[1]))


def error(msg, id=None):
    """
    PURPOSE:

     Terminate the program nicely and show the stack table

    MANDATORY ARGUMENTS:

     Parameter   Type                 Definition
     =========== ==================== ==========================================================================================
     logger                           Object returned by start_logger()
     msg         str                  Error message to show through screen

    OPTIONAL ARGUMENTS:

     Parameter   Type                 Default        Definition
     =========== ==================== ============== ===========================================================================
     id          int/None             None           Error ID
    """
    # Write info
    print('')
    print(msg)
    print('')
    print('Traceback is shown, first is the deepest call')
    print('')

    # Write stack table
    print('    {:20s} {:6s} {:20s}'.format('File', 'Line', 'Function'))
    print('    ' + '=' * 20 + ' ' + '=' * 6 + ' ' + '=' * 30)

    for i in range(1, len(stack())):

        if python_version <= 3.4:
            filename = os.path.basename(stack()[i][1])
            lineno = stack()[i][2]
            function = stack()[i][3]
        else:
            filename = os.path.basename(stack()[i].filename)
            lineno = stack()[i].lineno
            function = stack()[i].function

        print('{:3d} {:20s} {:6d} {:20s}'.format(i, filename, lineno, function))

        if function == 'execfile' or function == '<module>':
            break

    print('')

    if id:
        raise Exception('Fatal error ' + str(id))
    else:
        raise Exception('Fatal error')


def warning(msg, id=None):
    """
    PURPOSE:

     Show nice warning

    MANDATORY ARGUMENTS:

     Parameter   Type                 Definition
     =========== ==================== ==========================================================================================
     msg         str                  Warning message to show through screen

    OPTIONAL ARGUMENTS:

     Parameter   Type                 Default        Definition
     =========== ==================== ============== ===========================================================================
     id          int/None             None           Warning ID
    """
    # Get names
    if python_version <= 3.4:
        filename = os.path.basename(stack()[1][1])
        lineno = stack()[1][2]
        function = stack()[1][3]
    else:
        filename = os.path.basename(stack()[1].filename)
        lineno = stack()[1].lineno
        function = stack()[1].function

    # Write info
    print('')
    if id:
        print('Warning (' + str(id) + ') in ' + filename + '::' + function + ', line ' + str(lineno))
    else:
        print('Warning in ' + filename + '::' + function + ', line ' + str(lineno))

    print(msg)
    print('')


def type_checker(*types, **dict_types):
    """
    PURPOSE:

     Decorator definition to check types and number of input arguments

    MANDATORY ARGUMENTS:

     Parameter   Type                 Definition
     =========== ==================== ==========================================================================================
     types       list of types        Types of required input arguments, use tuple for multiple options
     dict_types  dict                 Types of optional input arguments, use tuple for multiple options
    """
    # print('types', types)
    # print('dict_types', dict_types)
    # types are the required arguments in decorator
    # dict_types are the optional arguments in decorator
    def check_types(f):
        # f is the object the decorator is decorating
        is_module = f.__code__.co_varnames[0] == 'self'  # True if decorator is applied to module
        # f.__code__.co_argcount is the total input arguments in f definition (not the call of f)
        arg_obj_def = f.__code__.co_argcount - 1 if is_module else f.__code__.co_argcount  # number of arguments in object definition
        arg_dec_usage = len(types) + len(dict_types)  # number of arguments in decorator usage

        # check that number of arguments in decorator usage matches the number arguments in object definition
        if arg_dec_usage == arg_obj_def:

            def new_f(*args, **kwds):
                # print('args', args)
                # print('kwds', kwds)
                # args are the required arguments of object call
                # kwds are the optional arguments of object call
                org_args = args  # keep copy of original arguments
                args = args[1:] if is_module else args  # remove self object for modules

                # check number of required arguments in object call
                if len(args) != len(types):
                    error('Number of required input arguments is {:d}, but {:d} are found'.format(len(types), len(args)))

                # check required input argument types
                for (arg, typ) in zip(args, types):

                    if not isinstance(arg, typ):

                        # make typ a tuple
                        typ = typ if isinstance(typ, tuple) else (typ,)  # don't use tuple(typ)

                        error('Input argument \'{:s}\' is of type {:s}, but must be {:s}'.format(
                               str(arg),
                               type(arg).__name__,
                               ' or '.join([t.__name__ for t in typ])
                              ))

                # check optional input argument types
                for (key, arg) in kwds.items():

                    # check that optional input argument is in object definition
                    if key not in dict_types:
                        error('Unknown optional input argument \'{:s}\''.format(key))

                    typ = dict_types[key]

                    if not isinstance(arg, typ):

                        # make typ a tuple
                        typ = typ if isinstance(typ, tuple) else (typ,)  # don't use tuple(typ)

                        error('Optional input argument \'{:s} = {:s}\' is of type {:s}, but must be {:s}'.format(
                               key,
                               str(arg),
                               type(arg).__name__,
                               ' or '.join([t.__name__ for t in typ])
                              ))

                return f(*org_args, **kwds)

            new_f.__name__ = f.__name__
            return new_f

        else:
            error('Object definition has {:d} arguments, but {:d} are found in decorator usage'.format(
                   arg_obj_def, arg_dec_usage))

    return check_types