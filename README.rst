Eventually
==========

Deprecation framework for Python.

To mark a method, function, or class as being deprecated do this::

    from incremental import Version
    from eventually import deprecated

    @deprecated(Version("MyProj", 8, 0, 0))
    def badAPI(self, first, second):
        '''
        Docstring for badAPI.
        '''
        ...

    @deprecated(Version("MyProj", 16, 0, 0))
    class BadClass(object):
        '''
        Docstring for BadClass.
        '''

The newly-decorated badAPI will issue a warning when called, and BadClass will
issue a warning when instantiated. Both will also have  a deprecation notice
appended to their docstring.

To deprecate properties you can use::

    from incremental import Version
    from eventually import deprecatedProperty

    class OtherwiseUndeprecatedClass(object):

        @deprecatedProperty(Version('MyProj', 16, 0, 0))
        def badProperty(self):
            '''
            Docstring for badProperty.
            '''

        @badProperty.setter
        def badProperty(self, value):
            '''
            Setter sill also raise the deprecation warning.
            '''


To mark module-level attributes as being deprecated you can use::

    badAttribute = "someValue"

    ...

    deprecatedModuleAttribute(
        Version("MyProj", 8, 0, 0),
        "Use goodAttribute instead.",
        "your.full.module.name",
        "badAttribute")

The deprecated attributes will issue a warning whenever they are accessed. If
the attributes being deprecated are in the same module as the
``deprecatedModuleAttribute`` call is being made from, the ``__name__`` global
can be used as the ``moduleName`` parameter.
