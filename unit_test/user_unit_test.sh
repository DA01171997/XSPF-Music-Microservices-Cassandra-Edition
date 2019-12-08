#!/bin/bash

echo "POSITIVE CASE: insert user"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_new_user.json \
	http://127.0.0.1:8000/api/v1/users/register
echo
echo
echo

echo "POSITIVE CASE: insert user"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_new_user2.json \
	http://127.0.0.1:8000/api/v1/users/register
echo
echo
echo

echo "NEGATIVE CASE: insert user - duplicate user"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_new_user.json \
	http://127.0.0.1:8000/api/v1/users/register
echo
echo
echo

echo "TESTING CASE: show all user"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/register
echo
echo
echo

echo "POSITIVE CASE: GET user by id"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/id/1
echo
echo
echo

echo "POSITIVE CASE: GET user by id"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/id/2
echo
echo
echo

echo "NEGATIVE CASE: GET user by id - invalid id"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/id/100
echo
echo
echo

echo "POSITIVE CASE: DELETE user by id "
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request DELETE \
	http://127.0.0.1:8000/api/v1/users/id/2
echo
echo
echo

echo "TESTING CASE: show all user"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/register
echo
echo
echo
echo "----------------------------------------------------------------------------------"

echo "NEGATIVE CASE: DELETE user by id -  id no longer valid "
curl --verbose \
	--header 'Content-Type: application/json' \
	--request DELETE \
	http://127.0.0.1:8000/api/v1/users/id/2
echo
echo
echo


echo "POSITIVE CASE: GET user by username"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/users/unitTestUser
echo
echo
echo

echo "POSITIVE CASE: Login"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_login.json \
	http://127.0.0.1:8000/api/v1/users/login
echo
echo
echo

echo "NEGATIVE CASE: Login - wrong password"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_login2.json \
	http://127.0.0.1:8000/api/v1/users/login
echo
echo
echo
echo "----------------------------------------------------------------------------------"

echo "POSITIVE CASE: Update password"
curl --verbose \
	--request PATCH \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_update_password.json \
	http://127.0.0.1:8000/api/v1/users/unitTestUser/password
echo
echo
echo

echo "POSITIVE CASE: Login"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_login2.json \
	http://127.0.0.1:8000/api/v1/users/login
echo
echo
echo

echo "NEGATIVE CASE: Login - wrong password"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_login.json \
	http://127.0.0.1:8000/api/v1/users/login
echo
echo
echo

echo "NEGATIVE CASE: Update password - user doesn't exist"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request PATCH \
	--header 'Content-Type: application/json' \
	--data @../json/unit_test_user_update_password2.json \
	http://127.0.0.1:8000/api/v1/users/WassupMan4daffaf04/password
echo
echo
echo
echo "----------------------------------------------------------------------------------"