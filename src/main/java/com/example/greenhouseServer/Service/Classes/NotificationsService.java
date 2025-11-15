package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Notifications;
import com.example.greenhouseServer.Repository.NotificationsRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.NotificationsServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class NotificationsService implements NotificationsServiceIntr {

    private final NotificationsRepositoryIntr notificationsRepositoryIntr;

    @Autowired
    public NotificationsService(NotificationsRepositoryIntr notificationsRepositoryIntr) {
        this.notificationsRepositoryIntr = notificationsRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Notifications notifications) {
        notificationsRepositoryIntr.save(notifications);
    }
}
