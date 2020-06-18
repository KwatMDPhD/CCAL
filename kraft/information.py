from numpy import asarray, exp, log, nan, outer, sign, sqrt, unique
from scipy.stats import pearsonr

from .array import normalize
from .kernel_density import get_bandwidth
from .point_x_dimension import get_grids, grid
from .probability import get_pdf


def get_entropy(vector):

    probability = vector / vector.sum()

    return -(probability * log(probability)).sum()


def get_kld(vector_0, vector_1):

    return vector_0 * log(vector_0 / vector_1)


def get_ic(vector_0, vector_1):

    if unique(vector_0).size == 1 or unique(vector_1).size == 1:

        return nan

    vector_0 = normalize(vector_0, "-0-")

    vector_1 = normalize(vector_1, "-0-")

    r = pearsonr(vector_0, vector_1)[0]

    bandwidth_factor = 1 - abs(r) * 2 / 3

    bandwidths = (
        get_bandwidth(vector_0) * bandwidth_factor,
        get_bandwidth(vector_1) * bandwidth_factor,
    )

    fraction_grid_extension = 0.1

    n_grid = 24

    grids = (
        grid(vector_0.min(), vector_0.max(), fraction_grid_extension, n_grid),
        grid(vector_1.min(), vector_1.max(), fraction_grid_extension, n_grid),
    )

    (x_grid, y_grid), pxy = get_grids(
        *get_pdf(
            asarray((vector_0, vector_1)).T,
            plot=False,
            bandwidths=bandwidths,
            grids=grids,
        )
    )

    dx = x_grid[1] - x_grid[0]

    dy = y_grid[1] - y_grid[0]

    px = pxy.sum(axis=1) * dy

    py = pxy.sum(axis=0) * dx

    pxpy = outer(px, py)

    mi = get_kld(pxy, pxpy).sum() * dx * dy

    ic = sqrt(1 - exp(-2 * mi))

    return sign(r) * ic


def get_icd(vector_0, vector_1):

    return -(get_ic(vector_0, vector_1) - 1)


def get_jsd(vector_0, vector_1, vector_reference=None):

    if vector_reference is None:

        vector_reference = (vector_0 + vector_1) / 2

    kld_0 = get_kld(vector_0, vector_reference)

    kld_1 = get_kld(vector_1, vector_reference)

    return kld_0, kld_1, kld_0 - kld_1


def get_zd(vector_0, vector_1):

    kld_0 = get_kld(vector_0, vector_1)

    kld_1 = get_kld(vector_1, vector_0)

    return kld_0, kld_1, kld_0 - kld_1