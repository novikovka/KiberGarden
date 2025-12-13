package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UsersRepositoryIntr extends JpaRepository<Users, Long> {
    Users findByToken(String token);
}
