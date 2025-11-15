package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Actions;
import com.example.greenhouseServer.Repository.ActionsRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.ActionsServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class ActionsService implements ActionsServiceIntr {

    private final ActionsRepositoryIntr actionsRepositoryIntr;

    @Autowired
    public ActionsService(ActionsRepositoryIntr actionsRepositoryIntr) {
        this.actionsRepositoryIntr = actionsRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Actions actions) {
        actionsRepositoryIntr.save(actions);
    }
}
