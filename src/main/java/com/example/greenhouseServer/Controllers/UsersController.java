package com.example.greenhouseServer.Controllers;

import com.example.greenhouseServer.Service.Interfaces.UsersServiceIntr;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UsersController {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final UsersServiceIntr usersServiceIntr;

    @Autowired
    public UsersController(UsersServiceIntr usersServiceIntr) {
        this.usersServiceIntr = usersServiceIntr;
    }

    @PostMapping("/ipUsers")
    public ResponseEntity<?> parseIpAddress(@RequestBody String json){
        try {
            JsonNode rootNode = objectMapper.readTree(json);
            String token = rootNode.get("token").asText();
            String ipAddress = rootNode.get("ip_address").asText();

            if (token == null || ipAddress == null) {
                return ResponseEntity.badRequest()
                        .body("Missing required fields");
            }

            usersServiceIntr.update(token, ipAddress);
            return ResponseEntity.ok(HttpStatus.OK);
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body("Invalid JSON: " + e.getMessage());
        }
    }

}
