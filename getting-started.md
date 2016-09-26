#Getting started with the Cloudfoundry Service Broker Framework from evoila

To build a Service Broker for Cloud Foundry is not easy and normaly takes much time. With a common aproach and our well designed framework it is possible to do this in less time.

**1. The first step to use the servicebroker framework is to fork the projekt on github.**

**2. After this checkout with git on your working device.**

**3. When the repository is checked out on your device you have to customize some namings. For this step we have writen the following "renaming guide".**

###Renaming Guide
change namings of project and shippables

The first step to use the servicebroker framework is to change namings of some folders, files and namings. To simplify this step in this description you find all folders, files and namings that must be changed.

3.1. Change folder names

3.2. ./pom.xml -> module servicebroker

3.3 ./cf-service-broker-couchdb/pom.xml
  3.3.1. artifact ld
  3.3.2. name
  
d) manifest.yml

  i) name
  
  ii) host
  
  iii) path
  
e) ExampleServiceBindingService.java

f) ExampleServiceCustomPropertyHandler.java

g) application.yml

  i) application.name
  
  ii) info.app.name
  
  iii) logging.file
  
h) container.cmd

  i) example-template.sh 3x
  
j) openstack/template.yml

  i) description
  
  ii) example-template.sh 3x
  
k) service-definition.yml

  i) id
  
  ii) name
  
  iii) description
  
( iv) plans.id            )

(  v) plans.name          )

(  vi) plans.description  )
   
**4. Define a service and it's plans in the service_definition.yml**

**5. Create deployment scripts for openstack (template.yaml) and/or docker (container.cmd)**

**6. Add service specific dependencies to pom.xml**

**7. Implement service specific code in <Example>ServiceBindingService.java**

**8. Add missing property values in application.yml**

**9. Add missing properties in ExampleServiceCustomPropertyHandler.java dependent on the properties used in your deployment scripts**

**10. Service Broker is finished - build it with mvn install**

**11. Complete your your manifest.yml and run cf push**

**12. Register your Service Broker with the URL created by your manifest.yml with cf create-service-broker <ServiceBrokerName> admin cloudfoundry <URL>**
