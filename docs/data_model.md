# Listing elements
(Avni,Reza)
Key items present on the listings page
- Name 'Queenie'
- Photo 
- Age '12 years and 7 months'
- Location
- Icons - Boolean values
    - Can live with other cats
    - Can live with dogs
    - Garden required
    - Can live with children
    
# Profile elements
(Anna/Marya)
Detailed view of each animal.
All of the above plus:
- Breed 'Domestic Short-hair'
- Size
- Reference number
- Textual description
- Special needs/conditions.
- .......

# Two Tables (Many-to-Many) Design Recipe Template

_Copy this recipe template to design and create two related database tables having a Many-to-Many relationship._

## 1. Extract nouns from the user stories or specification

```
# EXAMPLE USER STORIES:

####################
As a blogger,
So I can organise my blog posts,
I want to keep a list of posts with their title and content.

As a blogger,
So I can organise my blog posts,
I want to keep a list of tags with their name (e.g 'coding' or 'travel').

As a blogger,
So I can organise my blog posts,
I want to be able to assign one tag to different posts.

As a blogger,
So I can organise my blog posts,
I want to be able to tag one post with one or different many tags.
####################

As a shelter,
I want to create an advert for an animal available to adopt in my shelter

As a shelter,
I want to display the details of the animal [name, age, breed species, location, gender, neutered, lives with children]

As a shelter,
I want to display a bio for each animal

As a shelter,
I want to upload images of each animal

As a shelter, 
I want to pick a profile picture for each animal

As a shelter, 
I want to display a list of animals available from my shelter

As a shelter,
So only available animals are shown,
I want to be able to 'deactivate' animals that have been adopted

As a shelter,
I should be able to edit details of animals belonging to my shelter

As a shelter, 
I should be able to remove images from an advert

As a shelter,
I want to be contacted by a user if there is interest in one of our animals

As a shelter,
Members of our shelter should be able to sign up with their email address

As a shelter,
For security
Only email addresses with our domain should be able to register as a member of our shelter

As a user,
I should be able to sign up with my email address

As a user,
I should be able to view a list of animals available for adoption from all shelters

As a user, 
So I can register interest,
I should be able to contact the shelter about an animal

As a user,
I should be able to save my favourite animals

As a shelter, 
I want to see all messages sent to our shelter, about all of our animals

As a user, 
I should be able to see my messages from other users

As a user, 
I should be able to reply to a message

As a user, 
I should be able to see the message history in a conversation

As a user, 
I should be able to distinguish my opened messages from my unopened messages


```

```
Nouns:

shelter, user, animal, name, species, location, gender, neutered, images, advert, messages, email, member, domain, age, bio, active, conversation, 
```

## 2. Infer the Table Name and Columns

Put the different nouns in this table. Replace the example with your own nouns.

| Record                | Properties          |
| --------------------- | ------------------  |
| animals                 | name, species, location, gender, neutered, age, breed, lives_with_children, bio, active , profile_image, shelter_id,
| shelters                  | name, location, email, phone_number, domain
| users                  | first_name, last_name, email, password, shelter_id
| messages                  | sent_time, read_time, conversation, animal_id, shelter_id, recipient_id, sender_id, private

1. Name of the first table (always plural): `animals` 

    Column names: `name`, `species`, `location`, `male`, `neutered`, `age`, `breed`, `lives_with_children`, `bio`, `active` , `profile_image`, `shelter_id`

2. Name of the second table (always plural): `shelters` 

    Column names: `name`, `location`, `email`, `phone_number`, `domain`

3. Name of the third table (always plural): `users` 

    Column names: `first_name`, `last_name`, `email`, `password`, `shelter_id`

4. Name of the fourth table (always plural): `messages` 

    Column names: `sent_time`, `read_time`, `conversation`, `animal_id`, `shelter_id`, `recipient_id`, `sender_id`, `private`

## 3. Decide the column types.

[Here's a full documentation of PostgreSQL data types](https://www.postgresql.org/docs/current/datatype.html).

Most of the time, you'll need either `text`, `int`, `bigint`, `numeric`, or `boolean`. If you're in doubt, do some research or ask your peers.

Remember to **always** have the primary key `id` as a first column. Its type will always be `SERIAL`.

```
# EXAMPLE:

Table: posts
id: SERIAL
title: text
content: text

Table: tags
id: SERIAL
name: text

Table: animals
id: SERIAL
name: TEXT
species: TEXT
location: TEXT
male: BOOLEAN
neutered: BOOLEAN
age: INT
breed: TEXT

Table: shelters
id: SERIAL
name: TEXT
location: TEXT
email: TEXT
phone_number: INT
domain: TEXT

table: users
id: SERIAL
first_name: TEXT
last_name: TEXT
email: VARCHAR
password: VARCHAR
shelter_id: INT

table: messages
id: SERIAL
sent_time: DATE
read_time: DATE
conversation: UUID
private: BOOLEAN
animal_id: UUID
shelter_id: INT
recipient_id: INT
sender_id: INT
```

## 4. Design the Many-to-Many relationship

Make sure you can answer YES to these two questions:

1. Can animals have many shelters? NO
2. Can shelters have many animals? YES
3. Can shelters have many users? YES
4. Can users have many messages? YES
5. can messages have many users? YES?


_If you would answer "No" to one of these questions, you'll probably have to implement a One-to-Many relationship, which is simpler. Use the relevant design recipe in that case._

## 5. Design the Join Table

The join table usually contains two columns, which are two foreign keys, each one linking to a record in the two other tables.

The naming convention is `table1_table2`.

```
# EXAMPLE

Join table for tables: posts and tags
Join table name: posts_tags
Columns: post_id, tag_id
```

## 6. Write the SQL.

```sql
-- EXAMPLE
-- file: posts_tags.sql

-- Replace the table name, columm names and types.

-- Create the first table.
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title text,
  content text
);

-- Create the second table.
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name text
);

-- Create the join table.
CREATE TABLE posts_tags (
  post_id int,
  tag_id int,
  constraint fk_post foreign key(post_id) references posts(id) on delete cascade,
  constraint fk_tag foreign key(tag_id) references tags(id) on delete cascade,
  PRIMARY KEY (post_id, tag_id)
);

```

## 7. Create the tables.

```bash
psql -h 127.0.0.1 database_name < posts_tags.sql
```