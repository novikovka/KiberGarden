package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Notifications;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NotificationsRepositoryIntr extends JpaRepository<Notifications, Long> {
}
