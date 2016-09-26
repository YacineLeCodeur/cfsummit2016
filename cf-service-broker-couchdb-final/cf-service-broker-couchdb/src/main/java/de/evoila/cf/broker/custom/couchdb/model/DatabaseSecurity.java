/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.model;

import org.ektorp.support.CouchDbDocument;

/**
 * @author Christian
 *
 */
public class DatabaseSecurity extends CouchDbDocument {
	private static final long serialVersionUID = 1L;
	
	private Admins admins = new Admins();
	
	private Members members = new Members();

	public Admins getAdmins() {
		return admins;
	}

	public void setAdmins(Admins admins) {
		this.admins = admins;
	}

	public Members getMembers() {
		return members;
	}

	public void setMembers(Members members) {
		this.members = members;
	}
	
}
