#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import (
    LEVEL1,
    LEVEL2,
    LEVEL3,
    LEVEL4,
    LEVEL5
)


def verbose_mode(user_value: str, needed_value) -> bool:

    if (
        user_value == LEVEL1 or
        user_value == LEVEL2 or
        user_value == LEVEL3 or
        user_value == LEVEL4 or
        user_value == LEVEL5
    ):
        if (
            user_value == LEVEL1 and
            needed_value == LEVEL1
        ):
            return True
        elif (
            user_value == LEVEL2 and
            (
                needed_value == LEVEL1 or
                needed_value == LEVEL2
            )
        ):
            return True

        elif (
            user_value == LEVEL3 and
            (
                needed_value == LEVEL1 or
                needed_value == LEVEL2 or
                needed_value == LEVEL3
            )
        ):
            return True
        elif (
            user_value == LEVEL4 and
            (
                needed_value == LEVEL1 or
                needed_value == LEVEL2 or
                needed_value == LEVEL3 or
                needed_value == LEVEL4
            )
        ):
            return True
        elif (
            user_value == LEVEL5 and
            (
                needed_value == LEVEL1 or
                needed_value == LEVEL2 or
                needed_value == LEVEL3 or
                needed_value == LEVEL4 or
                needed_value == LEVEL5
            )
        ):
            return True
        else:
            return False
    else:
        return False
