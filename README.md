This is an educational project.
There are 5 API methods have been realized for now:
- POST api/submitData/ - creates a new object in the base. If you want to attach some photos,
you have to transform its into Base64 format. There are some test data in the test.txt
- GET /submitData/{id} - gets the object by its id 
- PATCH /submitData/{id}/ - gets the object for edit if its status is "new". Objects with the other statuses are not allowed to update
- GET /submitData/user__email={email} - gets all objects that are created by the user with specified email in the request