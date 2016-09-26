/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.model;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class Members {
	private List<String> names = new ArrayList<String>();
	private List<String> roles = new ArrayList<String>();

	public List<String> getNames() {
		return names;
	}

	public void setNames(List<String> names) {
		this.names = names;
	}

	public List<String> getRoles() {
		return roles;
	}

	public void setRoles(List<String> roles) {
		this.roles = roles;
	}
}
