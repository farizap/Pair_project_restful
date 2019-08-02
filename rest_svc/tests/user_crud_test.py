import json
from . import app, client, cache, create_token


class TestUserCrud():

    user_id = 0


########### get list
    def test_get_user_list_valid(self, client):
        token = create_token()
        res = client.get('/user/list', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_user_list_invalid(self, client):
        res = client.get('/user/list', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

########## post

    def test_post_user_invalid(self, client):
        token = create_token()
        data = {
            "age": 56,
        }
        res = client.post('/user', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_user_valid(self, client):
        token = create_token()
       
        data = {
        	"client_id":3,
            "name":"sukamto",
            "age":56,
            "sex":"female"
        }

        res = client.post('/user', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestUserCrud.user_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200

########### put
    def test_put_user_valid(self, client):
        token = create_token()
       
        data = {
            "name": "Rudy Sujarswoadass",
            "age": 56,
            "sex": "male",
            "client_id": 3
        }

        res = client.put(f'/user/{TestUserCrud.user_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_user_invalid(self, client):
        token = create_token()
       
        data = {
            "age": 56,
        }

        res = client.put(f'/user/{TestUserCrud.user_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400


############ get by id
    def test_get_by_id_user_valid(self, client):
        token = create_token()
       

        res = client.get(f'/user/{TestUserCrud.user_id}', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_user_invalid(self, client):
        token = create_token()
       

        res = client.get('/user/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404


########### delete

    def test_delete_user_valid(self, client):
        token = create_token()

        res = client.delete(f'/user/{TestUserCrud.user_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_user_invalid(self, client):
        token = create_token()

        res = client.delete('/client/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404


