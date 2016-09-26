/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.util;

import org.ektorp.CouchDbConnector;
import org.ektorp.CouchDbInstance;
import org.ektorp.http.HttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;

import de.evoila.cf.broker.custom.couchdb.model.DatabaseSecurity;
import de.evoila.cf.broker.custom.couchdb.model.User;
import de.evoila.cf.broker.custom.couchdb.repository.UserRepository;
import de.evoila.cf.broker.model.ServerAddress;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class CouchDBConnectionHandler {
	public static void createUser(String userName, String password, CouchDbInstance dbInstance) {
		CouchDbConnector userDatabase = new StdCouchDbConnector("_user", dbInstance);
		userDatabase.createDatabaseIfNotExists();
		UserRepository userRepository = new UserRepository(userDatabase);
	
		User user = new User();
		user.setId("org.couchdb.user:" + userName);
		user.setName(userName);
		user.setPassword(password);
		user.setType("user");
	
		userRepository.add(user);
		userDatabase.ensureFullCommit();
	}

	public static void addUserToDatabase(String userName, CouchDbConnector newDatabase) {
		DatabaseSecurity securityDefinition = newDatabase.find(DatabaseSecurity.class, "_security");
		boolean securityDefinitionIsNew = false;
		if (securityDefinition == null) {
			securityDefinition = new DatabaseSecurity();
			securityDefinitionIsNew = true;
		}
		securityDefinition.getMembers().getNames().add(userName);

		if (securityDefinitionIsNew) {
			newDatabase.create("_security", securityDefinition);
		} else {
			newDatabase.update(securityDefinition);
		}
		newDatabase.ensureFullCommit();
	}

	public static void removeUserFromDatabase(String userName, CouchDbConnector database) {
		DatabaseSecurity securityDefinition = database.find(DatabaseSecurity.class, "_security");
		if (securityDefinition != null) {
			securityDefinition.getMembers().getNames().remove(userName);
			database.update(securityDefinition);
			database.ensureFullCommit();
		}
	}

	public static CouchDbInstance connectToCouchDBInstance(String adminUserName, String adminPassword, ServerAddress host) {
		HttpClient httpClient = new CouchDBConnectionBuilder().host(host.getIp()).port(host.getPort())
				.username(adminUserName).password(adminPassword).build();

		CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);
		return dbInstance;
	}

	public static CouchDbConnector connectToDatabase(String databaseName, CouchDbInstance dbInstance) {
		CouchDbConnector newDatabase = new StdCouchDbConnector(databaseName, dbInstance);
		return newDatabase;
	}
}
