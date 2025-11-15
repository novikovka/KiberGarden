package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Indicators;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface IndicatorsRepositoryIntr extends JpaRepository<Indicators, Long> {
}
