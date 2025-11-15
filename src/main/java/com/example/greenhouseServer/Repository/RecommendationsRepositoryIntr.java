package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Recommendations;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RecommendationsRepositoryIntr extends JpaRepository<Recommendations, Long> {
}
