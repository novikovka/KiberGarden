package com.example.greenhouseServer.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "users")
public class Users {

    @Id
    @Column(name = "telegram_id")
    private Long id;

    @Column(name = "token")
    private String token;

    @Column(name = "ip_address")
    private String ipAddress;

    @Column(name = "name")
    private String nameTgUser;

    @Column(name = "plant_name")
    private String plantName;

    public Users() {
    }

    public Users(Long id, String token, String ipAddress, String nameTgUser, String plantName) {
        this.id = id;
        this.token = token;
        this.ipAddress = ipAddress;
        this.nameTgUser = nameTgUser;
        this.plantName = plantName;
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

    public String getNameTgUser() {
        return nameTgUser;
    }

    public void setNameTgUser(String nameTgUser) {
        this.nameTgUser = nameTgUser;
    }

    public String getPlantName() {
        return plantName;
    }

    public void setPlantName(String plantName) {
        this.plantName = plantName;
    }
}
