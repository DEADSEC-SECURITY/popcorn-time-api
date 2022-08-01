#  Copyright (c) 2022.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

import logging
import functools


# Wrapper for deprecated function
def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning(
            f'The function {func.__name__} is deprecated and will be removed in the next major release.')
        return func(*args, **kwargs)

    return wrapper


# Wrapper for beta functions
def beta(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning(f'The function {func.__name__} is in BETA so might not work 100% of the '
                        f'times.')
        return func(*args, **kwargs)

    return wrapper
