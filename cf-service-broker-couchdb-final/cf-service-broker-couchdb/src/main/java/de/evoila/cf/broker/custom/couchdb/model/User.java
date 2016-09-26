/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.model;

import java.util.List;

import org.ektorp.support.CouchDbDocument;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class User  extends CouchDbDocument{
	private static final long serialVersionUID = 1L;
	
	private String name;
	private String password;
	private List<String> roles;
	private String type;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public List<String> getRoles() {
		return roles;
	}

	public void setRoles(List<String> roles) {
		this.roles = roles;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}
}
