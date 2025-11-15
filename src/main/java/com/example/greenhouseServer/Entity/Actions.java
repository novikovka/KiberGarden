package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.time.LocalTime;

@Entity
@Table(name = "actions")
public class Actions {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_actions")
    private Long idActions;

    @JoinColumn(name = "token", referencedColumnName = "token")
    @NotEmpty(message = "token do not empty")
    @Size(min = 1, max = 30, message = "Size token is error")
    private String token;

    @Enumerated(EnumType.STRING)
    @Column(name = "type")
    @NotEmpty(message = "type do not empty")
    private TypeBool typeBool;

    @Column(name = "time")
    @NotEmpty(message = "time do not empty")
    private LocalTime timeAction;

    @Column(name = "status")
    @NotEmpty(message = "bool working do not empty")
    private Boolean isWorking;

    public Actions() {
    }

    public Actions(String token, TypeBool typeBool, LocalTime timeAction, Boolean isWorking) {
        this.token = token;
        this.typeBool = typeBool;
        this.timeAction = timeAction;
        this.isWorking = isWorking;
    }

    public Long getIdActions() {
        return idActions;
    }

    public void setIdActions(Long idActions) {
        this.idActions = idActions;
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
