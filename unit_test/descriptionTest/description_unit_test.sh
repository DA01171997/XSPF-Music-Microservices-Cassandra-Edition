echo "POSITIVE CASE: insert user description"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--request POST \
	--header 'Content-Type: application/json' \
	--data @add_description_unit_test.json \
	http://127.0.0.1:8000/api/v1/descriptions/
echo
echo


echo "POSITIVE CASE: GET description by username of song via trackMedia"
echo "----------------------------------------------------------------------------------"
curl --verbose \
	--header 'Content-Type: application/json' \
	--request GET \
	http://127.0.0.1:8000/api/v1/descriptions/users/WassupMan404/descriptions?trackMediaURL=http://localhost:8000/media/song00.mp3
echo
echo
echo
