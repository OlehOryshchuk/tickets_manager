from flask import (
    Blueprint,
    render_template,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from app.models import Group, Roles
from app.utils import role_required


group_bl = Blueprint("group", __name__)

# Endpoints for Group model


@group_bl.get("/groups/<int:group_id>")
@login_required
@role_required([Roles.analyst.value, Roles.manager.value])
def detail_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    if current_user not in group.users:
        abort(403, description="You are not assigned for this group")
    return render_template("groups/group_detail.html", group=group)
