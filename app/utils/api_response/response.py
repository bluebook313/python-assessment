from fastapi import Response


class CustoneResponse(Response):
    @staticmethod
    def response(details, status, result):
        return {
            "Status":status,
            "Details":details,
            "Result":result
        }