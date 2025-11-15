package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Actions;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ActionsRepositoryIntr extends JpaRepository<Actions, Long> {
}
