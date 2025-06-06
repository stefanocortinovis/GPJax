# Copyright 2022 The JaxGaussianProcesses Contributors. All Rights Reserved.
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
from jaxtyping import Float
import numpyro.distributions as npd

from gpjax.kernels.stationary.base import StationaryKernel
from gpjax.kernels.stationary.utils import (
    build_student_t_distribution,
    euclidean_distance,
)
from gpjax.typing import Array


class Matern52(StationaryKernel):
    r"""The Matérn kernel with smoothness parameter fixed at 2.5.


    Computes the covariance for pairs of inputs $(x, y)$ with
    lengthscale parameter $\ell$ and variance $\sigma^2$.

    $$
    k(x, y) = \sigma^2 \exp \Bigg(1+ \frac{\sqrt{5}\lvert x-y \rvert}{\ell^2} + \frac{5\lvert x - y \rvert^2}{3\ell^2} \Bigg)\exp\Bigg(-\frac{\sqrt{5}\lvert x-y\rvert}{\ell^2} \Bigg)
    $$
    """

    name: str = "Matérn52"

    def __call__(
        self, x: Float[Array, " D"], y: Float[Array, " D"]
    ) -> Float[Array, ""]:
        x = self.slice_input(x) / self.lengthscale.value
        y = self.slice_input(y) / self.lengthscale.value
        tau = euclidean_distance(x, y)
        K = (
            self.variance.value
            * (1.0 + jnp.sqrt(5.0) * tau + 5.0 / 3.0 * jnp.square(tau))
            * jnp.exp(-jnp.sqrt(5.0) * tau)
        )
        return K.squeeze()

    @property
    def spectral_density(self) -> npd.StudentT:
        return build_student_t_distribution(nu=5)
