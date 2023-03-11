"""
Tests for space adapter factory.
"""

# pylint: disable=missing-function-docstring

import pytest

import ConfigSpace as CS

from mlos_core.spaces.adapters import SpaceAdapterFactory, SpaceAdapterType
from mlos_core.spaces.adapters.adapter import BaseSpaceAdapter


@pytest.mark.parametrize(('space_adapter_type', 'kwargs'), [
    # Default space adapter
    (None, {}),
    # Enumerate all supported Optimizers
    *[(member, {}) for member in SpaceAdapterType],
])
def test_create_space_adapter_with_factory_method(space_adapter_type: SpaceAdapterType, kwargs):
    # Start defining a ConfigurationSpace for the Optimizer to search.
    input_space = CS.ConfigurationSpace(seed=1234)

    # Add a single continuous input dimension between 0 and 1.
    input_space.add_hyperparameter(CS.UniformFloatHyperparameter(name='x', lower=0, upper=1))
    # Add a single continuous input dimension between 0 and 1.
    input_space.add_hyperparameter(CS.UniformFloatHyperparameter(name='y', lower=0, upper=1))

    # Adjust some kwargs for specific space adapters
    if space_adapter_type is SpaceAdapterType.LLAMATUNE:
        if kwargs is None:
            kwargs = {}
        kwargs.setdefault('num_low_dims', 1)

    space_adapter: BaseSpaceAdapter = None
    if space_adapter_type is None:
        space_adapter = SpaceAdapterFactory.create(input_space)
    else:
        space_adapter = SpaceAdapterFactory.create(input_space, space_adapter_type, space_adapter_kwargs=kwargs)

    if space_adapter_type is None or space_adapter_type is SpaceAdapterType.IDENTITY:
        assert space_adapter is None
    else:
        assert space_adapter is not None
        assert space_adapter.orig_parameter_space is not None
        myrepr = repr(space_adapter)
        assert myrepr.startswith(space_adapter_type.value.__name__), \
            f"Expected {space_adapter_type.value.__name__} but got {myrepr}"