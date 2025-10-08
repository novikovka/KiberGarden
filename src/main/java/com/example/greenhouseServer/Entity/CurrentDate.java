package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.*;

@Entity
@Table(name = "current_date_tbl")
public class CurrentDate {
    @Id
    @ManyToOne
    @JoinColumn(name = "id_tg_user", referencedColumnName = "id_tg_user")
    private Users user;

    @Column(name = "type")
    private TypeBool typeBool;

    @Column(name = "boolean")
    private Boolean isWorking;

    public CurrentDate() {
    }

    public CurrentDate(TypeBool typeBool, Boolean isWorking) {
        this.typeBool = typeBool;
        this.isWorking = isWorking;
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
