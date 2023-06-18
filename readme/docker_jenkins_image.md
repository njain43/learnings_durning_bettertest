# install jenkins on docker host


1) download Jenkins image 
    ```docker pull jenkins/jenkins ```
2) Once the image is downloaded, fire up the container with jenkins image
   ``` docker run -d -p 8080:8080 -v jenkins_home:/var/jenkins_home --name jenkins_container jenkins/jenkins ```
    1) desc of all parms.
      1.1) -d starts the container in detached mode.
      1.2) -p 8080:8080 maps port 8080 of the container to port 8080 of the host machine, allowing access to the Jenkins web interface.
      1.3) -v jenkins_home:/var/jenkins_home creates a named volume (jenkins_home) and mounts it to the container's /var/jenkins_home directory, which is where Jenkins stores its data.
         --name jenkins_container assigns the name "jenkins_container" to the running container.
