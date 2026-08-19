import subprocess
import sys


# ============================================================
# PHASE 3 PIPELINE
# ============================================================

STEPS = [
    (
        "EDGE → CLOUD SIMULATION",
        [
            sys.executable,
            "-m",
            "edge.simulator",
        ],
    ),

    (
        "TRANSFER OPTIMIZATION",
        [
            sys.executable,
            "data/models/transfer_optimizer.py",
        ],
    ),

    (
        "CLOUD INTELLIGENCE",
        [
            sys.executable,
            "cloud/intelligence.py",
        ],
    ),

    (
        "UNIFIED EDGE-CLOUD PRIORITY",
        [
            sys.executable,
            "cloud/unified_priority.py",
        ],
    ),

    (
        "FINAL DECISION VALIDATION",
        [
            sys.executable,
            "cloud/final_validator.py",
        ],
    ),
]


def run_step(name, command):

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    result = subprocess.run(
        command,
        cwd=".",
    )

    if result.returncode != 0:

        print()
        print(
            f"❌ {name} FAILED"
        )

        return False

    print()
    print(
        f"✅ {name} COMPLETED"
    )

    return True


def main():

    print()
    print("=" * 70)
    print("EDGE-CLOUD INVENTORY AI")
    print("PHASE 3 PIPELINE")
    print("=" * 70)

    for name, command in STEPS:

        success = run_step(
            name,
            command,
        )

        if not success:

            print()
            print(
                "❌ Phase 3 pipeline stopped."
            )

            sys.exit(1)

    print()
    print("=" * 70)
    print("PHASE 3 PIPELINE COMPLETED")
    print("=" * 70)

    print()
    print("Generated outputs:")

    print(
        "1. data/processed/optimized_transfers.csv"
    )

    print(
        "2. data/processed/cloud_action_plan.csv"
    )

    print(
        "3. data/processed/unified_priority.csv"
    )

    print(
        "4. data/processed/validated_action_plan.csv"
    )


if __name__ == "__main__":

    main()