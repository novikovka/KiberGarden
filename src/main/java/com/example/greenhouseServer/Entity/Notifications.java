package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;

@Entity
@Table(name = "notifications_tbl")
public class Notifications {
    @Id
    @ManyToOne
    @JoinColumn(name = "id_tg_user", referencedColumnName = "id_tg_user")
    private Users user;

    @Column(name = "name_value")
    private TypeValue nameValue;

    @Column(name = "value")
    private int value;

    public Notifications() {
    }

    public Notifications(Users user, TypeValue nameValue, int value) {
        this.user = user;
        this.nameValue = nameValue;
        this.value = value;
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
