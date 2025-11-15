package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Recommendations;
import com.example.greenhouseServer.Repository.RecommendationsRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.RecommendationsServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class RecommendationsService implements RecommendationsServiceIntr {

    private final RecommendationsRepositoryIntr recommendationsRepositoryIntr;

    @Autowired
    public RecommendationsService(RecommendationsRepositoryIntr recommendationsRepositoryIntr) {
        this.recommendationsRepositoryIntr = recommendationsRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Recommendations recommendations) {
        recommendationsRepositoryIntr.save(recommendations);
    }
}
