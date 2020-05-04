#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from const.constants import (
    LEVEL1,
    LEVEL2,
    LEVEL3,
    LEVEL4,
    LEVEL5,
)
from functions.verbose_mode import verbose_mode


@given(u'I create a varibale with verbose mode level1')
def step_impl(context):
    context.level1 = LEVEL1


@given(u'I create a varibale with verbose mode level2')
def step_impl(context):
    context.level2 = LEVEL2


@given(u'I create a varibale with verbose mode level3')
def step_impl(context):
    context.level3 = LEVEL3


@given(u'I create a varibale with verbose mode level4')
def step_impl(context):
    context.level4 = LEVEL4


@given(u'I create a varibale with verbose mode level5')
def step_impl(context):
    context.level5 = LEVEL5


@then(u'I test that function with level1 works')
def step_impl(context):
    assert verbose_mode(
        user_value=context.level1,
        needed_value=LEVEL1
    )

    assert not verbose_mode(
        user_value=context.level1,
        needed_value=LEVEL2
    )

    assert not verbose_mode(
        user_value=context.level1,
        needed_value=LEVEL3
    )

    assert not verbose_mode(
        user_value=context.level1,
        needed_value=LEVEL4
    )

    assert not verbose_mode(
        user_value=context.level1,
        needed_value=LEVEL5
    )


@then(u'I test that function with level2 works')
def step_impl(context):
    assert verbose_mode(
        user_value=context.level2,
        needed_value=LEVEL1
    )

    assert verbose_mode(
        user_value=context.level2,
        needed_value=LEVEL2
    )

    assert not verbose_mode(
        user_value=context.level2,
        needed_value=LEVEL3
    )

    assert not verbose_mode(
        user_value=context.level2,
        needed_value=LEVEL4
    )

    assert not verbose_mode(
        user_value=context.level2,
        needed_value=LEVEL5
    )


@then(u'I test that function with level3 works')
def step_impl(context):
    assert verbose_mode(
        user_value=context.level3,
        needed_value=LEVEL1
    )

    assert verbose_mode(
        user_value=context.level3,
        needed_value=LEVEL2
    )

    assert verbose_mode(
        user_value=context.level3,
        needed_value=LEVEL3
    )

    assert not verbose_mode(
        user_value=context.level3,
        needed_value=LEVEL4
    )

    assert not verbose_mode(
        user_value=context.level3,
        needed_value=LEVEL5
    )


@then(u'I test that function with level4 works')
def step_impl(context):
    assert verbose_mode(
        user_value=context.level4,
        needed_value=LEVEL1
    )

    assert verbose_mode(
        user_value=context.level4,
        needed_value=LEVEL2
    )

    assert verbose_mode(
        user_value=context.level4,
        needed_value=LEVEL3
    )

    assert verbose_mode(
        user_value=context.level4,
        needed_value=LEVEL4
    )

    assert not verbose_mode(
        user_value=context.level4,
        needed_value=LEVEL5
    )


@then(u'I test that function with level5 works')
def step_impl(context):
    assert verbose_mode(
        user_value=context.level5,
        needed_value=LEVEL1
    )

    assert verbose_mode(
        user_value=context.level5,
        needed_value=LEVEL2
    )

    assert verbose_mode(
        user_value=context.level5,
        needed_value=LEVEL3
    )

    assert verbose_mode(
        user_value=context.level5,
        needed_value=LEVEL4
    )

    assert verbose_mode(
        user_value=context.level5,
        needed_value=LEVEL5
    )