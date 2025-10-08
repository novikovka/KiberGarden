package com.example.greenhouseServer.Entity;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "recommendations_tbl")
public class Recommendations {

    @Id
    @ManyToOne
    @JoinColumn(name = "id_tg_user", referencedColumnName = "id_tg_user")
    private Users user;

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "text")
    private String text;

    public Recommendations() {
    }

    public Recommendations(Users user, LocalDate date, String text) {
        this.user = user;
        this.date = date;
        this.text = text;
    }

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
}
