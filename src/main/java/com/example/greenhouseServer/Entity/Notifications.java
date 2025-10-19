package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;

@Entity
@Table(name = "notifications")
public class Notifications {

    @Id
    @ManyToOne
    @JoinColumn(name = "telegram_id", referencedColumnName = "telegram_id")
    private Users user;

    @Column(name = "token")
    private String token;

    @Column(name = "type")
    @Enumerated(EnumType.STRING)
    private TypeValue nameValue;

    @Column(name = "value")
    private int value;

    public Notifications() {
    }

    public Notifications(Users user, String token, TypeValue nameValue, int value) {
        this.user = user;
        this.token = token;
        this.nameValue = nameValue;
        this.value = value;
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

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }

}
