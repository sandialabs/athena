import pytest

@pytest.fixture(params=['timeloop'])
def output_types(request):
    return request.param


def test_get_output_parser(self,output_types):
    
