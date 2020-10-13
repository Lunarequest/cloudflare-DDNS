from cloudflare_ddns.verify import verify
from cloudflare_ddns.internals import read_data_record
def test_answer():
    data=read_data_record()
    response= verify(data)
    print(response)
    assert response==False