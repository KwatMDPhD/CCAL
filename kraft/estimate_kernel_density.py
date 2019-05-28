from numpy import linspace
from statsmodels.nonparametric.kernel_density import KDEMultivariate

from .make_mesh_grid_point_x_dimension import make_mesh_grid_point_x_dimension


def estimate_kernel_density(
    variables, bandwidths=None, mins=None, maxs=None, n_grid=64
):

    n_dimension = len(variables)

    kdemultivariate = KDEMultivariate(variables, "c" * n_dimension, bw=bandwidths)

    if mins is None:

        mins = tuple(variable.min() for variable in variables)

    if maxs is None:

        maxs = tuple(variable.max() for variable in variables)

    n_grids = (n_grid,) * n_dimension

    return kdemultivariate.pdf(
        make_mesh_grid_point_x_dimension(
            (
                linspace(min, max, num=n_grid)
                for (min, max, n_grid) in zip(mins, maxs, n_grids)
            )
        )
    ).reshape(n_grids)
