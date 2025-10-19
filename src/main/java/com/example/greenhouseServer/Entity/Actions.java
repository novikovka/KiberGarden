package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name = "actions")
public class Actions {

    @Id
    @ManyToOne
    @JoinColumn(name = "telegram_id", referencedColumnName = "telegram_id")
    private Users user;

    @Column(name = "token")
    private String token;

    @Enumerated(EnumType.STRING)
    @Column(name = "type")
    private TypeBool typeBool;

    @Column(name = "time")
    private LocalTime timeAction;

    @Column(name = "status")
    private Boolean isWorking;

    public Actions() {
    }

    public Actions(Users user, String token, TypeBool typeBool, LocalTime timeAction, Boolean isWorking) {
        this.user = user;
        this.token = token;
        this.typeBool = typeBool;
        this.timeAction = timeAction;
        this.isWorking = isWorking;
    }

    public Boolean getWorking() {
        return isWorking;
    }

    public void setWorking(Boolean working) {
        isWorking = working;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }

    public TypeBool getTypeBool() {
        return typeBool;
    }

    public void setTypeBool(TypeBool typeBool) {
        this.typeBool = typeBool;
    }

    public LocalTime getTimeAction() {
        return timeAction;
    }

    public void setTimeAction(LocalTime timeAction) {
        this.timeAction = timeAction;
    }
}
