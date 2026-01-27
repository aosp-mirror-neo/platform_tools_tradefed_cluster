# Copyright 2018 Google Inc. All Rights Reserved.
# Author: xingdai@example.com (Xing Dai)
#
# Package:
#   tradefed_cluster/configs
#
# Description:
#   Tools for configs.

load("//third_party/bazel_rules/rules_python/python:py_test.bzl", "py_test")
load("//tradefed_cluster:adapter.bzl", "proto_library", "py_library", "py_proto_library", "third_party")

package(
    default_applicable_licenses = ["//tradefed_cluster:license"],
    default_visibility = ["//tradefed_cluster:tradefed_cluster_clients"],
)

licenses(["notice"])

py_library(
    name = "lab_config_lib",
    srcs = [
        "lab_config.py",
    ],
    strict_deps = False,
    visibility = ["//visibility:public"],
    deps = [
        ":lab_config_py_pb2",
        ":unified_lab_config_lib",
        third_party("strictyaml"),
        "//net/proto2/python/public",
    ],
)

py_library(
    name = "unified_lab_config_lib",
    srcs = [
        "unified_lab_config.py",
    ],
    strict_deps = False,
    visibility = ["//visibility:public"],
    deps = [
        third_party("ansible"),
        third_party("strictyaml"),
    ],
)

proto_library(
    name = "lab_config_proto",
    srcs = [
        "lab_config.proto",
    ],
)

py_proto_library(
    name = "lab_config_py_pb2",
    srcs = [
        "lab_config.proto",
    ],
    deps = [
        ":lab_config_proto",
    ],
)

py_test(
    name = "lab_config_test",
    srcs = ["lab_config_test.py"],
    data = [
        ":testdata",
    ],
    deps = [
        ":lab_config_lib",
        third_party("six"),
    ],
)

py_test(
    name = "unified_lab_config_test",
    srcs = [
        "unified_lab_config_test.py",
    ],
    data = [
        ":testdata",
    ],
    deps = [
        ":unified_lab_config_lib",
    ],
)


filegroup(
    name = "testdata",
    srcs = glob(["testdata/**"]),
)
