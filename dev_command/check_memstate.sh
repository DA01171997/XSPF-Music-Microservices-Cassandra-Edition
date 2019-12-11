#!/bin/bash
memcstat --servers=localhost | grep get_hits
memcstat --servers=localhost | grep get_misses
memcstat --servers=localhost | grep curr_items