# [API for Blog Website](https://fastapi-devansh.herokuapp.com)

## Features
- Can Create User
- Login User
- Only users can Create Posts
- Owner of Posts can edit, delete posts
- Users can vote posts


# Routes 

### Posts
                    
Route  | Method | Purpose
------------- | ------------- | -------------
/posts  | GET | Get all posts 
/posts/{id}  | GET | Get a particular post using Post ID
/posts | POST | Create a Post 
/posts/{id} | PUT | Update an existing Post
/posts/{id} | DEL | Delete a post 


### Users
                    
Route  | Method | Purpose
------------- | ------------- | -------------
/users  | POST | Create a User
/users/{id}  | GET | Get a particular user details using User ID
/users/{username} | GET | Get a particular user details using username


### Votes
                    
Route  | Method | Purpose
------------- | ------------- | -------------
/votes  | POST | Like or Remove Like from a post
