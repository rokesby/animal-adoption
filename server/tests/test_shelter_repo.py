def test_shelter_domain_returns_true():
    """
    given a domain that belongs to an organisation
    is_shelter_domain should return True
    """

def test_non_shelter_domain_returns_false():
    """
    Given a domain that doesn't belong to an organisation
    is_shelter_domain should return False
    """

def test_get_shelter_id_by_domain(shelter_repo):
    """
    Given a valid domain
    get_shelter_id_by_domain
    SHOULD return the id of the shelter
    """
    repo = shelter_repo
    domain = 'example.com'
    
    result = repo.get_shelter_id_by_domain(domain)
    assert result == 1
    
def test_get_shelter_id_by_domain_returns_none(shelter_repo):
    """
    Given a non-shelter domain
    get_shelter_id_by_domain
    SHOULD return None
    """
    repo = shelter_repo
    domain = 'none.com'
    
    result = repo.get_shelter_id_by_domain(domain)
    assert result == None

def test_add_shelter():
    """
    add_new_shelter should create a new shelter
    """