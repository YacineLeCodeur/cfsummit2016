/**
 * 
 */
package de.evoila.cf.broker.custom.couchdb.util;

import java.net.MalformedURLException;
import java.net.URL;

import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.params.ClientPNames;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.params.ConnRoutePNames;
import org.apache.http.conn.scheme.PlainSocketFactory;
import org.apache.http.conn.scheme.Scheme;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.http.impl.client.DecompressingHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.PoolingClientConnectionManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.ektorp.http.HttpClient;
import org.ektorp.http.IdleConnectionMonitor;
import org.ektorp.http.PreemptiveAuthRequestInterceptor;
import org.ektorp.http.StdHttpClient;
import org.ektorp.http.StdHttpClient.WithCachingBuilder;
import org.ektorp.util.Exceptions;

/**
 * @author Christian Brinker, evoila.
 *
 */
public class CouchDBConnectionBuilder {
	protected String host = "localhost";
	protected int port = 5984;
	protected int maxConnections = 20;
	protected int connectionTimeout = 1000;
	protected int socketTimeout = 10000;
	protected ClientConnectionManager conman;
	protected int proxyPort = -1;
	protected String proxy = null;

	protected boolean enableSSL = false;
	protected boolean relaxedSSLSettings = false;
	protected SSLSocketFactory sslSocketFactory;

	protected String username;
	protected String password;

	protected boolean cleanupIdleConnections = true;
	protected boolean useExpectContinue = true;
	protected boolean caching = true;
	protected boolean compression; // Default is false;
	protected int maxObjectSizeBytes = 8192;
	protected int maxCacheEntries = 1000;

	public CouchDBConnectionBuilder url(String s) throws MalformedURLException {
		if (s == null)
			return this;
		return this.url(new URL(s));
	}

	/**
	 * Will set host, port and possible enables SSL based on the properties if
	 * the supplied URL. This method overrides the properties: host, port and
	 * enableSSL.
	 * 
	 * @param url
	 * @return
	 */
	public CouchDBConnectionBuilder url(URL url) {
		this.host = url.getHost();
		this.port = url.getPort();
		if (url.getUserInfo() != null) {
			String[] userInfoParts = url.getUserInfo().split(":");
			if (userInfoParts.length == 2) {
				this.username = userInfoParts[0];
				this.password = userInfoParts[1];
			}
		}
		enableSSL("https".equals(url.getProtocol()));
		if (this.port == -1) {
			if (this.enableSSL) {
				this.port = 443;
			} else {
				this.port = 80;
			}
		}
		return this;
	}

	public CouchDBConnectionBuilder host(String s) {
		host = s;
		return this;
	}

	public CouchDBConnectionBuilder proxyPort(int p) {
		proxyPort = p;
		return this;
	}

	public CouchDBConnectionBuilder proxy(String s) {
		proxy = s;
		return this;
	}

	/**
	 * Controls if the http client should send Accept-Encoding: gzip,deflate
	 * header and handle Content-Encoding responses. This enable compression on
	 * the server; although not supported natively by CouchDB, you can use a
	 * reverse proxy, such as nginx, in front of CouchDB to achieve this.
	 * <p>
	 * Disabled by default (for backward compatibility).
	 * 
	 * @param b
	 * @return This builder
	 */
	public CouchDBConnectionBuilder compression(boolean b) {
		compression = b;
		return this;
	}

	/**
	 * Controls if the http client should cache response entities. Default is
	 * true.
	 * 
	 * @param b
	 * @return
	 */
	public CouchDBConnectionBuilder caching(boolean b) {
		caching = b;
		return this;
	}

	public CouchDBConnectionBuilder maxCacheEntries(int m) {
		maxCacheEntries = m;
		return this;
	}

	public CouchDBConnectionBuilder maxObjectSizeBytes(int m) {
		maxObjectSizeBytes = m;
		return this;
	}

	public ClientConnectionManager configureConnectionManager(HttpParams params) {
		if (conman == null) {
			SchemeRegistry schemeRegistry = new SchemeRegistry();
			schemeRegistry.register(configureScheme());

			PoolingClientConnectionManager cm = new PoolingClientConnectionManager(schemeRegistry);
			cm.setMaxTotal(maxConnections);
			cm.setDefaultMaxPerRoute(maxConnections);
			conman = cm;
		}

		if (cleanupIdleConnections) {
			IdleConnectionMonitor.monitor(conman);
		}
		return conman;
	}

