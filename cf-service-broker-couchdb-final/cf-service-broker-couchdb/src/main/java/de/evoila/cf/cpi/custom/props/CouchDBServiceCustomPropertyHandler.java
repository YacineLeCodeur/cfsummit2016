/**
 * 
 */
package de.evoila.cf.cpi.custom.props;

import java.util.Map;

import de.evoila.cf.broker.model.Plan;
import de.evoila.cf.broker.model.ServiceInstance;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class CouchDBServiceCustomPropertyHandler extends DefaultDatabaseCustomPropertyHandler {

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * de.evoila.cf.cpi.openstack.custom.props.DomainBasedCustomPropertyHandler#
	 * addDomainBasedCustomProperties(de.evoila.cf.broker.model.Plan,
	 * java.util.Map, java.lang.String)
	 */
	@Override
	public Map<String, String> addDomainBasedCustomProperties(Plan plan, Map<String, String> customProperties,
			ServiceInstance serviceInstance) {
		customProperties = super.addDomainBasedCustomProperties(plan, customProperties, serviceInstance);
		
		customProperties.remove("database_name");
		
		customProperties.put("log_host", "127.0.0.1");
		customProperties.put("log_port", "1234");
		customProperties.put("log_protocol", "tcp");
		
		return customProperties;
	}
}
