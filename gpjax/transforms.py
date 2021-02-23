import jax.numpy as jnp
from .types import Array
from chex import dataclass
from typing import Callable


def softplus(x: Array) -> Array:
    """
    Map an input value x from a constrained space into an unconstrained space using the softplus transformation
    :math:`\log(\exp(x)-1)`.

    :param x: A constrained value that exists on the positive real line
    :return: An unconstrained representation of x that exists on the entire real line
    """
    return jnp.log(jnp.exp(x) - 1.0)


def inverse_softplus(x: Array) -> Array:
    """
    Reverse the softplus transformation such that the unconstrained representation now exists on the positive real
    line again using  :math:`\log(1+\exp(x))`.

    :param x: An unconstrained representation of x that exists on the entire real line
    :return: A constrained value that exists on the positive real line
    """
    return jnp.log(1.0 + jnp.exp(x))


@dataclass
class Transformation:
    forward: Callable
    backward: Callable


@dataclass
class SoftplusTransformation(Transformation):
    forward: Callable = softplus
    backward: Callable = inverse_softplus


def transform(params: dict, transformation: Transformation):
    transformed_params = {}
    for k, v in params.items():
        transformed_params[k] = transformation.forward(v)
    return transformed_params


def untransform(params: dict, transformation: Transformation):
    untransformed_params = {}
    for k, v in params.items():
        untransformed_params[k] = transformation.backward(v)
    return untransformed_params
