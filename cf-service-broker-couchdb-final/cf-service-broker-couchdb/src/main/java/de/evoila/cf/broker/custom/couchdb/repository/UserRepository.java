/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.repository;

import org.ektorp.CouchDbConnector;
import org.ektorp.support.CouchDbRepositorySupport;

import de.evoila.cf.broker.custom.couchdb.model.User;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class UserRepository extends CouchDbRepositorySupport<User> {

    public UserRepository(CouchDbConnector db) {
            super(User.class, db);
    }
}