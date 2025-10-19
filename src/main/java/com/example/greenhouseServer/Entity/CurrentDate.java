package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;

@Entity
@Table(name = "current_state")
public class CurrentDate {

    @Id
    @ManyToOne
    @JoinColumn(name = "telegram_id", referencedColumnName = "telegram_id")
    private Users user;

    @Column(name = "token")
    private String token;

    @Column(name = "type")
    @Enumerated(EnumType.STRING)
    private TypeBool typeBool;

    @Column(name = "status")
    private Boolean isWorking;

    public CurrentDate() {
    }

    public CurrentDate(Users user, String token, TypeBool typeBool, Boolean isWorking) {
        this.user = user;
        this.token = token;
        this.typeBool = typeBool;
        this.isWorking = isWorking;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public TypeBool getTypeBool() {
        return typeBool;
    }

    public void setTypeBool(TypeBool typeBool) {
        this.typeBool = typeBool;
    }

    public Boolean getWorking() {
        return isWorking;
    }

    public void setWorking(Boolean working) {
        isWorking = working;
    }

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }
}
