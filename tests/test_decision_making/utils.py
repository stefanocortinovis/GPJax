# Copyright 2023 The JaxGaussianProcesses Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import jax.numpy as jnp

from beartype.typing import Mapping

from gpjax.dataset import Dataset
from gpjax.decision_making.test_functions import Quadratic
from gpjax.decision_making.utility_functions import (
    AbstractSinglePointUtilityFunctionBuilder,
    SinglePointUtilityFunction,
)
from gpjax.gps import ConjugatePosterior, NonConjugatePosterior, Prior
from gpjax.typing import KeyArray
from gpjax.kernels import RBF
from gpjax.likelihoods import (
    Gaussian,
    Poisson,
)
from gpjax.mean_functions import Zero


class QuadraticSinglePointUtilityFunctionBuilder(
    AbstractSinglePointUtilityFunctionBuilder
):
    """
    Dummy utility function builder for testing purposes, which returns the negative
    of the value of a quadratic test function at the input points. This is because
    utility functions are *maximised*, and we wish to *minimise* the quadratic test
    function. Note that this is a `SinglePointUtilityFunctionBuilder`.
    """

    def build_utility_function(
        self,
        posteriors: Mapping[str, ConjugatePosterior],
        datasets: Mapping[str, Dataset],
        key: KeyArray,
    ) -> SinglePointUtilityFunction:
        test_function = Quadratic()
        return lambda x: -1.0 * test_function.evaluate(
            x
        )  # Utility functions are *maximised*


def generate_dummy_conjugate_posterior(dataset: Dataset) -> ConjugatePosterior:
    kernel = RBF(lengthscale=jnp.ones(dataset.X.shape[1]))
    mean_function = Zero()
    prior = Prior(kernel=kernel, mean_function=mean_function)
    likelihood = Gaussian(num_datapoints=dataset.n)
    posterior = prior * likelihood
    return posterior


def generate_dummy_non_conjugate_posterior(dataset: Dataset) -> NonConjugatePosterior:
    kernel = RBF(lengthscale=jnp.ones(dataset.X.shape[1]))
    mean_function = Zero()
    prior = Prior(kernel=kernel, mean_function=mean_function)
    likelihood = Poisson(num_datapoints=dataset.n)
    posterior = prior * likelihood
    return posterior
