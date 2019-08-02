import json
from . import app, client, cache, create_token


class TestTripCrud():

    trip_id = 0


########### get list
    def test_get_trip_list_valid(self, client):
        token = create_token()
        res = client.get('/trip/internal/list', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_trip_list_invalid(self, client):
        res = client.get('/trip/internal/list', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

########## post

    def test_post_trip_invalid(self, client):
        token = create_token()
        data = {
            "client_id":3
        }
        res = client.post('/trip/internal', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_trip_valid(self, client):
        token = create_token()
       
        data = {
            "client_id":3,
        	"event_id":5,
            "airport":"TEST"
            
        }

        res = client.post('/trip/internal', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestTripCrud.trip_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200

########### put
    def test_put_trip_valid(self, client):
        token = create_token()
       
        data = {
            "event_id":5,
            "client_id":3,
            "airport":"TEST"
        }

        res = client.put(f'/trip/internal/{TestTripCrud.trip_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_trip_invalid(self, client):
        token = create_token()
       
        data = {
            "client_id":3
        }

        res = client.put(f'/trip/internal/{TestTripCrud.trip_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400


############ get by id
    def test_get_by_id_trip_valid(self, client):
        token = create_token()
       

        res = client.get(f'/trip/internal/{TestTripCrud.trip_id}', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_trip_invalid(self, client):
        token = create_token()
       

        res = client.get('/trip/internal/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404


########### delete

    def test_delete_trip_valid(self, client):
        token = create_token()

        res = client.delete(f'/trip/internal/{TestTripCrud.trip_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_trip_invalid(self, client):
        token = create_token()

        res = client.delete('/trip/internal/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404


