package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;

import java.time.LocalTime;

@Entity
@Table(name = "sensor_data")
public class Indicators {

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

    @Column(name = "time")
    private LocalTime timeAction;

    public Indicators() {
    }

    public Indicators(Users user, String token, TypeValue nameValue, int value, LocalTime timeAction) {
        this.user = user;
        this.token = token;
        this.nameValue = nameValue;
        this.value = value;
        this.timeAction = timeAction;
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

    public TypeValue getNameValue() {
        return nameValue;
    }

    public void setNameValue(TypeValue nameValue) {
        this.nameValue = nameValue;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public LocalTime getTimeAction() {
        return timeAction;
    }

    public void setTimeAction(LocalTime timeAction) {
        this.timeAction = timeAction;
    }
}
