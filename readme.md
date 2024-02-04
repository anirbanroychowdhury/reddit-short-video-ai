# Aim

The main aim of this project is to create an automated short video creation pipeline. Currently short form video platforms are overrun with generic reddit post being narrated with brain dead backgroud video and music playing. The creation of such a
video can be completely automated.

RUN COMMAND: flask --app src.app --debug run

The steps would be:
1. Get the top X number of posts form story subreddit such as r/nosleep or r/aita. 
2. Also get an image of the entire post as that will be overlayed on top of the background video - selenium script????
2. Get the text from this post.
3. Generate a text to speach ai voice over of the post.
4. Generate generic music/video for background.
5. Stich all the 3 things together. 

Adding a flask backend for easier access???


Added swagger for easier api doc and validation
Added blueprints for easier path managemet
Added config to seperate out app run and config
Added SQL Alchemy ORM

# TODO:

1. Create an api layer to interact with the db. - insert a record, insert a dataframe?
2. Create the api to get screenshot using selenium