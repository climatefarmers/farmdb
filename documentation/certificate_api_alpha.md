# Alpha version of how our certificate endpoint could look like

This describes a really rough brain storming idea of how the api representation 
of our certificate could look like. This is really really early on and this should 
really be seen as a rough collection of ideas.

## URL schema
```
url: /certs/<hash>
```

The ```<hash>``` url key is a hash over all the values we describe in the 
certificate.  This enables us to guarantee that we can not modify the values 
once we have shared the hash.

For now we will be returning in the json format.

## Values represented

* Methodology used : link and hash to a document in which we describe the 
  methodologies we use. 
* Technical manual: link and hash to the current version of the technical manual 
  which describes how the system is set up.
* Pipeline setup: This is a data structure which describes the various 
  calculations we used to come to the stated results. This is a json structure 
  representing the setup of the docker containers. 
** Will include in what configuration we used the various algorithms
** Will include a hash of every algorithm we use (docker container hash)

* Source data: Link and hash of all the source data we used with the pipeline
* Result data of all the external services we used. As we will be querying 
  loads of different services we need to save what these returned. 

* Reference to the hardware we used. Initially a string with aws, google or similar
* Date of when the certificate was created
* Link and hash to shapefiles for the fields we created the certificate for
* Size of all the fields in ha
* List of various scenarios we have calculated. This will include how we model
  the development of the various indicators. Initially for every month. We still
  need to decide if we do this for every hectare/ field or some other resolution.
  This will include a multitude of scenarios as we need to factor in climate 
  change, possible droughts and rain. 
* List of values we see as most likely to accrue. Again values for every month
  and then we need to see for what resolution





