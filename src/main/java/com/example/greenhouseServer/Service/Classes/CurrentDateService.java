package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.CurrentDate;
import com.example.greenhouseServer.Repository.CurrentDateRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.CurrentDateServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class CurrentDateService implements CurrentDateServiceIntr {

    private final CurrentDateRepositoryIntr currentDateRepositoryIntr;

    @Autowired
    public CurrentDateService(CurrentDateRepositoryIntr currentDateRepositoryIntr) {
        this.currentDateRepositoryIntr = currentDateRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(CurrentDate currentDate) {
        currentDateRepositoryIntr.save(currentDate);
    }
}
