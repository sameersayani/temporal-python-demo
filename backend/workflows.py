from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from .activities import (
        validate_policy,
        calculate_premium,
        save_policy,
        send_notification,
    )


@workflow.defn
class PolicyWorkflow:

    @workflow.run
    async def run(
        self,
        policy_id: str,
        customer_id: str,
        coverage_amount: float,
    ) -> dict:

        # 1. Validate
        validation_result = await workflow.execute_activity(
            validate_policy,
            args=[policy_id, customer_id],
            start_to_close_timeout=timedelta(seconds=30),
        )

        if validation_result != "VALID":
            return {
                "status": "FAILED",
                "reason": "Invalid policy",
            }

        # 2. Calculate premium
        premium = await workflow.execute_activity(
            calculate_premium,
            args=[policy_id, coverage_amount],
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 3. Save policy
        save_result = await workflow.execute_activity(
            save_policy,
            args=[
                policy_id,
                customer_id,
                premium,
            ],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            ),
        )

        # 4. Send notification
        notification_result = await workflow.execute_activity(
            send_notification,
            args=[policy_id, customer_id],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            ),
        )

        return {
            "status": "COMPLETED",
            "policy_id": policy_id,
            "premium": premium,
            "save": save_result,
            "notification": notification_result,
        }