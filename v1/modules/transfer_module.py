# Created by Muzaffar Makhkamov on 6/6/23, 11:24 PM
# Please make contact with me if you have any questions.
from v1.models.transfer import Transfer
import uuid
from datetime import datetime


def create(user, ext_id, sender, receiver, amount, currency):
    """
    Create a new transfer if ext_id does not already exist for the user.
    """

    if Transfer.objects.filter(user=user, ext_id=ext_id).exists():
        return {'error': 'ext_id already exists'}
    # ...continue with creation logic...

    now = datetime.now().strftime('%m%d%y%H%M%S')
    uid = str(uuid.uuid4()).replace('-', '')[:10]
    ref_num = f"{user.id}-{now}-{uid}"

    cheque = Transfer.objects.create(
        user=user,
        ext_id=ext_id,
        ref_num=ref_num,
        sender=sender,
        receiver=receiver,
        amount=amount,
        currency=currency
    )

    return cheque.to_result()


def confirm(user, ext_id):
    # Implement your logic here
    pass


def state(user, ext_id):
    # Implement your logic here
    pass
