from app.rest_api import bp


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    Return a user based on their ID
    """
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['POST'])
def create_user():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
