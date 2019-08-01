import json
from . import app, client, cache, create_token


class TestClientCrud():

    client_id = 0


########### get list
    def test_get_client_list_valid(self, client):
        token = create_token()
        res = client.get('/client/list', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_client_list_invalid(self, client):
        res = client.get('/client/list', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

########## post
    def test_post_client_invalid(self, client):
        token = create_token()
        data = {
            'client_key': 'CSADSDS'
        }
        res = client.post('/client', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_client_valid(self, client):
        token = create_token()
       
        data = {
        'client_key': 'CLIENT',
        'client_secret': 'SECRET',
        'status': True
        }

        res = client.post('/client', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestClientCrud.client_id = res_json['id']
        # assert res_json['id'] > 0
    
        assert res.status_code == 200

########### put
    def test_put_client_valid(self, client):
        token = create_token()
       
        data = {
        'client_key': 'CLIENT0100',
        'client_secret': 'SECRET0100',
        'status': True
        }

        res = client.put(f'/client/{TestClientCrud.client_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_client_invalid(self, client):
        token = create_token()
       
        data = {
        'client_key': 'CLIENT05',
        'client_secret': 'SECRET05',
        }

        res = client.put(f'/client/{TestClientCrud.client_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 500


############ get by id
    def test_get_by_id_client_valid(self, client):
        token = create_token()
       

        res = client.get(f'/client/{TestClientCrud.client_id}', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_client_invalid(self, client):
        token = create_token()
       

        res = client.get(f'/client/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404


########### delete

    def test_delete_client_valid(self, client):
        token = create_token()

        res = client.delete(f'/client/{TestClientCrud.client_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_client_invalid(self, client):
        token = create_token()

        res = client.delete('/client/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404


