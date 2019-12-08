-- :name create_user :insert
INSERT INTO users(userName, userUserName, userEmail, userPassword)
VALUES(:userName, :userUserName, :userEmail, :userPassword)