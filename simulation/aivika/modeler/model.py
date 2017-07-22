# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class InvalidVariableException(Exception):
    """Raised when the variable is invalid."""

    def __init__(self, name, message):
        """Initializes a new instance."""
        self.name = name
        self.message = message

class Model:
    """It represents the simulation model."""
    pass

class MainModel(Model):
    """It represents the main simulation model."""

    def __init__(self, base_comp = None):
        """Initializes a new simulation model."""
        self._base_comp = base_comp
        self._package_imports = set()
        self._module_imports = set()
        self._actions = []
        self._sources = []
        self._var_names = set()
        self._lazy_var_names = set()

    def get_main_model(self):
        """Return the main model."""
        return self

    def get_base_comp(self):
        """Return the basic computation type."""
        return self._base_comp

    def get_var_prefix(self):
        """Return the variable prefix."""
        return ''

    def add_package_import(self, package):
        """Add the specified package to import."""
        self._package_imports.add(package)

    def add_module_import(self, module):
        """Add the specified module to import."""
        self._module_imports.add(module)

    def add_var(self, name, comp):
        """Add a new variable with the specified definition."""
        if name in self._var_names:
            raise InvalidVariableException(name,
                'Variable ' + name + ' is already defined')
        elif name in self._lazy_var_names:
            action = name + ' <- ' + comp
            self._lazy_var_names.remove(name)
            self._var_names.add(name)
            self.add_action(action)
        else:
            action = name + ' <- ' + comp
            self._var_names.add(name)
            self.add_action(action)

    def add_lazy_var(self, name):
        """Add a new variable that will be defined lazily."""
        if name in self._var_names:
            raise InvalidVariableException(name,
                'Variable ' + name + ' is already defined')
        elif name in self._lazy_var_names:
            raise InvalidVariableException(name,
                'Variable ' + name + ' is already added as lazy')
        else:
            self._lazy_var_names.add(name)

    def add_action(self, action):
        """Add the specified action."""
        self._actions.append(action)

    def add_result_source(self, source):
        """Add the specified result source."""
        self._sources.append(source)

    def generate_code(self, indent = ''):
        """Generate the code for this model."""
        if len(self._lazy_var_names) > 0:
            for name in self._lazy_var_names:
                raise InvalidVariableException(name,
                    'Variable ' + name + ' is used but not defined')
        else:
            code = indent + 'mdo { \n'
            indent2 = indent + '  '
            for action in self._actions:
                code += indent2 + action + ';\n'
            code += indent2 + 'return $\n'
            code += indent2 + '  results\n'
            code += self._get_sources(indent2 + '  ') + '\n'
            code += indent + '}'
            return code

    def _get_sources(self, indent):
        """Get the result source list."""
        code = indent + '['
        first = True
        for source in self._sources:
            if first:
                first = False
                code += source
            else:
                code += ',\n' + indent + ' ' + source
        code += ']'
        return code

class SubModel(Model):
    """It represents a sub-model."""

    _next_id = 1

    def __init__(self, model):
        """Initializes a new sub-model."""
        self._main_model = model.get_main_model()
        self._model = model
        self._var_prefix = '__comp_' + str(SubModel._next_id) + '_'
        SubModel._next_id += 1

    def get_main_model(self):
        """Return the main model."""
        return self._main_model

    def get_parent_model(self):
        """Return the parent model."""
        return self._model

    def get_base_comp(self):
        """Get the basic computation type."""
        return self._main_model.get_base_comp()

    def get_var_prefix(self):
        """Return the variable prefix."""
        return self._var_prefix

    def add_package_import(self, package):
        """Add the specified package to import."""
        self._main_model.add_package_import(package)

    def add_module_import(self, module):
        """Add the specified module to import."""
        self._main_model.add_module_import(module)

    def add_var(self, name, comp):
        """Add a new variable with the specified definition."""
        self._main_model.add_var(name, comp)

    def add_lazy_var(self, name):
        """Add a new variable that will be defined lazily."""
        self._main_model.add_lazy_var(name)

    def add_action(self, action):
        """Add the specified action."""
        self._main_model.add_action(action)

    def add_result_source(self, source):
        """Add the specified result source."""
        self._main_model.add_result_source(source)
