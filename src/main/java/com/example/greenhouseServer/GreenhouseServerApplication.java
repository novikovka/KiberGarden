package com.example.greenhouseServer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class GreenhouseServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(GreenhouseServerApplication.class, args);
	}

}
