package com.example.greenhouseServer.Entity;

import com.example.greenhouseServer.Entity.EnumList.TypeValue;
import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.LocalTime;

@Entity
@Table(name = "sensor_data")
public class Indicators {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_date")
    private Long idDate;

    @JoinColumn(name = "token", referencedColumnName = "token")
    @NotEmpty(message = "token do not empty")
    @Size(min = 1, max = 30, message = "Size token is error")
    private String token;

    @Column(name = "type")
    @Enumerated(EnumType.STRING)
    @NotNull(message = "type do not empty")
    private TypeValue nameValue;

    @Column(name = "value")
    @Min(value = 0, message = "value do not < 0")
    private int value;

    @Column(name = "time")
    private LocalTime timeAction;

    public Indicators() {
    }

    public Indicators(String token, TypeValue nameValue, int value, LocalTime timeAction) {
        this.token = token;
        this.nameValue = nameValue;
        this.value = value;
        this.timeAction = timeAction;
    }

    public Long getIdDate() {
        return idDate;
    }

    public void setIdDate(Long idDate) {
        this.idDate = idDate;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
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
