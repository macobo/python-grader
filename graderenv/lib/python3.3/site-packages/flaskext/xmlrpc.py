# -*- coding: utf-8 -*-
"""
flaskext.xmlrpc
===============

Adds support for creating XML-RPC APIs to Flask.

:copyright: (c) 2010 by Matthew "LeafStorm" Frazier.
:license: MIT, see LICENSE for more details.
"""

from flask import request, current_app
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher as Dispatcher
import sys
import xmlrpclib

Fault = xmlrpclib.Fault

class XMLRPCHandler(Dispatcher):
    """
    This is the basic XML-RPC handler class. To use it, you create it::
    
        handler = XMLRPCHandler('api')
    
    Then, you can register functions with the :meth:`register` method::
    
        @handler.register
        def spam():
            pass
    
    :meth:`register` is just an alias for :meth:`register_function`, so you
    can use that too.
    You can also register an instance using the :meth:`register_instance`
    method, and any methods on said instance will be exposed if they do not
    start with an ``_``.
    
    Then, you connect it to a :class:`~flask.Flask` instance or a Flask
    module with the :meth:`connect` method, like this::
    
        handler.connect(app, '/')
    
    :param endpoint_name: The name to use as an endpoint when connected to
                          an app or module. If not specified here, you specify
                          when you call :meth:`connect`.
    :param instance: The instance to register and expose the methods of.
    :param introspection: Whether to register the introspection functions,
                          like :obj:`system.listMethods`. (It will by
                          default.)
    :param multicall: Whether to register the :obj:`system.multicall`
                      function. (It won't by default.)
    """
    def __init__(self, endpoint_name=None, instance=None, introspection=True,
                 multicall=False):
        if sys.version_info[:2] < (2, 5):
            Dispatcher.__init__(self)
        else:
            Dispatcher.__init__(self, True, 'utf-8')
        self.endpoint_name = endpoint_name
        if introspection:
            self.register_introspection_functions()
        if multicall:
            self.register_multicall_functions()
        if instance:
            self.register_instance(instance)
    
    def register(self, *args, **kwargs):
        """
        An alias for :meth:`register_function`.
        """
        return self.register_function(*args, **kwargs)
    
    def register_function(self, function, name=None):
        """
        This will register the given function. There are two ways to use it.
        
        As a plain old method, with or without a name::
        
            handler.register_function(spam)
            handler.register_function(spam, 'spam')
        
        As a decorator, also with or without a name::
        
            @handler.register_function
            def spam():
                pass
            
            @handler.register_function('spam')
            def spam():
                pass
        
        It's shorter and easier to use :meth:`register`, however, as it does
        the exact same thing.
        
        :param function: The function to register. (In the named decorator
                         form, this is the function's name.)
        :param name: The name to use, except in the named decorator form.
                     If not given, the function's :obj:`__name__` attribute
                     will be used.
        """
        if isinstance(function, basestring):
            return lambda fn: self.register_function(fn, function)
        return Dispatcher.register_function(self, function, name)
    
    def register_instance(self, instance, allow_dotted_names=False):
        """
        This registers any kind of object. If the requested method hasn't been
        registered by :meth:`register_function`, it will be checked against
        the instance. You can only have one instance at a time, however.
        
        If :obj:`allow_dotted_names` is True, the name will be split on the
        dots and the object will be traveled down recursively. However, this
        is a **HUGE SECURITY LOOPHOLE**, as while private methods (starting
        with ``_``) will not be exposed, it's still possible that someone
        could get access to your globals and do very bad things. So don't
        do it unless you have a very good reason.
        
        :param instance: The instance to register.
        :param allow_dotted_names: Whether to resolve dots in method names.
                                   You probably shouldn't.
        """
        # Yes, it's just a wrapper. I know. This way the docs are consistent.
        Dispatcher.register_instance(self, instance, allow_dotted_names)
    
    def connect(self, app_module, route, endpoint_name=None):
        """
        Connects the handler to an app or module. You have to provide the
        app and the URL route to use. The route can't contain any variable
        parts, because there is no way to get them to the method. ::
        
            handler.connect(app, '/api')
        
        :param app_module: The app or module to connect the handler to.
        :param route: The URL route to use for the handler.
        :param endpoint_name: The name to use when connecting the endpoint.
        """
        if endpoint_name is None:
            endpoint_name = self.endpoint_name
            if endpoint_name is None:   # still
                raise RuntimeError("No endpoint name given!")
        app_module.add_url_rule(route, endpoint_name, self.handle_request,
                                methods=['POST'])
    
    def handle_request(self):
        """
        This is the actual request handler that is routed by :meth:`connect`.
        It takes the request data, dispatches the method, and sends it back
        to the client.
        """
        response_data = self._marshaled_dispatch(request.data)
        return current_app.response_class(response_data,
                                          content_type='text/xml')
    
    def namespace(self, prefix):
        """
        This returns a :class:`XMLRPCNamespace` object, which has
        :meth:`~XMLRPCNamespace.register` and
        :meth:`~XMLRPCNamespace.register_function` methods. These forward
        directly to the :meth:`register_function` method of the parent they
        were created from, but they will prepend the given prefix, plus a dot,
        to the name registered. For example::
        
            blog = handler.namespace('blog')
            
            @blog.register
            def new_post(whatever):
                pass
        
        would make :obj:`new_post` available as :obj:`blog.new_post`.
        
        :param prefix: The name to prefix the methods with.
        """
        return XMLRPCNamespace(self, prefix)


