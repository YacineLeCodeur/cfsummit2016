#Getting started with the Cloudfoundry Service Broker Framework from evoila

To build a Service Broker for Cloud Foundry is not easy and normaly takes much time. With a common aproach and our well designed framework it is possible to do this in less time.

###A. The first step to use the servicebroker framework is to fork the projekt on github.

###B. After this checkout with git on your working device.

###C. When the repository is checked out on your device you have to customize some namings. For this step we have writen the following "renaming guide".

####Renaming Guide
change namings of project and shippables

The first step to use the servicebroker framework is to change namings of some folders, files and namings. To simplify this step in this description you find all folders, files and namings that must be changed.

1. Change folder names

2. ./pom.xml -> module servicebroker

3. ./cf-service-broker-couchdb/pom.xml

  i) artifact ld
  
  ii) name
  
4. manifest.yml

  i) name
  
  ii) host
  
  iii) path
  
5. ExampleServiceBindingService.java

6. ExampleServiceCustomPropertyHandler.java

7. application.yml

  i) application.name
  
  ii) info.app.name
  
  iii) logging.file
  
8. container.cmd

  i) example-template.sh 3x
  
9. openstack/template.yml

  i) description
  
  ii) example-template.sh 3x
  
10. service-definition.yml

  i) id
  
  ii) name
  
  iii) description
  
( iv) plans.id            )

(  v) plans.name          )

(  vi) plans.description  )
   
###D. Define a service and it's plans in the service_definition.yml

###E. Create deployment scripts for openstack (template.yaml) and/or docker (container.cmd)

###F. Add service specific dependencies to pom.xml

###G. Implement service specific code in <Example>ServiceBindingService.java

###H. Add missing property values in application.yml

###I. Add missing properties in ExampleServiceCustomPropertyHandler.java dependent on the properties used in your deployment scripts

###J. Service Broker is finished - build it with mvn install

###K. Complete your your manifest.yml and run cf push

###L. Register your Service Broker with the URL created by your manifest.yml with cf create-service-broker <ServiceBrokerName> admin cloudfoundry <URL>
