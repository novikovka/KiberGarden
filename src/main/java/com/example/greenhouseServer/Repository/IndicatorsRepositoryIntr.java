package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Indicators;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalTime;
import java.util.Optional;

@Repository
public interface IndicatorsRepositoryIntr extends JpaRepository<Indicators, Long> {
    Optional<Indicators> findByTokenAndTimeAction(String token, LocalTime timeAction);
}
