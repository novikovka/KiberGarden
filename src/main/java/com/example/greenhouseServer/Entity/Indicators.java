package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;

import java.time.LocalTime;

@Entity
@Table(name = "indicators_for_day")
public class Indicators {

    @Id
    @ManyToOne
    @JoinColumn(name = "id_tg_user", referencedColumnName = "id_tg_user")
    private Users user;

    @Column(name = "name_value")
    private TypeValue nameValue;

    @Column(name = "value")
    private int value;

    @Column(name = "time")
    private LocalTime timeAction;

    public Indicators() {
    }

    public Indicators(Users user, TypeValue nameValue, int value, LocalTime timeAction) {
        this.user = user;
        this.nameValue = nameValue;
        this.value = value;
        this.timeAction = timeAction;
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
