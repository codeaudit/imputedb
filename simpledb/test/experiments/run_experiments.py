#!/usr/bin/env python

from __future__ import print_function
import os
import subprocess
import tempfile

executable_default    = ["java","-Xmx3200m","-jar","../../dist/simpledb.jar"]
executable_longimpute = ["java","-Xmx3200m","-Dsimpledb.ImputeSlow","-jar","../../dist/simpledb.jar"]
output_dir            = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")
catalog_default       = "../../catalog.txt"
queries_default       = "queries.txt"

def run_small_experiment():
    this_output_dir = os.path.join(output_dir, "small")

    iters     = 3
    min_alpha = 0.01
    max_alpha = 0.99
    step      = 0.32

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step)

def run_medium_experiment():
    this_output_dir = os.path.join(output_dir, "medium")

    iters     = 100
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 0.20

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step)

def run_large_experiment():
    this_output_dir = os.path.join(output_dir, "large")

    iters     = 220
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 1.00

    queries = "queries01.txt"

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step, queries =
            queries, executable = executable_longimpute)

def run_alt_experiment():
    this_output_dir = os.path.join(output_dir, "alt")

    iters     = 220
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 1.00

    queries = "queries02.txt"

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step, queries =
            queries, executable = executable_longimpute)

def run_large03_experiment():
    this_output_dir = os.path.join(output_dir, "large03")

    iters     = 220
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 1.00

    queries = "queries03.txt"

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step, queries =
            queries, executable = executable_longimpute)

def run_large04_experiment():
    this_output_dir = os.path.join(output_dir, "large04")

    iters     = 220
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 1.00

    queries = "queries04.txt"

    run_experiment(this_output_dir, iters, min_alpha, max_alpha, step, queries =
            queries, executable = executable_longimpute)

def run_acs_experiment():
    catalog = catalog_default
    executable = executable_default

    this_output_dir = os.path.join(output_dir, "acs")

    # Impute on base table
    (f, acs_query) = tempfile.mkstemp()
    os.write(f, "SELECT AVG(c0) FROM acs_dirty;\n")

    iters = 1

    print("Running acs base...")
    executable_max_heap = [executable[0]] + ["-Xmx3200m", "-Dsimpledb.ImputeSlow"] + executable[1:]
    cmd = executable_max_heap + \
        ["experiment", catalog, acs_query, this_output_dir, str(iters), "--base"]
    print(cmd)
    subprocess.call(cmd)
    print("Running acs base...done.")

    # Impute using ImputeDB
    iters     = 220
    min_alpha = 0.00
    max_alpha = 1.00
    step      = 1.00

    subprocess.call(executable_longimpute +
        ["experiment", catalog, acs_query, this_output_dir,
         str(iters), str(min_alpha), str(max_alpha), str(step)])

    os.close(f)

def run_experiment(this_output_dir, iters, min_alpha, max_alpha, step,
        queries=None, executable=None):
    if not os.path.isdir(this_output_dir):
        os.makedirs(this_output_dir)

    if not queries:
        queries = queries_default

    if not executable:
        executable = executable_default


    catalog = catalog_default

    # Timing using ImputeDB
    subprocess.call(executable +
        ["experiment", catalog, queries, this_output_dir,
         str(iters), str(min_alpha), str(max_alpha), str(step)])

    # Timing using impute on base table
    subprocess.call(executable +
        ["experiment", catalog, queries, this_output_dir,
         str(iters), "--base"])

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        experiment_size = sys.argv[1]
    else:
        experiment_size = "small"

    if experiment_size == "small":
        run_small_experiment()
    elif experiment_size == "medium":
        run_medium_experiment()
    elif experiment_size == "large":
        run_large_experiment()
    elif experiment_size == "alt":
        run_alt_experiment()
    elif experiment_size == "large03":
        run_large03_experiment()
    elif experiment_size == "large04":
        run_large04_experiment()
    elif experiment_size == "acs":
        run_acs_experiment()
    else:
        raise Error

    print("Done.")
