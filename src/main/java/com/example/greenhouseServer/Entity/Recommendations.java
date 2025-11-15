package com.example.greenhouseServer.Entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;

@Entity
@Table(name = "recommendations")
public class Recommendations {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_recommendations")
    private Long idRecommendations;

    @JoinColumn(name = "token", referencedColumnName = "token")
    @NotEmpty(message = "token do not empty")
    @Size(min = 1, max = 30, message = "Size token is error")
    private String token;

    @Column(name = "date")
    @NotEmpty(message = "date do not empty")
    private LocalDate date;

    @Column(name = "text")
    private String text;

    public Recommendations() {
    }

    public Recommendations(String token, LocalDate date, String text) {
        this.token = token;
        this.date = date;
        this.text = text;
    }

    public Long getIdRecommendations() {
        return idRecommendations;
    }

    public void setIdRecommendations(Long idRecommendations) {
        this.idRecommendations = idRecommendations;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
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
