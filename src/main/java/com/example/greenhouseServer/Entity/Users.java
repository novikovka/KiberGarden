package com.example.greenhouseServer.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "users_tbl")
public class Users {

    @Id
    @Column(name = "id_tg_user")
    private Long id;

    @Column(name = "id_token_greenhouse")
    private String token;

    @Column(name = "ip_greenhouse")
    private String ipAddress;

    public Users() {
    }

    public Users(Long id, String token, String ipAddress) {
        this.id = id;
        this.token = token;
        this.ipAddress = ipAddress;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
}
