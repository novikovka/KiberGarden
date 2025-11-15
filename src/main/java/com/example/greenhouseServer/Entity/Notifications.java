package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "notifications")
public class Notifications {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_notifications")
    private Long idNotifications;

    @JoinColumn(name = "token", referencedColumnName = "token")
    @NotEmpty(message = "token do not empty")
    @Size(min = 1, max = 30, message = "Size token is error")
    private String token;

    @Column(name = "type")
    @Enumerated(EnumType.STRING)
    @NotEmpty(message = "type do not empty")
    private TypeValue nameValue;

    @Column(name = "value")
    @Min(value = 0, message = "value do not < 0")
    private int value;

    public Notifications() {
    }

    public Notifications(String token, TypeValue nameValue, int value) {
        this.token = token;
        this.nameValue = nameValue;
        this.value = value;
    }

    public Long getIdNotifications() {
        return idNotifications;
    }

    public void setIdNotifications(Long idNotifications) {
        this.idNotifications = idNotifications;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public TypeValue getNameValue() {
        return nameValue;
    }

    public void setNameValue(TypeValue nameValue) {
        this.nameValue = nameValue;
    }

}
