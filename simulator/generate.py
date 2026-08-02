#!/usr/bin/env python3
"""
CLI tool for generating synthetic E-Commerce Payment incident datasets.
Usage:
    python simulator/generate.py --count 1000 --services 10 --output data/payment_incidents.json --seed 42
"""

import argparse
import sys
import logging
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulator.incident_simulator import IncidentSimulator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Synthetic Cloud Incident Dataset Generator (E-Commerce Payment Domain)")
    parser.add_argument("--count", type=int, default=1000, help="Number of incidents to generate (default: 1000)")
    parser.add_argument("--services", type=int, default=10, help="Number of services in topology (default: 10)")
    parser.add_argument("--output", type=str, default="data/payment_incidents.json", help="Output JSON path (default: data/payment_incidents.json)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")

    args = parser.parse_args()

    logging.info(f"Initializing IncidentSimulator (services={args.services}, seed={args.seed})...")
    simulator = IncidentSimulator(service_count=args.services, seed=args.seed)

    logging.info(f"Generating {args.count} incident records...")
    generated_count = simulator.generate_and_export(count=args.count, output_path=args.output)

    logging.info(f"Successfully generated and exported {generated_count} incidents to '{args.output}'.")


if __name__ == "__main__":
    main()
