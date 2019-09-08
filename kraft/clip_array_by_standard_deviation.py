from .check_array_for_bad import check_array_for_bad


def clip_array_by_standard_deviation(array, standard_deviation, raise_for_bad=True):

    is_good = ~check_array_for_bad(array, raise_for_bad=raise_for_bad)

    array_ = array.copy()

    if not is_good.any():

        return array_

    array_good = array[is_good]

    array_good_mean = array_good.mean()

    array_good_interval = array_good.std() * standard_deviation

    array_[is_good] = array[is_good].clip(
        min=array_good_mean - array_good_interval,
        max=array_good_mean + array_good_interval,
    )

    return array_
