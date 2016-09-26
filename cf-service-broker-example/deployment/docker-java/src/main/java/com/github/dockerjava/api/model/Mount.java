package com.github.dockerjava.api.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Mount {

	@JsonProperty("Name")
	private String name;
	
	@JsonProperty("Source")
	private String source;
	
	@JsonProperty("Destination")
	private String destination;

	public String getName() {
		return name;
	}

	public String getSource() {
		return source;
	}

	public String getDestination() {
		return destination;
	}
	
	
}