	protected Scheme configureScheme() {
		if (enableSSL) {
			try {
				if (sslSocketFactory == null) {
					SSLContext context = SSLContext.getInstance("TLS");

					if (relaxedSSLSettings) {
						context.init(null, new TrustManager[] { new X509TrustManager() {
							public java.security.cert.X509Certificate[] getAcceptedIssuers() {
								return null;
							}

							public void checkClientTrusted(java.security.cert.X509Certificate[] certs,
									String authType) {
							}

							public void checkServerTrusted(java.security.cert.X509Certificate[] certs,
									String authType) {
							}
						} }, null);
					} else {
						context.init(null, null, null);
					}

					sslSocketFactory = relaxedSSLSettings
							? new SSLSocketFactory(context, SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER)
							: new SSLSocketFactory(context);

				}
				return new Scheme("https", port, sslSocketFactory);
			} catch (Exception e) {
				throw Exceptions.propagate(e);
			}
		} else {
			return new Scheme("http", port, PlainSocketFactory.getSocketFactory());
		}
	}

	public org.apache.http.client.HttpClient configureClient() {
		HttpParams params = new BasicHttpParams();
		HttpProtocolParams.setUseExpectContinue(params, useExpectContinue);
		HttpConnectionParams.setConnectionTimeout(params, connectionTimeout);
		HttpConnectionParams.setSoTimeout(params, socketTimeout);
		HttpConnectionParams.setTcpNoDelay(params, Boolean.TRUE);

		String protocol = "http";

		if (enableSSL)
			protocol = "https";

		params.setParameter(ClientPNames.DEFAULT_HOST, new HttpHost(host, port, protocol));
		if (proxy != null) {
			params.setParameter(ConnRoutePNames.DEFAULT_PROXY, new HttpHost(proxy, proxyPort, protocol));
		}
		ClientConnectionManager connectionManager = configureConnectionManager(params);
		DefaultHttpClient client = new DefaultHttpClient(connectionManager, params);
		if (username != null && password != null) {
			client.getCredentialsProvider().setCredentials(new AuthScope(host, port, AuthScope.ANY_REALM),
					new UsernamePasswordCredentials(username, password));
			client.addRequestInterceptor(new PreemptiveAuthRequestInterceptor(), 0);
		}

		if (compression) {
			return new DecompressingHttpClient(client);
		}
		return client;
	}

	public CouchDBConnectionBuilder port(int i) {
		port = i;
		return this;
	}

	public CouchDBConnectionBuilder username(String s) {
		username = s;
		return this;
	}

	public CouchDBConnectionBuilder password(String s) {
		password = s;
		return this;
	}

	public CouchDBConnectionBuilder maxConnections(int i) {
		maxConnections = i;
		return this;
	}

	public CouchDBConnectionBuilder connectionTimeout(int i) {
		connectionTimeout = i;
		return this;
	}

	public CouchDBConnectionBuilder socketTimeout(int i) {
		socketTimeout = i;
		return this;
	}

	/**
	 * If set to true, a monitor thread will be started that cleans up idle
	 * connections every 30 seconds.
	 * 
	 * @param b
	 * @return
	 */
	public CouchDBConnectionBuilder cleanupIdleConnections(boolean b) {
		cleanupIdleConnections = b;
		return this;
	}

	/**
	 * Bring your own Connection Manager. If this parameters is set, the
	 * parameters port, maxConnections, connectionTimeout and socketTimeout are
	 * ignored.
	 * 
	 * @param cm
	 * @return
	 */
	public CouchDBConnectionBuilder connectionManager(ClientConnectionManager cm) {
		conman = cm;
		return this;
	}

	/**
	 * Set to true in order to enable SSL sockets. Note that the CouchDB host
	 * must be accessible through a https:// path Default is false.
	 * 
	 * @param s
	 * @return
	 */
	public CouchDBConnectionBuilder enableSSL(boolean b) {
		enableSSL = b;
		return this;
	}

	/**
	 * Bring your own SSLSocketFactory. Note that schemeName must be also be
	 * configured to "https". Will override any setting of relaxedSSLSettings.
	 * 
	 * @param f
	 * @return
	 */
	public CouchDBConnectionBuilder sslSocketFactory(SSLSocketFactory f) {
		sslSocketFactory = f;
		return this;
	}

	/**
	 * If set to true all SSL certificates and hosts will be trusted. This might
	 * be handy during development. default is false.
	 * 
	 * @param b
	 * @return
	 */
	public CouchDBConnectionBuilder relaxedSSLSettings(boolean b) {
		relaxedSSLSettings = b;
		return this;
	}

	/**
	 * Activates 'Expect: 100-Continue' handshake with CouchDB. Using expect
	 * continue can reduce stale connection problems for PUT / POST operations.
	 * body. Enabled by default.
	 * 
	 * @param b
	 * @return
	 */
	public CouchDBConnectionBuilder useExpectContinue(boolean b) {
		useExpectContinue = b;
		return this;
	}

	public HttpClient build() {
		org.apache.http.client.HttpClient client = configureClient();
		org.apache.http.client.HttpClient cachingHttpClient = client;

		if (caching) {
			cachingHttpClient = WithCachingBuilder.withCaching(client, maxCacheEntries, maxObjectSizeBytes);
		}
		return new StdHttpClient(cachingHttpClient, client);
	}

}
