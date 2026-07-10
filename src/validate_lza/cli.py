"""Entry point for the validate-lza pre-commit hooks.

Builds the raw.githubusercontent.com URL for a config type's upstream JSON
Schema at a pinned LZA release tag, then delegates the actual validation to
check-jsonschema (which downloads and caches remote --schemafile URLs).
"""

import argparse
import subprocess
import sys

SCHEMA_URL_TEMPLATE = (
    "https://raw.githubusercontent.com/awslabs/landing-zone-accelerator-on-aws/"
    "{version}/source/packages/@aws-accelerator/config/lib/schemas/{config_type}.json"
)


def build_schema_url(version: str, config_type: str) -> str:
    return SCHEMA_URL_TEMPLATE.format(version=version, config_type=config_type)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="validate-lza")
    parser.add_argument(
        "--lza-version",
        required=True,
        help="LZA release git tag to validate against, e.g. v1.15.5",
    )
    parser.add_argument(
        "--config-type",
        required=True,
        help="LZA config type, matching an upstream schema filename, e.g. global-config",
    )
    parser.add_argument("files", nargs="+", help="Config files to validate")
    args = parser.parse_args(argv)

    schema_url = build_schema_url(args.lza_version, args.config_type)
    result = subprocess.run(
        ["check-jsonschema", "--schemafile", schema_url, *args.files]
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
