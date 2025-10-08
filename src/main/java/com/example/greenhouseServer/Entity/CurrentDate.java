package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "current_date_tbl")
public class CurrentDate {

    @Id
    @Column(name = "id_tg_user")
    private Long id;

    @Column(name = "type")
    private TypeBool typeBool;

    @Column(name = "boolean")
    private Boolean isWorking;

    public CurrentDate() {
    }

    public CurrentDate(Long id, TypeBool typeBool, Boolean isWorking) {
        this.id = id;
        this.typeBool = typeBool;
        this.isWorking = isWorking;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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
