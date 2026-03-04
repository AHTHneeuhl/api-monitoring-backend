class OrganizationMiddleware:
    """
    Attaches organization to request object.
    Ensures all tenant queries can use request.organization.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.organization = request.user.organization
        else:
            request.organization = None

        response = self.get_response(request)
        return response