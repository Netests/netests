#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def after_step(context, step):
    if 'own_skipped' in context.scenario.tags:
        context.test_not_implemented.append(step.name)
        context.scenario.tags.remove('own_skipped')
