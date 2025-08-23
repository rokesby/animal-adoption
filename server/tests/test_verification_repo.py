
import uuid
from helpers.helpers import generate_pin


def test_add_verification(verification_repo):
    """
    SHOULD add a new verification entry to db
    """
    repo = verification_repo
    user_id = 19
    _, hashed_pin = generate_pin()
    
    result = repo.add_verification(user_id, hashed_pin)
    
    assert result.user_id == 19
    assert result.pin_hash == hashed_pin

def test_get_verification_by_id(verification_repo):
    """
    GIVEN an id
    SHOULD return the verification matching the id
    """
    repo = verification_repo
    user_id = 19
    _, hashed_pin = generate_pin()
    
    verification = repo.add_verification(user_id, hashed_pin)
    
    verification_id = verification.id
    
    result = repo.get_verification_by_id(verification_id)
    
    assert result.id == verification_id
    assert result.user_id == 19
    assert result.pin_hash == hashed_pin
    
def test_get_verification_by_id_doesnt_return_used_tokens(verification_repo):
    """
    GIVEN an id
    SHOULD NOT return the verification matching the id
    IF used_at has been populated
    """
    repo = verification_repo
    
    verification_id=uuid.UUID('5a991853-3ff2-48b3-b4f2-d5399324bfd4')
    
    result = repo.get_verification_by_id(verification_id)
    
    assert result is None

    
def test_update_verification_used_at(verification_repo):
    """
    GIVEN a valid verification_id
    update_verification_used_at
    SHOULD update the given column with the current time
    """
    repo = verification_repo
    verification_id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    
    result = repo.update_verification_used_at(verification_id)
    print(result.used_at)
    assert result.used_at is not None