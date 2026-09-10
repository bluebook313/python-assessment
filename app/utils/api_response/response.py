from fastapi import Response


class CustoneResponse(Response):
    def response(self, details, status):
        return {
            "Status":status,
            "Details":details
        }