package com.example.greenhouseServer.Service.Interfaces;

import com.example.greenhouseServer.Entity.Indicators;
import org.springframework.http.ResponseEntity;

import java.time.LocalTime;

public interface IndicatorsServiceIntr {

    void save(Indicators indicators);

}
