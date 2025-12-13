package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Indicators;
import com.example.greenhouseServer.Repository.IndicatorsRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.IndicatorsServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalTime;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
public class IndicatorsService implements IndicatorsServiceIntr {

    private final IndicatorsRepositoryIntr indicatorsRepositoryIntr;

    @Autowired
    public IndicatorsService(IndicatorsRepositoryIntr indicatorsRepositoryIntr) {
        this.indicatorsRepositoryIntr = indicatorsRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Indicators indicators) {
        Optional<Indicators> existingIndicator = indicatorsRepositoryIntr
                .findByTokenAndTimeAction(indicators.getToken(), indicators.getTimeAction());

        if (existingIndicator.isPresent()) {
            Indicators existing = existingIndicator.get();
            existing.setNameValue(indicators.getNameValue());
            existing.setValue(indicators.getValue());
            indicatorsRepositoryIntr.save(existing);
        } else {
            indicatorsRepositoryIntr.save(indicators);
        }
    }

}
