package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "current_state")
public class CurrentDate {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_status")
    private Long idStatus;

    @JoinColumn(name = "token", referencedColumnName = "token")
    @NotEmpty(message = "token do not empty")
    @Size(min = 1, max = 30, message = "Size token is error")
    private String token;

    @Column(name = "type")
    @Enumerated(EnumType.STRING)
    @NotEmpty(message = "type do not empty")
    private TypeBool typeBool;

    @Column(name = "status")
    @NotEmpty(message = "bool working do not empty")
    private Boolean isWorking;

    public CurrentDate() {
    }

    public CurrentDate(String token, TypeBool typeBool, Boolean isWorking) {
        this.token = token;
        this.typeBool = typeBool;
        this.isWorking = isWorking;
    }

    public Long getIdStatus() {
        return idStatus;
    }

    public void setIdStatus(Long idStatus) {
        this.idStatus = idStatus;
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
}
