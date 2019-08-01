import json
from . import app, client, cache, create_token_noninternal


class TestrentCrud():

    rent_id = 0


########### get list
    def test_get_rent_list_valid(self, client):
        token = create_token_noninternal()
        res = client.get('/rent/list', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_rent_list_invalid(self, client):
        res = client.get('/rent/list', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

########## post

    def test_post_rent_invalid(self, client):
        token = create_token_noninternal()
        data = {
            "book_id":2
        }
        res = client.post('/rent', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_rent_valid(self, client):
        token = create_token_noninternal()
       
        data = {
            "user_id":7,
            "book_id":2
        }

        res = client.post('/rent', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestrentCrud.rent_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############ get by id
    def test_get_by_id_rent_valid(self, client):
        token = create_token_noninternal()
       

        res = client.get(f'/rent/{TestrentCrud.rent_id}', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_rent_invalid(self, client):
        token = create_token_noninternal()
       

        res = client.get('/rent/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404

