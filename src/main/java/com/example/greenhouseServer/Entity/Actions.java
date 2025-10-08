package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name = "actions_tbl")
public class Actions {

    @Id
    @ManyToOne
    @JoinColumn(name = "id_tg_user", referencedColumnName = "id_tg_user")
    private Users user;

    @Column(name = "type")
    private TypeBool typeBool;

    @Column(name = "time")
    private LocalTime timeAction;

    public Actions() {
    }

    public Actions(Users user, TypeBool typeBool, LocalTime timeAction) {
        this.user = user;
        this.typeBool = typeBool;
        this.timeAction = timeAction;
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
