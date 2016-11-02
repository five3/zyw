#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime


def split_date(date):
    all = date.split('-')
    year = all[0]
    month = all[1]
    day = all[2]
    return year, month, day


def strtodatetime(datestr,format='%Y-%m-%d'):
    return datetime.datetime.strptime(datestr.strip(), format)


def gyrc_ite(start='2015-01-01', end=None, ttl=50):
    if not end:
        end = datetime.date.today()
    else:
        end = strtodatetime(end).date()
    start = strtodatetime(start).date()
    delta = end - start
    if delta.days > 0:
        for i in range(delta.days):
            start = start + datetime.timedelta(days=1)
            year, month, day = split_date(start.strftime('%Y-%m-%d'))
            for j in range(1, 50):
                yield year, month, day, j

