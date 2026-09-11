from fastapi import Response


class CustoneResponse(Response):
    @staticmethod
    def response(details, status):
        return {
            "Status":status,
            "Details":details
        }