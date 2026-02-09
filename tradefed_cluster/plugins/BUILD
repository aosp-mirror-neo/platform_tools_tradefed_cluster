load("//third_party/bazel_rules/rules_python/python:py_test.bzl", "py_test")
load("//tradefed_cluster:adapter.bzl", "py_library", "pytype_strict_library", "third_party")

package(
    default_applicable_licenses = ["//tradefed_cluster:license"],
    default_visibility = ["//tradefed_cluster:tradefed_cluster_clients"],
)

licenses(["notice"])

py_library(
    name = "appengine_lib",
    srcs = [
        "appengine.py",
    ],
    strict_deps = False,
    deps = [
        ":base_lib",
    ],
)

pytype_strict_library(
    name = "base_lib",
    srcs = [
        "base.py",
    ],
    deps = [
        third_party("six"),
    ],
)

py_test(
    name = "base_test",
    srcs = [
        "base_test.py",
    ],
    strict_deps = False,
    deps = [
        ":base_lib",
        "//third_party/py/google/protobuf:use_fast_cpp_protos",  # Automatically added go/proto_python_upb_flip
    ],
)

py_library(
    name = "google_cloud_lib",
    srcs = [
        "google_cloud.py",
    ],
    strict_deps = False,
    deps = [
        ":base_lib",
        third_party("google-cloud-tasks"),
        third_party("six"),
    ],
)

py_test(
    name = "google_cloud_test",
    srcs = [
        "google_cloud_test.py",
    ],
    strict_deps = False,
    deps = [
        ":google_cloud_lib",
        third_party("mock"),
        "//third_party/py/google/protobuf:use_fast_cpp_protos",  # Automatically added go/proto_python_upb_flip
    ],
)

py_library(
    name = "metric_client_lib",
    srcs = [
        "metric_client.py",
    ],
    strict_deps = False,
)

pytype_strict_library(
    name = "noop_plugin_lib",
    srcs = [
        "noop_plugin.py",
    ],
    deps = [
        ":base_lib",
    ],
)

pytype_strict_library(
    name = "registry_lib",
    srcs = [
        "registry.py",
    ],
    deps = [
        ":base_lib",
        ":noop_plugin_lib",
    ],
)

py_test(
    name = "registry_test",
    srcs = [
        "registry_test.py",
    ],
    strict_deps = False,
    deps = [
        ":registry_lib",
        third_party("mock"),
        "//third_party/py/google/protobuf:use_fast_cpp_protos",  # Automatically added go/proto_python_upb_flip
    ],
)

