"""Entry point for the cppwg package."""

import argparse
import logging

from cppwg import CppWrapperGenerator


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns
    -------
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="cppwg",
        description="Generate Python Wrappers for C++ code",
    )

    parser.add_argument(
        "source_root",
        metavar="SOURCE_ROOT",
        type=str,
        help="Path to the root directory of the input C++ source code.",
    )

    parser.add_argument(
        "-w",
        "--wrapper_root",
        type=str,
        help="Path to the output directory for the Pybind11 wrapper code.",
    )

    parser.add_argument(
        "-p", "--package_info", type=str, help="Path to the package info file."
    )

    parser.add_argument(
        "-c",
        "--castxml_binary",
        type=str,
        help="Path to the castxml executable.",
    )

    parser.add_argument(
        "-f",
        "--castxml_cflags",
        type=str,
        help="Extra cflags for CastXML e.g. '-std=c++17'.",
    )

    parser.add_argument(
        "-i",
        "--include",
        type=str,
        action="append",
        help="Paths to include directories.",
    )

    args = parser.parse_args()

    return args


def generate(args: argparse.Namespace) -> None:
    """
    Generate the Python wrappers.

    Parameters
    ----------
    args : argparse.Namespace
        The parsed command line arguments.
    """
    generator = CppWrapperGenerator(
        source_root=args.source_root,
        source_includes=args.include,
        wrapper_root=args.wrapper_root,
        package_info_path=args.package_info,
        castxml_binary=args.castxml_binary,
        castxml_cflags=args.castxml_cflags,
    )

    generator.generate_wrapper()


def main() -> None:
    """Generate wrappers from command line arguments."""
    logging.basicConfig(
        format="%(levelname)s %(message)s",
        handlers=[logging.FileHandler("filename.log"), logging.StreamHandler()],
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    args = parse_args()
    generate(args)


if __name__ == "__main__":
    main()
