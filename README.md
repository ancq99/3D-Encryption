# 3D Encryption

In this project we fill a 3D space with points, so that from one particular angle, position and FOV the encrypted image is seen. Of course that is just the visual representation of what the programme is doing.

###### How the encryption works.

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Rotation_view_example.gif?raw=true)

###### Image of letter "H". I appears as shifted because we are projecting a square image to a circle. 

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Picture_view_example.png?raw=true)

# Black box

From GUI the user can select options regarding encryption space, noise, and selecting files to encrypt. It takes in binary image saved as '0' and '1'. It operates on very small images: 50x50 pix takes around a minute to decrypt.

###### Binary image.

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Image_coded.png?raw=true)

###### Interpretation of the binary image - Before and after converting.

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Image.png?raw=true) ![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Shifted_Image.png?raw=true)

Because of the way our programme works, we need to cast rays out of the point in the shape of the cone.
To do that we need to convert square image into an even, circular one.

###### Image spray. 
![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Spray.png?raw=true)

# Density and holes

In order for this programme to work, we need to find a location for our "eye". Once we find it, we cast rays on which we place randomly points that represent pixels (or 'ones' in binary file).

Because of that, if we were to place the "eye near the edge some rays would be much shorter than other, resulting in higher density in that area. Ideally we would put the cone (our image in 3D space is seen as a cone) perpendicularly to the side of the box, this way there would be no unnecessary distortions.

After we create the cone, we calculate based on density number of points we create around. An additional option is creating noise, simply adding some number of points to our space.

###### Visual interpretation of the encrypted file.
###### Red - The image 
###### Blue - Non informational data created during encryption. 

###### (Obviously this is just a set of points as seen from outside the programme.)

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/Result.png?raw=true)

# Decryption

When it comes to decrypting the file, after entering the key programme creates the same rays as before, and checks for collisions with our "dots". When it hits a point, a correct square on resulting image is painted black (or more percisely with a "1").

###### Here is the interpretation of what the programme sees during the decryption

![alt text](https://github.com/M2etroline/ProjectBase/blob/master/decryption_view.jpg?raw=true)

# Summary

This project is not at all comparable to newer (and old) techniques of encryption. It is an educational experiment, a presentation of what encrypting data, and using a key means. But all in all, it was just a fun idea that we wanted to implement.
 
###### Co-Authors 
https://github.com/M2etroline

https://github.com/kon4770

https://github.com/SuchodolskijEdvin

https://github.com/krzsza1
