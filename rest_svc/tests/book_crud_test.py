import json
from . import app, client, cache, create_token


class TestbookCrud():

    book_id = 0


########### get list
    def test_get_book_list_valid(self, client):
        token = create_token()
        res = client.get('/books/list', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_book_list_invalid(self, client):
        res = client.get('/books/list', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

########## post

    def test_post_book_invalid(self, client):
        token = create_token()
        data = {
            "writer":"sutoyo"
        }
        res = client.post('/books', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_book_valid(self, client):
        token = create_token()
       
        data = {
            "title":"blink",
            "isbn":"123-1231235-2",
            "writer":"sutoyo"
        }

        res = client.post('/books', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestbookCrud.book_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200

########### put
    def test_put_book_valid(self, client):
        token = create_token()
       
        data = {
            "title":"homo sapiens",
            "isbn":"123-1232131235-2",
            "writer":"broh"
        }

        res = client.put(f'/books/{TestbookCrud.book_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_book_invalid(self, client):
        token = create_token()
       
        data = {
            "writer":"sutoyo"
        }

        res = client.put(f'/books/{TestbookCrud.book_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400


############ get by id
    def test_get_by_id_book_valid(self, client):
        token = create_token()
       

        res = client.get(f'/books/{TestbookCrud.book_id}', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_book_invalid(self, client):
        token = create_token()
       

        res = client.get('/books/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404



########### delete

    def test_delete_book_valid(self, client):
        token = create_token()

        res = client.delete(f'/books/{TestbookCrud.book_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_book_invalid(self, client):
        token = create_token()

        res = client.delete('/books/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404


