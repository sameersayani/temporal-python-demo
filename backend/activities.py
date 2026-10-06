from temporalio import activity


@activity.defn
async def validate_policy(policy_id: str, customer_id: str) -> str:

    print(f"Validating policy {policy_id}")

    # In real application:
    # - validate customer
    # - validate policy data
    # - call external service
    # - query database

    return "VALID"


@activity.defn
async def calculate_premium(
    policy_id: str,
    coverage_amount: float
) -> float:

    print(
        f"Calculating premium for {policy_id}"
    )

    premium = coverage_amount * 0.0025

    return premium


@activity.defn
async def save_policy(
    policy_id: str,
    customer_id: str,
    premium: float
) -> str:

    print(
        f"Saving policy {policy_id} "
        f"premium={premium}"
    )

    # Real implementation:
    # await postgres.execute(...)

    return "SAVED"


@activity.defn
async def send_notification(
    policy_id: str,
    customer_id: str
) -> str:

    print(
        f"Sending notification for {policy_id}"
    )

    # Real implementation:
    # call email/SMS/notification service

    return "SENT"