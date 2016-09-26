/**
 * 
 */
package de.evoila.cf.broker.custom;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import de.evoila.cf.broker.exception.ServiceBrokerException;
import de.evoila.cf.broker.model.RouteBinding;
import de.evoila.cf.broker.model.ServerAddress;
import de.evoila.cf.broker.model.ServiceInstance;
import de.evoila.cf.broker.model.ServiceInstanceBinding;
import de.evoila.cf.broker.service.impl.BindingServiceImpl;

/**
 * @author Christian Brinker, evoila.
 *
 */
@Service
public class CouchDBServiceBindingService extends BindingServiceImpl {

	private Logger log = LoggerFactory.getLogger(getClass());

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * de.evoila.cf.broker.service.impl.BindingServiceImpl#createCredentials(
	 * java.lang.String, de.evoila.cf.broker.model.ServiceInstance,
	 * de.evoila.cf.broker.model.ServerAddress)
	 */
	@Override
	protected Map<String, Object> createCredentials(String bindingId, ServiceInstance serviceInstance,
			ServerAddress host) throws ServiceBrokerException {
		log.debug("bind Service");

		// Use service instance ID as user name and password (depends on
		// implementation of ;do not use in production).
		String adminUserName = serviceInstance.getId();
		String adminPassword = serviceInstance.getId();

		// The ID of Service Binding is used as database name in the CouchDB
		// instance.
		String databaseName = bindingId;
		String userName = bindingId;
		String password = bindingId;

		Map<String, Object> credentials = new HashMap<String, Object>();
		credentials.put("uri", "http://" + userName + ":" + password + "@" + host.getIp() + ":" + host.getPort());

		return credentials;
	}

	@Override
	protected void deleteBinding(String bindingId, ServiceInstance serviceInstance) throws ServiceBrokerException {
		log.debug("unbind Service");

		// Use service instance ID as user name and password (depends on
		// implementation of ;do not use in production).
		String adminUserName = serviceInstance.getId();
		String adminPassword = serviceInstance.getId();

		// The ID of Service Binding is used as database name in the CouchDB
		// instance.
		String databaseName = bindingId;
		String userName = bindingId;

		ServerAddress host = serviceInstance.getHosts().get(0);
	}

	@Override
	public ServiceInstanceBinding getServiceInstanceBinding(String id) {
		throw new UnsupportedOperationException();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * de.evoila.cf.broker.service.impl.BindingServiceImpl#bindRoute(de.evoila.
	 * cf.broker.model.ServiceInstance, java.lang.String)
	 */
	@Override
	protected RouteBinding bindRoute(ServiceInstance serviceInstance, String route) {
		throw new UnsupportedOperationException();
	}

	

}