class XMLRPCNamespace(object):
    """
    This is a simple proxy that can register methods, and passes them on to
    the :class:`XMLRPCHandler` that created it with a given name added as a
    prefix (with a dot). For more nesting, you can create namespaces from
    namespaces with the :meth:`namespace` method.
    
    :parameter handler: The handler to pass the methods to.
    :parameter prefix: The prefix to give to the assigned methods. A dot will
                       be appended.
    """
    def __init__(self, handler, prefix):
        self.handler = handler
        self.prefix = prefix
    
    def register_function(self, function, name=None):
        """
        Registers a function. Use is the same as with the
        :meth:`XMLRPCHandler.register_function` method.
        
        :param function: The function to register. (In the named decorator
                         form, this is the function's name.)
        :param name: The name to use, except in the named decorator form.
                     If not given, the function's :obj:`__name__` attribute
                     will be used.
        """
        if isinstance(function, basestring):
            return lambda fn: self.register_function(fn, function)
        if name is None:
            name = function.__name__
        new_name = self.prefix + '.' + name
        self.handler.register_function(function, new_name)
    
    def register(self, *args, **kwargs):
        """
        An alias for :meth:`register_function`. As with
        :meth:`XMLRPCHandler.register`, it's shorter and easier to type.
        """
        return self.register_function(*args, **kwargs)
    
    def namespace(self, name):
        """
        Returns another namespace for the same handler, with the given name
        postfixed to the current namespace's prefix. For example, ::
        
            handler.namespace('foo').namespace('bar')
        
        gives the same result as::
        
            handler.namespace('foo.bar')
        
        :param prefix: The name to prefix the methods with.
        """
        return XMLRPCNamespace(self.handler, self.prefix + '.' + name)


def dump_method_call(method, *params):
    """
    This marshals the given method and parameters into a proper XML-RPC method
    call. It's very useful for testing.
    
    :param method: The name of the method to call.
    :param params: The parameters to pass to the method.
    """
    return xmlrpclib.dumps(params, methodname=method)


def load_method_response(response):
    """
    This returns the actual value returned from an XML-RPC response. If it's
    a :obj:`Fault` instance, it will return the fault instead of the value.
    This is also useful for testing.
    
    :param response: The marshaled XML-RPC method response or fault.
    """
    try:
        return xmlrpclib.loads(response)[0][0]
    except Fault, fault:
        return fault


def test_xmlrpc_call(client, rpc_path, method, *params):
    """
    This makes a method call using a Werkzeug :obj:`Client`, such as the one
    returned by :meth:`flask.Flask.test_client`. It constructs the method
    call, makes the request, and then returns the response value or a
    :obj:`Fault`.
    
    :param client: A :obj:`werkzeug.Client`.
    :param rpc_path: The path to the XML-RPC handler.
    :param method: The method to call.
    :param params: The parameters to pass to the method.
    """
    rv = client.post(
        rpc_path,
        data=dump_method_call(method, *params),
        content_type='text/xml'
    )
    return load_method_response(rv.data)
test_xmlrpc_call.__test__ = False   # prevents Nose from collecting it


class XMLRPCTester(object):
    """
    This lets you conveniently make method calls using a Werkzeug
    :obj:`Client`, like the one returned by :meth:`flask.Flask.test_client`.
    You create it with the :obj:`Client` and the path to the responder, and
    then you call it with the method and params.
    
    :param client: A :obj:`werkzeug.Client`.
    :param rpc_path: The path to the XML-RPC handler.
    """
    __test__ = False    # prevents Nose from collecting it
    
    def __init__(self, client, rpc_path):
        self.client = client
        self.rpc_path = rpc_path
    
    def call(self, method, *params):
        """
        This calls the client's :obj:`post` method with the responder path,
        the marshaled method call, and a content type of ``text/xml``. It will
        return the unmarshaled response or fault.
        
        You can just call the instance like a function for the same effect.
        These two calls are equivalent::
        
            tester.call('hello', 'world')
            tester('hello', 'world')
        
        :param method: The name of the method to call.
        :param params: The parameters to pass to the method.
        """
        return test_xmlrpc_call(self.client, self.rpc_path, method, *params)
    
    def __call__(self, method, *params):
        return self.call(method, *params)
