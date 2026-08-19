from app.core.tool_permissions import (
    TOOL_PERMISSIONS,
    ToolPermission,
)


class ToolAuthorizationError(
    PermissionError
):
    pass


class ToolAuthorization:

    def __init__(
        self,
        permissions: dict[
            str,
            ToolPermission
        ] | None = None,
    ) -> None:

        self.permissions = (
            permissions
            or TOOL_PERMISSIONS
        )

    def get_permission(
        self,
        tool_name: str,
    ) -> ToolPermission:

        permission = self.permissions.get(
            tool_name
        )

        if permission is None:
            raise ToolAuthorizationError(
                f"Unknown tool: {tool_name}"
            )

        return permission

    def authorize(
        self,
        tool_name: str,
        approved: bool = False,
    ) -> None:

        permission = self.get_permission(
            tool_name
        )

        if permission == ToolPermission.READ:
            return

        if permission == ToolPermission.WRITE and not approved:
            raise ToolAuthorizationError(
                f"Write tool '{tool_name}' "
                "requires authorization."
                )