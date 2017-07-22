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
        self._pragmas = set()
        self._package_imports = set()
        self._module_imports = set()
        self._actions = []
        self._sources = []
        self._var_names = set()
        self._lazy_var_names = set()
        if base_comp is None:
            self._pragmas.add('{-# LANGUAGE RecursiveDo #-}')
            self._package_imports.add('aivika')
            self._module_imports.add('import Simulation.Aivika')
        else:
            self._pragmas.add('{-# LANGUAGE RecursiveDo #-}')
            self._package_imports.add('aivika-transformers')
            self._module_imports.add('import Simulation.Aivika.Trans')

    def get_main_model(self):
        """Return the main model."""
        return self

    def get_base_comp(self):
        """Return the basic computation type."""
        return self._base_comp

    def get_var_prefix(self):
        """Return the variable prefix."""
        return ''

    def add_pragma(self, pragma):
        """Add the specified pragma."""
        self._pragmas.add(pragma)

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

    def require_complete(self):
        """Require the model to be complete."""
        if len(self._lazy_var_names) > 0:
            for name in self._lazy_var_names:
                raise InvalidVariableException(name,
                    'Variable ' + name + ' is used but not defined')

    def write(self, file):
        """Write the model file."""
        self.require_complete()
        for pragma in self._pragmas:
            file.write(pragma)
            file.write('\n')
        if len(self._pragmas) > 0:
            file.write('\n')
        file.write('-- NOTE: This file was auto-generated by aivika-modeler 1.0\n')
        file.write('\n')
        file.write('module Model(model) where\n')
        file.write('\n')
        for module_import in self._module_imports:
            file.write(module_import)
            file.write('\n')
        if len(self._module_imports) > 0:
            file.write('\n')
        self._write_model(file)
        file.write('\n')

    def _write_model(self, file):
        """Write the model definition in the file."""
        file.write('model =')
        file.write('\n')
        self._write_code(file, '  ')

    def _write_code(self, file, indent = ''):
        """Write the code in the file."""
        file.write(indent)
        file.write('mdo --')
        file.write('\n')
        indent2 = indent + '    '
        for action in self._actions:
            file.write(indent2)
            file.write(action)
            file.write('\n')
        file.write(indent2)
        file.write('return $\n')
        file.write(indent2)
        file.write('  results\n')
        self._write_sources(file, indent2 + '  ')
        file.write('\n')

    def _write_sources(self, file, indent):
        """Write the result source list in file."""
        file.write(indent)
        file.write('[')
        first = True
        for source in self._sources:
            if first:
                first = False
                file.write(source)
            else:
                file.write(',\n')
                file.write(indent)
                file.write(' ')
                file.write(source)
        file.write(']')

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

    def add_pragma(self, pragma):
        """Add the specified pragma."""
        self._main_model.add_pragma(pragma)

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
