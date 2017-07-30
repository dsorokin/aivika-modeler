# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

import os

cabal_file_template = """
name:                modeling-project
version:             0.1.0.0
synopsis:            Simulation Model
description:         Generated by Aivika Modeler
homepage:            https://github.com/githubuser/modeling-project#readme
license:             AllRightsReserved
license-file:        LICENSE.txt
author:              Author name here
maintainer:          example@example.com
copyright:           2017 Author name here
category:            Simulation
build-type:          Simple
extra-source-files:  README.md
cabal-version:       >=1.10

library
  hs-source-dirs:      src
  exposed-modules:     Lib
  build-depends:       base >= 4.7 && < 5
  default-language:    Haskell2010

executable modeling-project-exe
  hs-source-dirs:      app
  main-is:             Main.hs
  ghc-options:         -threaded -O2 -rtsopts -with-rtsopts=-N
  build-depends:       base
                     , modeling-project
{packages_to_import}
  default-language:    Haskell2010

source-repository head
  type:     git
  location: https://github.com/githubuser/modeling-project

"""

license_text = """Copyright Author name here (c) 2017

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of Author name here nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

readme_text = """Simulation model

"""

setup_code = """import Distribution.Simple
main = defaultMain

"""

lib_code = """module Lib where

"""

stack_file_template = """# This file was automatically generated by 'stack init'
#
# Some commonly used options have been documented as comments in this file.
# For advanced use and comprehensive documentation of the format, please see:
# http://docs.haskellstack.org/en/stable/yaml_configuration/

# Resolver to choose a 'specific' stackage snapshot or a compiler version.
# A snapshot resolver dictates the compiler version and the set of packages
# to be used for project dependencies. For example:
#
# resolver: lts-3.5
# resolver: nightly-2015-09-21
# resolver: ghc-7.10.2
# resolver: ghcjs-0.1.0_ghc-7.10.2
# resolver:
#  name: custom-snapshot
#  location: "./custom-snapshot.yaml"
resolver: lts-8.13

# User packages to be built.
# Various formats can be used as shown in the example below.
#
# packages:
# - some-directory
# - https://example.com/foo/bar/baz-0.0.2.tar.gz
# - location:
#    git: https://github.com/commercialhaskell/stack.git
#    commit: e7b331f14bcffb8367cd58fbfc8b40ec7642100a
# - location: https://github.com/commercialhaskell/stack/commit/e7b331f14bcffb8367cd58fbfc8b40ec7642100a
#   extra-dep: true
#  subdirs:
#  - auto-update
#  - wai
#
# A package marked 'extra-dep: true' will only be built if demanded by a
# non-dependency (i.e. a user package), and its test suites and benchmarks
# will not be run. This is useful for tweaking upstream packages.
packages:
{package_locations}
- '.'
# Dependency packages to be pulled from upstream that are not in the resolver
# (e.g., acme-missiles-0.3)
extra-deps:
{extra_deps}

# Override default flag values for local packages and extra-deps
flags: {}

# Extra package databases containing global packages
extra-package-dbs: []

# Control whether we use the GHC we find on the path
# system-ghc: true
#
# Require a specific version of stack, using version ranges
# require-stack-version: -any # Default
# require-stack-version: ">=1.3"
#
# Override the architecture used by stack, especially useful on Windows
# arch: i386
# arch: x86_64
#
# Extra directories used by stack for building
# extra-include-dirs: [/path/to/dir]
# extra-lib-dirs: [/path/to/dir]
#
# Allow a newer minor version of GHC than the snapshot specifies
# compiler-check: newer-minor

"""

def generate_cabal_file_impl(model, filename):
    """Generate a cabal file."""
    with open(filename, "w") as file:
        write_cabal_file_impl(model, file)

def generate_license_file_impl(filename):
    """Generate the LICENSE file."""
    with open(filename, "w") as file:
        write_license_file_impl(file)

def generate_readme_file_impl(filename):
    """Generate the README.md file."""
    with open(filename, "w") as file:
        write_readme_file_impl(file)

def generate_setup_file_impl(filename):
    """Generate the Setup.hs file."""
    with open(filename, "w") as file:
        write_setup_file_impl(file)

def generate_lib_file_impl(filename):
    """Generate the library file."""
    with open(filename, "w") as file:
        write_lib_file_impl(file)

def generate_stack_file_impl(model, filename):
    """Generate a stack file."""
    with open(filename, "w") as file:
        write_stack_file_impl(model, file)

def write_cabal_file_impl(model, file):
    """Write the cabal file."""
    indent = '                     , '
    lines = '\n'.join(map(lambda x: indent + x, model._package_imports))
    contents = cabal_file_template
    contents = contents.replace('{packages_to_import}', lines)
    file.write(contents)

def write_license_file_impl(file):
    """Write the license file."""
    file.write(license_text)

def write_readme_file_impl(file):
    """Write the README.md file."""
    file.write(readme_text)

def write_setup_file_impl(file):
    """Write the Setup.hs file."""
    file.write(setup_code)

def write_lib_file_impl(file):
    """Write the library file."""
    file.write(lib_code)

def write_stack_file_impl(model, file):
    """Write the stack file."""
    indent = '- '
    def get_location(location):
        return '- location:\n   ' + location + '\n  extra-dep: true'
    def get_locations(locations):
        return '\n'.join(map(get_location, locations))
    def get_extra_deps(extra_deps):
        return '\n'.join(map(lambda x: '- ' + x, extra_deps))
    contents = stack_file_template
    contents = contents.replace('{package_locations}', get_locations(model._package_locations))
    contents = contents.replace('{extra_deps}', get_extra_deps(model._extra_deps))
    file.write(contents)
