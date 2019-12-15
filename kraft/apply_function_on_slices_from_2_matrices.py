from numpy import full, nan

from .apply_function_on_2_vectors import apply_function_on_2_vectors
from .check_array_for_bad import check_array_for_bad


def apply_function_on_slices_from_2_matrices(
    matrix_0,
    matrix_1,
    axis,
    function,
    n_required=None,
    raise_for_n_less_than_required=True,
    raise_for_bad=True,
    use_only_good=True,
):

    check_array_for_bad(matrix_0, raise_for_bad=raise_for_bad)

    check_array_for_bad(matrix_1, raise_for_bad=raise_for_bad)

    if axis == 0:

        matrix_0 = matrix_0.T

        matrix_1 = matrix_1.T

    matrix = full((matrix_0.shape[0], matrix_1.shape[0]), nan)

    for i_0 in range(matrix_0.shape[0]):

        matrix_0_slice = matrix_0[i_0]

        for i_1 in range(matrix_1.shape[0]):

            matrix[i_0, i_1] = apply_function_on_2_vectors(
                matrix_0_slice,
                matrix_1[i_1],
                function,
                n_required=n_required,
                raise_for_n_less_than_required=raise_for_n_less_than_required,
                raise_for_bad=raise_for_bad,
                use_only_good=use_only_good,
            )

    return matrix