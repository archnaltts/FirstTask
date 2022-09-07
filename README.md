# FirstTask
A task from SkyTeam for practice


# To Run the application
a) Clone it
b) sudo docker-compose build
c) sudo docker-compose up

#Run API-Url in postman
a)Method = 'POST', Url to add users : http://0.0.0.0:5000/api/v1/addusers/
b)Method = 'GET', Url to get all users : http://0.0.0.0:5000/api/v1/users
c)Method = 'GET', Url to get user by token stored in Redis : http://0.0.0.0:5000/api/v1/usertoken/<user_token>
d)Method = 'GET', Url to get user by id from mongo db : http://0.0.0.0:5000/api/v1/user/<id>
e)Mehod = 'Delete', Url to delete user using its ID : http://0.0.0.0:5000/api/v1/delete/<id>
f)Method = 'PUT', Url to update user using its ID : http://0.0.0.0:5000/api/v1/update/<id>
