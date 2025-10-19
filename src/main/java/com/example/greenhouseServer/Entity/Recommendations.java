package com.example.greenhouseServer.Entity;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "recommendations")
public class Recommendations {

    @Id
    @ManyToOne
    @JoinColumn(name = "telegram_id", referencedColumnName = "telegram_id")
    private Users user;

    @Column(name = "token")
    private String token;

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "text")
    private String text;

    public Recommendations() {
    }

    public Recommendations(Users user, String token, LocalDate date, String text) {
        this.user = user;
        this.token = token;
        this.date = date;
        this.text = text;
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
