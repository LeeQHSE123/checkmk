#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Type definitions

Some of these are exposed in the API, some are not.
"""
from collections.abc import Mapping
from typing import (
    Any,
    Callable,
    Generator,
    List,
    MutableMapping,
    NamedTuple,
    Optional,
    Set,
    Union,
)
import pprint

from cmk.utils.type_defs import (
    ParsedSectionName,
    SectionName,
    SNMPDetectBaseType,
)
from cmk.snmplib.type_defs import SNMPTree  # pylint: disable=cmk-module-layer-violation

from cmk.base.discovered_labels import HostLabel  # pylint: disable=cmk-module-layer-violation


class Parameters(Mapping):
    """Parameter objects are used to pass parameters to plugin functions"""
    def __init__(self, data):
        if not isinstance(data, dict):
            self._data = data  # error handling will try to repr(self).
            raise TypeError("Parameters expected dict, got %r" % (data,))
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        # use pformat to be testable.
        return "%s(%s)" % (self.__class__.__name__, pprint.pformat(self._data))


StringTable = List[List[str]]
StringByteTable = List[List[Union[str, List[int]]]]

AgentParseFunction = Callable[[StringTable], Any]

HostLabelGenerator = Generator[HostLabel, None, None]
HostLabelFunction = Callable[..., HostLabelGenerator]

SNMPParseFunction = Union[  #
    Callable[[List[StringTable]], Any],  #
    Callable[[List[StringByteTable]], Any],  #
]

SimpleSNMPParseFunction = Union[  #
    Callable[[StringTable], Any],  #
    Callable[[StringByteTable], Any],  #
]

AgentSectionPlugin = NamedTuple(
    "AgentSectionPlugin",
    [
        ("name", SectionName),
        ("parsed_section_name", ParsedSectionName),
        ("parse_function", AgentParseFunction),
        ("host_label_function", HostLabelFunction),
        ("supersedes", Set[SectionName]),
        ("module", Optional[str]),  # not available for auto migrated plugins.
    ],
)

SNMPSectionPlugin = NamedTuple(
    "SNMPSectionPlugin",
    [
        ("name", SectionName),
        ("parsed_section_name", ParsedSectionName),
        ("parse_function", SNMPParseFunction),
        ("host_label_function", HostLabelFunction),
        ("supersedes", Set[SectionName]),
        ("detect_spec", SNMPDetectBaseType),
        ("trees", List[SNMPTree]),
        ("module", Optional[str]),  # not available for auto migrated plugins.
    ],
)

SectionPlugin = Union[AgentSectionPlugin, SNMPSectionPlugin]

ValueStore = MutableMapping[str, Any]
