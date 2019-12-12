# CPSC449-Project
Project3-specification: https://docs.google.com/document/d/1W7tUT0LMe-fvmGY8d8TbdpE-XIStVdXS2ocA5_hdMj0/edit <br />
Github: https://github.com/DA01171997/XSPF-Music-Microservices-Cassandra-Edition  <br />
<b>Team Members</b><br />
Wellson Pan - WellsonPan@csu.fullerton.edu - Ops<br />
Liam Fitzpatrick - lfitzpatrick0@csu.fullerton.edu - Dev 2<br />
Duy Do - duy.ado@csu.fullerton.edu - Dev 1<br />

<b>Usage:<br /></b> 
&nbsp;&nbsp;if first run then:<br />
&nbsp;&nbsp;&nbsp;&nbsp;sudo kong start <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;./add_services.sh <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;sudo ./minio server /data  <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;./first_run (in seperate terminal, make sure scylla db is fully up before do this step or making requests.) <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;./curl_requests  (in seperate terminal, make sure scylla db is fully up before do this step or making requests.) <br />
&nbsp;&nbsp;else:<br />
&nbsp;&nbsp;&nbsp;&nbsp;foreman start <br />

<b>To configure kong:<br /></b>
&nbsp;&nbsp;sudo kong start
&nbsp;&nbsp;./add_services.sh

<b>To populate all microservices:<br /></b>
&nbsp;&nbsp;./curl_requests.sh

<b>To start MinIO bucket:<br /></b>
&nbsp;&nbsp;sudo ./minio server /data 

<b>Schema File:</b><br />
&nbsp;&nbsp;cql/init.cql<br />

<b>Notes:</b></br>
&nbsp;&nbsp;<b>./first_run</b> will also drop the Scylla keyspace if exists and recreate keyspace and tables. (Make sure Scylla is running)</br>
&nbsp;&nbsp;<b>source</b> XSPF generator code is taken from here: https://github.com/alastair/xspf</br>

&nbsp;&nbsp;<b>Fast simple way to test XSPF</b></br>
&nbsp;&nbsp;<b>1: After having all service running, run the ./curl_requests.sh. This will add the users, tracks, playlist, and descriptions metadata to Cassandra</b></br>
&nbsp;&nbsp;<b>2: Then upload a song to minio and name it song00.mp3 so that the url: http://localhost:8000/media/song00.mp3</b></br>
&nbsp;&nbsp;<b>3: Then use this url to test our Playlist 00: http://127.0.0.1:5400/api/v1/collections/playlists/Playlist%2000.xspf</b></br>


# ***IMPORTANT***: Please don't change the Procfile, and just run "foreman start" with all the standard 3 instances for the microservices, except xspfApi. Because kong wills still direct traffics to offline upstreams. Also please make sure Scylla is fully up and running before running curl_requests.sh script or try any requests. We also have issue when testing in Tuffix, and sometime we can't drop scylla keyspace or data correctly (check out dropkeyspace.PNG to see the issue). So if you tried to run signup for an existing users again, before Scylla drop the keyspace and tables, you will get a 409. If this happens just restart your VM, or drop the scylla docker image and container and reinstall the docker image. Lastly we assumed that the testing environment has all of the necessary packages specified in the Project 1-3 installed.