from fastapi.responses import JSONResponse


class CustomResponse:

    @staticmethod
    def response(status, details, result):
        return JSONResponse(
            status_code=status,
            content={
                "Details": details,
                "Result": result,
            },
        )