# CPSC449-Project
project3-specification: https://docs.google.com/document/d/1W7tUT0LMe-fvmGY8d8TbdpE-XIStVdXS2ocA5_hdMj0/edit <br />
<b>Team Members</b><br />
Wellson Pan - WellsonPan@csu.fullerton.edu - Ops<br />
Liam Fitzpatrick - lfitzpatrick0@csu.fullerton.edu - Dev 2<br />
Duy Do - duy.ado@csu.fullerton.edu - Dev 1<br />

<b>Usage:<br /></b> 
&nbsp;&nbsp;if first run then:<br />
&nbsp;&nbsp;&nbsp;&nbsp;./first_run <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;./curl_requests <br />
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
&nbsp;&nbsp;<b>./first_run</b> will install pip3 so it asks for sudo. It then installs the packages in requirements.txt.
&nbsp;&nbsp;<b>./first_run</b> will also drop the Scylla keyspace if exists and recreate keyspace and tables. (Make sure Scylla is running)
&nbsp;&nbsp;<b>source</b> XSPF generator code is taken from here: https://github.com/alastair/xspf

&nbsp;&nbsp;<b>Fast simple way to test XSPF</b>
&nbsp;&nbsp;<b>1: After having all service running, run the ./curl_requests.sh. This will add the users, tracks, playlist, and descriptions metadata to Cassandra</b>
&nbsp;&nbsp;<b>2: Then upload a song to minio and name it song00.mp3 so that the url: http://localhost:8000/media/song00.mp3</b>
&nbsp;&nbsp;<b>3: Then use this url to test our Playlist 00: http://127.0.0.1:5400/api/v1/collections/playlists/Playlist%2000.xspf</b>


# ***IMPORTANT***: Please keep foreman running with all the standard 3 instances for the microservices, except xspfApi. Because kong wills still direct traffics to offline instances.