package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Indicators;
import com.example.greenhouseServer.Repository.IndicatorsRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.IndicatorsServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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
        indicatorsRepositoryIntr.save(indicators);
    }

}
