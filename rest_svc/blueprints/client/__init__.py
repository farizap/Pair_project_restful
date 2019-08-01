# import random

# ## Client class
# class Client():
#     def __init__(self):
#         self.reset()

#     def reset(self):
#         self.client_id = None
#         self.client_key = 0
#         self.client_secret = None
#         self.status = None

#     def serialize(self):
#         return {
#             'client_id':self.client_id,
#             'client_key':self.client_key,
#             'client_secret':self.client_secret,
#             'status':self.status
#         }

# class Clients():

#     list_client = []

#     def __init__(self):

#         for i in range(20):
#             client = Client()
#             client.client_id = i
#             client.client_key = "CLIENT0" + str(i)
#             client.client_secret = "SECRET0" + str(i)
#             client.status = random.choice(["True", "False"])

#             self.add(client.serialize())
    
#     def add(self,client_serialized):
#         self.list_client.append(client_serialized)


#     def get_list(self):
#         return self.list_client

#     def get_one(self,id):
#         for val in self.list_client:
#             if val['client_id'] == int(id):
#                 return val
#         return None

#     def edit_one(self,id, client_key, client_secret, status):
#         for ind, val in enumerate(self.list_client):
#             if val['client_id'] == int(id):
#                 client = Client()
#                 client.client_id = int(id)
#                 client.client_key = client_key
#                 client.client_secret = client_secret
#                 client.status = status

#                 self.list_client[ind] = client.serialize()
#                 return self.list_client[ind]
#         return None
                


#     def delete_one(self, id):
#         for ind,val in enumerate(self.list_client):
#             if val['client_id'] == int(id):
#                 return self.list_client.pop(ind)
#         return None


