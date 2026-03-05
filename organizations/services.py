PLAN_LIMITS = {
    "FREE": 3,
    "PRO": 50,
    "ENTERPRISE": 999999,
}


def get_api_limit_for_org(organization):
    """
    Returns max allowed APIs for given organization plan.
    """
    return PLAN_LIMITS.get(organization.plan, 3)