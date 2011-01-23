# -*- coding: utf-8 -*-

def filesize_human_format(size_in_bytes):
    for suffix in ['b','KB','MB','GB','TB']:
        if size_in_bytes < 1024.0:
            return "%3.1f%s" % (size_in_bytes, suffix)
        size_in_bytes /= 1024.0
