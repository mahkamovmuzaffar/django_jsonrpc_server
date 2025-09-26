# Created by Muzaffar Makhkamov on 6/6/23, 11:24 PM
# Please make contact with me if you have any questions.
def create(user, ext_id, sender, receiver, amount, currency):
    """
    Create a new transfer if ext_id does not already exist for the user.
    """
    from v1.models.transfer import Transfer
    if Transfer.objects.filter(user=user, ext_id=ext_id).exists():
        return {'error': 'ext_id already exists'}
    # ...continue with creation logic...
    # For now, just a placeholder for actual creation
    # Transfer.objects.create(user=user, ext_id=ext_id, sender=sender, receiver=receiver, amount=amount, currency=currency)
    return {'success': True}


def confirm(user, ext_id):
    # Implement your logic here
    pass


def state(user, ext_id):
    # Implement your logic here
    pass
