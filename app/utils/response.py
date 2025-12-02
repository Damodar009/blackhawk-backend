from fastapi.responses import JSONResponse


def success_response(data=None, message: str = "Success", status_code: int = 200):
    """
    Standardized success response for all API endpoints.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "data": data
        }
    )

def paginated_success_response(
    data,
    total_count: int,
    skip: int,
    limit: int,
    message: str = "Success",
    status_code: int = 200
):
    """
    Standardized paginated success response.
    Includes data + minimal pagination metadata.
    """
    current_page = (skip // limit) + 1 if limit > 0 else 1

    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "data": {
                "items": data,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "current_page": current_page,
                },
            },
        },
    )

